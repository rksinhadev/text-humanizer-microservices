const $ = id => document.getElementById(id);
const words = t => (t.trim().match(/\S+/g) || []).length;
let tone = "natural", mode = "login";
let token = localStorage.getItem("th_token") || "";
let user = JSON.parse(localStorage.getItem("th_user") || "null");

async function api(path, opts = {}) {
  const headers = {"Content-Type": "application/json"};
  if (token) headers.Authorization = "Bearer " + token;
  const r = await fetch("/api" + path, {...opts, headers});
  const d = await r.json().catch(() => ({}));
  if (!r.ok) {
    if (r.status === 401 && token && !path.startsWith("/auth/")) logout();
    throw new Error(d.error || d.message || "Request failed");
  }
  return d;
}

/* ---------- tone ---------- */
function setTone(t) {
  tone = t;
  document.querySelectorAll("#tones button").forEach(b => b.classList.toggle("active", b.dataset.tone === t));
}
$("tones").addEventListener("click", e => e.target.dataset.tone && setTone(e.target.dataset.tone));
$("input").addEventListener("input", () => $("inCount").textContent = words($("input").value) + " words");

/* ---------- nav / auth ---------- */
function btn(label, cls, fn) { const b = document.createElement("button"); b.textContent = label; b.className = cls; b.onclick = fn; return b; }
function renderNav() {
  const n = $("navR"); n.textContent = "";
  if (token) {
    const hi = document.createElement("span"); hi.textContent = "Hi, " + ((user && user.name) || "there");
    n.append(hi, btn("History", "nbtn", openHistory), btn("Log out", "nbtn", logout));
  } else n.append(btn("Log in", "nbtn", () => openAuth("login")), btn("Sign up", "nbtn fill", () => openAuth("signup")));
}
function logout() {
  token = ""; user = null; localStorage.removeItem("th_token"); localStorage.removeItem("th_user");
  $("drawer").classList.remove("on"); renderNav();
}
function openAuth(m) {
  mode = m; const s = m === "signup";
  $("name").style.display = s ? "" : "none"; $("name").required = s;
  $("authTitle").textContent = s ? "Create account" : "Welcome back";
  $("authBtn").textContent = s ? "Sign up" : "Log in";
  $("swap").textContent = s ? "Have an account? Log in" : "New here? Sign up";
  $("authErr").textContent = ""; $("modal").classList.add("on");
}
$("swap").onclick = () => openAuth(mode === "login" ? "signup" : "login");
$("closeAuth").onclick = () => $("modal").classList.remove("on");
$("authForm").onsubmit = async e => {
  e.preventDefault(); $("authErr").textContent = "";
  const email = $("email").value.trim(), password = $("pw").value, name = $("name").value.trim();
  $("authBtn").disabled = true;
  try {
    if (mode === "signup") await api("/auth/signup", {method: "POST", body: JSON.stringify({name, email, password})});
    const d = await api("/auth/login", {method: "POST", body: JSON.stringify({email, password})});
    token = d.token || d.access_token; user = d.user || {name};
    localStorage.setItem("th_token", token); localStorage.setItem("th_user", JSON.stringify(user));
    $("modal").classList.remove("on"); $("authForm").reset(); renderNav();
  } catch (err) { $("authErr").textContent = err.message; }
  $("authBtn").disabled = false;
};

/* ---------- history ---------- */
$("closeDrawer").onclick = () => $("drawer").classList.remove("on");
async function openHistory() { $("drawer").classList.add("on"); await loadHistory(); }
async function loadHistory() {
  const box = $("hist"); box.textContent = "Loading…";
  try {
    const {history} = await api("/history"); box.textContent = "";
    if (!history.length) { box.innerHTML = '<p class="empty">No saved results yet.</p>'; return; }
    history.forEach(h => {
      const el = document.createElement("div"); el.className = "item";
      const top = document.createElement("div"); top.className = "top";
      top.append(Object.assign(document.createElement("span"), {textContent: h.tone}),
                 Object.assign(document.createElement("span"), {textContent: new Date(h.created_at).toLocaleString()}));
      const p = document.createElement("p"); p.textContent = h.humanized_text || h.original_text;
      const row = document.createElement("div"); row.className = "row";
      row.append(btn("Use", "nbtn", () => {
        $("input").value = h.original_text; $("input").dispatchEvent(new Event("input"));
        $("output").textContent = h.humanized_text || ""; $("output").className = "result done";
        $("outCount").textContent = words(h.humanized_text || "") + " words"; setTone(h.tone);
        $("drawer").classList.remove("on");
      }), btn("Copy", "nbtn", () => navigator.clipboard.writeText(h.humanized_text || "")),
      btn("Delete", "nbtn", async () => {
        try { await api("/history/" + h.id, {method: "DELETE"}); el.remove(); } catch (e) { alert(e.message); }
      }));
      el.append(top, p, row); box.append(el);
    });
  } catch (e) { box.textContent = e.message; }
}

/* ---------- humanize ---------- */
$("go").addEventListener("click", async () => {
  const text = $("input").value.trim();
  $("err").textContent = "";
  if (!text) return $("err").textContent = "Please paste some text first.";
  $("go").disabled = true; $("loader").classList.add("on");
  try {
    const d = await api("/humanize", {method: "POST", body: JSON.stringify({text, tone})});
    $("output").textContent = d.humanized_text; $("output").className = "result done";
    $("outCount").textContent = words(d.humanized_text) + " words";
    let meta = d.mode === "transformer" ? d.changed_sentences + " sentences rewritten by " + d.model
      : (d.model_error ? "Model failed to load, rules only. See the ai_service terminal." : "Model made no changes, rules only");
    if (token) {
      try {
        await api("/history", {method: "POST", body: JSON.stringify({original_text: text, humanized_text: d.humanized_text, tone, status: "completed"})});
        meta += " · saved to history";
        if ($("drawer").classList.contains("on")) loadHistory();
      } catch (e) { meta += " · not saved (" + e.message + ")"; }
    } else meta += " · log in to save results";
    $("meta").textContent = meta;
  } catch (e) { $("err").textContent = e.message; }
  $("go").disabled = false; $("loader").classList.remove("on");
});
$("copy").addEventListener("click", async () => {
  await navigator.clipboard.writeText($("output").textContent);
  $("copy").textContent = "Copied ✓"; setTimeout(() => $("copy").textContent = "Copy", 1500);
});
$("clear").addEventListener("click", () => {
  $("input").value = ""; $("output").textContent = "Your result appears here."; $("output").className = "result";
  $("inCount").textContent = $("outCount").textContent = "0 words"; $("meta").textContent = "";
});

/* ---------- AI status ---------- */
function checkHealth() {
  fetch("/api/health").then(r => r.json()).then(d => {
    const st = d.model_state, label = $("status").lastChild;
    if (st === "ready") { $("status").className = "pill ok"; label.textContent = "Model ready · " + d.model; }
    else if (st === "error") { $("status").className = "pill bad"; label.textContent = "Model failed to load (rules only)"; }
    else if (st === "disabled") { $("status").className = "pill ok"; label.textContent = "Rules mode"; }
    else { $("status").className = "pill"; label.textContent = "Loading model…"; setTimeout(checkHealth, 3000); }
  }).catch(() => { $("status").className = "pill bad"; $("status").lastChild.textContent = "AI service offline"; });
}
renderNav(); checkHealth();