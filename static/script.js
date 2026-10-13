
const API = "";

let authMode = "login";
let currentOutput = "";

const $ = (id) => document.getElementById(id);

function getToken() {
    return localStorage.getItem("textHumanizerToken");
}

function authHeaders() {
    const token = getToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
}

async function apiRequest(path, options = {}) {
    const response = await fetch(`${API}${path}`, {
        ...options,
        headers: {
            ...(options.body ? { "Content-Type": "application/json" } : {}),
            ...authHeaders(),
            ...(options.headers || {})
        }
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.error || data.message || `Request failed (${response.status})`);
    }

    return data;
}

function showNotice(message, isError = false) {
    const notice = $("notice");
    notice.textContent = message;
    notice.classList.remove("hidden", "error");
    if (isError) notice.classList.add("error");
}

function hideNotice() {
    $("notice").classList.add("hidden");
}

function showSection(section) {
    ["humanizerSection", "authSection", "historySection"].forEach(id => {
        $(id).classList.toggle("hidden", id !== section);
    });

    $("homeNav").classList.toggle("active", section === "humanizerSection");
    $("historyNav").classList.toggle("active", section === "historySection");
    $("authNav").classList.toggle("active", section === "authSection");

    hideNotice();

    if (section === "historySection") {
        loadHistory();
    }
}

function updateAuthUI() {
    const loggedIn = Boolean(getToken());
    $("logoutBtn").classList.toggle("hidden", !loggedIn);
    $("authNav").textContent = loggedIn ? "Account" : "Login / Signup";
}

function setAuthMode(mode) {
    authMode = mode;
    const isSignup = mode === "signup";

    $("nameGroup").classList.toggle("hidden", !isSignup);
    $("name").required = isSignup;
    $("password").autocomplete = isSignup ? "new-password" : "current-password";
    $("loginTab").classList.toggle("active", !isSignup);
    $("signupTab").classList.toggle("active", isSignup);
    $("authSubmitBtn").textContent = isSignup ? "Create Account" : "Login";
}

$("homeNav").addEventListener("click", () => showSection("humanizerSection"));
$("historyNav").addEventListener("click", () => {
    if (!getToken()) {
        showSection("authSection");
        showNotice("Please login to view your history.", true);
        return;
    }
    showSection("historySection");
});

$("authNav").addEventListener("click", () => showSection("authSection"));
$("loginTab").addEventListener("click", () => setAuthMode("login"));
$("signupTab").addEventListener("click", () => setAuthMode("signup"));

$("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("textHumanizerToken");
    updateAuthUI();
    showSection("humanizerSection");
    showNotice("You have been logged out.");
});

$("inputText").addEventListener("input", () => {
    $("charCount").textContent = `${$("inputText").value.length} characters`;
});

$("authForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    hideNotice();

    const payload = {
        email: $("email").value.trim(),
        password: $("password").value
    };

    if (authMode === "signup") {
        payload.name = $("name").value.trim();
    }

    const endpoint = authMode === "signup" ? "/auth/signup" : "/auth/login";
    const button = $("authSubmitBtn");
    button.disabled = true;

    try {
        const data = await apiRequest(endpoint, {
            method: "POST",
            body: JSON.stringify(payload)
        });

        if (authMode === "signup") {
            setAuthMode("login");
            $("password").value = "";
            showNotice(data.message || "Account created. Please login.");
        } else {
            const token = data.token || data.access_token;
            if (!token) {
                throw new Error("Login response did not include a token.");
            }

            localStorage.setItem("textHumanizerToken", token);
            updateAuthUI();
            $("authForm").reset();
            showSection("humanizerSection");
            showNotice("Login successful!");
        }
    } catch (error) {
        showNotice(error.message, true);
    } finally {
        button.disabled = false;
    }
});

$("humanizeBtn").addEventListener("click", async () => {
    hideNotice();

    const text = $("inputText").value.trim();
    const tone = $("tone").value;

    if (!text) {
        showNotice("Please enter some text first.", true);
        return;
    }

    const button = $("humanizeBtn");
    button.disabled = true;
    button.textContent = "Processing...";

    $("outputContainer").classList.add("hidden");

    try {
        // Validate text through the Text Service.
        await apiRequest("/text/validate", {
            method: "POST",
            body: JSON.stringify({ text })
        });

        // Send the text to the AI Service.
        const result = await apiRequest("/ai/humanize", {
            method: "POST",
            body: JSON.stringify({ text, tone })
        });

        currentOutput = result.humanized_text || "";
        $("outputText").textContent = currentOutput;
        $("outputContainer").classList.remove("hidden");

        if (getToken()) {
            try {
                await apiRequest("/history", {
                    method: "POST",
                    body: JSON.stringify({
                        original_text: text,
                        humanized_text: currentOutput,
                        tone,
                        status: "completed"
                    })
                });
                showNotice("Text processed and history saved.");
            } catch (error) {
                showNotice(`Text processed, but history was not saved: ${error.message}`, true);
            }
        } else {
            showNotice("Text processed. Login to save your history.");
        }
    } catch (error) {
        showNotice(error.message, true);
    } finally {
        button.disabled = false;
        button.textContent = "Humanize Text";
    }
});

$("copyBtn").addEventListener("click", async () => {
    try {
        await navigator.clipboard.writeText(currentOutput);
        showNotice("Output copied to clipboard.");
    } catch {
        showNotice("Could not copy automatically. Please select and copy the text.", true);
    }
});

function addText(parent, tag, text, className = "") {
    const element = document.createElement(tag);
    element.textContent = text ?? "";
    if (className) element.className = className;
    parent.appendChild(element);
    return element;
}

async function loadHistory() {
    const list = $("historyList");
    list.replaceChildren();

    if (!getToken()) {
        addText(list, "p", "Please login to view your history.");
        return;
    }

    addText(list, "p", "Loading history...", "muted");

    try {
        const data = await apiRequest("/history");
        list.replaceChildren();

        const records = Array.isArray(data.history) ? data.history : [];

        if (records.length === 0) {
            addText(list, "p", "No history records found.", "muted");
            return;
        }

        records.forEach(record => {
            const item = document.createElement("article");
            item.className = "history-item";

            addText(item, "h3", `Record #${record.id}`);
            addText(
                item,
                "div",
                `Tone: ${record.tone || "natural"} | Status: ${record.status || "unknown"}`,
                "history-meta"
            );

            if (record.created_at) {
                addText(item, "div", `Created: ${record.created_at}`, "history-meta");
            }

            addText(item, "strong", "Original text");
            addText(item, "p", record.original_text || "");

            addText(item, "strong", "Processed text");
            addText(item, "p", record.humanized_text || "No processed text available.");

            const actions = document.createElement("div");
            actions.className = "history-actions";

            const deleteButton = document.createElement("button");
            deleteButton.className = "delete-btn";
            deleteButton.textContent = "Delete";
            deleteButton.addEventListener("click", async () => {
                if (!confirm("Delete this history record?")) return;

                deleteButton.disabled = true;
                try {
                    await apiRequest(`/history/${record.id}`, {
                        method: "DELETE"
                    });
                    showNotice("History record deleted.");
                    await loadHistory();
                } catch (error) {
                    showNotice(error.message, true);
                    deleteButton.disabled = false;
                }
            });

            actions.appendChild(deleteButton);
            item.appendChild(actions);
            list.appendChild(item);
        });
    } catch (error) {
        list.replaceChildren();
        addText(list, "p", error.message, "muted");
        showNotice(`Could not load history: ${error.message}`, true);
    }
}

$("refreshHistoryBtn").addEventListener("click", loadHistory);

updateAuthUI();
setAuthMode("login");
showSection("humanizerSection");
