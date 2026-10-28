import os, re, threading
from flask import Flask, request, jsonify

app = Flask(__name__)

MAX_TEXT_LENGTH = 20000
ALLOWED_TONES = {"natural", "formal", "casual", "academic"}
# A paraphrase model. facebook/bart-large-cnn is a summariser and mostly copies text back.
MODEL_NAME = os.getenv("HF_MODEL", "humarin/chatgpt_paraphraser_on_T5_base")
USE_MODEL = os.getenv("USE_MODEL", "true").lower() == "true"

_tok = _model = None
_lock = threading.Lock()
_state = {"status": "idle" if USE_MODEL else "disabled", "error": None}


def load_model():
    global _tok, _model
    with _lock:
        if _model is not None or not USE_MODEL or _state["status"] == "error":
            return
        _state["status"] = "loading"
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            _tok = AutoTokenizer.from_pretrained(MODEL_NAME)
            _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).eval()
            _state["status"] = "ready"
        except Exception as e:
            _state.update(status="error", error=str(e))
            app.logger.warning("Model load failed: %s", e)


def paraphrase(sentences):
    import torch
    prefix = "paraphrase: " if "t5" in MODEL_NAME.lower() else ""
    out = []
    for i in range(0, len(sentences), 8):
        enc = _tok([prefix + s for s in sentences[i:i + 8]], return_tensors="pt",
                   padding=True, truncation=True, max_length=256)
        with torch.no_grad():
            gen = _model.generate(**enc, do_sample=True, top_p=0.92, temperature=0.9,
                                  no_repeat_ngram_size=3, repetition_penalty=1.2,
                                  max_new_tokens=int(enc["input_ids"].shape[1] * 1.4) + 16)
        out += _tok.batch_decode(gen, skip_special_tokens=True)
    return out


def norm(s):
    return re.sub(r"\W+", " ", s).lower().strip()


def rewrite_with_model(text):
    """Returns (text, changed_sentences, model_used)."""
    load_model()
    if _model is None:
        return text, 0, False
    changed, paragraphs = 0, []
    for para in text.split("\n"):
        sents = [s for s in re.split(r"(?<=[.!?])\s+", para.strip()) if s]
        todo = [i for i, s in enumerate(sents) if len(s.split()) >= 4]
        if todo:
            new = paraphrase([sents[i] for i in todo])
            for i, n in zip(todo, new):
                n = n.strip()
                if n and norm(n) != norm(sents[i]):
                    sents[i] = n
                    changed += 1
        paragraphs.append(" ".join(sents))
    return "\n".join(paragraphs), changed, True


# ---------- rule-based layer (always runs; also the fallback) ----------
FILLERS = [r"it is (?:important|worth) to (?:note|mention|remember) that,?\s*",
           r"in today's (?:fast-paced |digital |modern )?world,?\s*",
           r"in conclusion,?\s*", r"it goes without saying that\s*"]
STIFF = {"utilize": "use", "utilise": "use", "leverage": "use", "furthermore": "also",
         "moreover": "also", "additionally": "also", "in order to": "to",
         "delve into": "dig into", "crucial": "key", "pivotal": "key", "numerous": "many",
         "commence": "start", "endeavor": "try", "a plethora of": "plenty of",
         "due to the fact that": "because", "in the realm of": "in", "facilitate": "help with",
         "plays a vital role": "matters", "ensure that": "make sure", "therefore": "so",
         "consequently": "so", "however": "but", "nevertheless": "still"}
PAIRS = [("do not", "don't"), ("does not", "doesn't"), ("did not", "didn't"), ("is not", "isn't"),
         ("are not", "aren't"), ("cannot", "can't"), ("will not", "won't"), ("it is", "it's"),
         ("that is", "that's"), ("they are", "they're"), ("we are", "we're"), ("I am", "I'm"),
         ("would not", "wouldn't"), ("have not", "haven't")]


def sub_keep_case(text, pat, rep):
    def fn(m):
        return rep[:1].upper() + rep[1:] if m.group(0)[:1].isupper() else rep
    return re.sub(pat, fn, text, flags=re.I)


def tone_pass(text, tone):
    text = text.replace(" — ", ", ").replace("—", ", ")
    if tone in ("natural", "casual"):
        for f in FILLERS:
            text = re.sub(f, "", text, flags=re.I)
        for k, v in STIFF.items():
            if tone == "natural" and k in ("however", "therefore", "consequently", "nevertheless"):
                continue
            text = sub_keep_case(text, r"\b" + re.escape(k) + r"\b", v)
        for full, short in PAIRS:
            text = sub_keep_case(text, r"\b" + re.escape(full) + r"\b", short)
    else:
        for full, short in PAIRS:
            text = sub_keep_case(text, r"\b" + re.escape(short) + r"\b", full)
    text = re.sub(r"\b(but|so|still),", r"\1", text, flags=re.I)
    text = re.sub(r"[ \t]{2,}", " ", text).strip()
    return re.sub(r"(^|[.!?]\s+)([a-z])", lambda m: m.group(1) + m.group(2).upper(), text)


@app.get("/health")
def health():
    return jsonify({"service": "ai-service", "status": "ok", "model": MODEL_NAME,
                    "model_enabled": USE_MODEL, "model_state": _state["status"],
                    "model_error": _state["error"]}), 200


@app.post("/ai/humanize")
def humanize():
    data = request.get_json(silent=True) or {}
    text, tone = data.get("text"), data.get("tone", "natural")
    if not isinstance(text, str):
        return jsonify({"error": "Text must be a string"}), 400
    text = text.strip()
    if not text:
        return jsonify({"error": "Text cannot be empty"}), 400
    if len(text) > MAX_TEXT_LENGTH:
        return jsonify({"error": f"Text cannot exceed {MAX_TEXT_LENGTH} characters"}), 400
    if not isinstance(tone, str) or tone not in ALLOWED_TONES:
        return jsonify({"error": "Invalid tone", "allowed_tones": sorted(ALLOWED_TONES)}), 400

    rewritten, changed, used = rewrite_with_model(text)
    result = tone_pass(rewritten, tone)
    return jsonify({"mode": "transformer" if used and changed else "rules",
                    "model": MODEL_NAME if used else None, "changed_sentences": changed,
                    "model_error": _state["error"], "tone": tone,
                    "original_text": text, "humanized_text": result}), 200


if __name__ == "__main__":
    if USE_MODEL:
        threading.Thread(target=load_model, daemon=True).start()  # download/load in background
    app.run(host="127.0.0.1", port=5003, debug=False)