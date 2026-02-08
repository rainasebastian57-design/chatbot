const chatEl = document.getElementById("chat");
const form = document.getElementById("form");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");

const chatListEl = document.getElementById("chatList");
const newChatBtn = document.getElementById("newChatBtn");
const chatTitleEl = document.getElementById("chatTitle");
const renameBtn = document.getElementById("renameBtn");
const deleteBtn = document.getElementById("deleteBtn");

let currentChatId = null;
let chatsCache = [];

function addMessage(role, text) {
  const row = document.createElement("div");
  row.className = `msg ${role}`;
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  row.appendChild(bubble);
  chatEl.appendChild(row);
  chatEl.scrollTop = chatEl.scrollHeight;
}

function setSending(state) {
  sendBtn.disabled = state;
  input.disabled = state;
}

function clearChatUI() {
  chatEl.innerHTML = "";
}

function escapeHtml(s) {
  return (s || "").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;");
}

function renderChatList(chats) {
  chatListEl.innerHTML = "";
  chats.forEach(c => {
    const item = document.createElement("div");
    item.className = "chat-item" + (c.id === currentChatId ? " active" : "");
    item.innerHTML = `
      <div>${escapeHtml(c.title)}</div>
      <small>${escapeHtml(c.updated || "")}</small>
    `;
    item.addEventListener("click", () => loadChat(c.id));
    chatListEl.appendChild(item);
  });
}

async function fetchChats() {
  const res = await fetch("/chats");
  const data = await res.json();
  chatsCache = data.chats || [];

  if (!currentChatId && chatsCache.length) {
    currentChatId = chatsCache[0].id;
  }

  renderChatList(chatsCache);

  if (currentChatId) {
    await loadChat(currentChatId, false);
  }
}

async function loadChat(chatId, refreshList = true) {
  currentChatId = chatId;

  const meta = chatsCache.find(c => c.id === chatId);
  chatTitleEl.textContent = meta ? meta.title : "Chat";

  clearChatUI();
  addMessage("bot", "🔁 Opened previous conversation.");

  const res = await fetch(`/chats/${chatId}`);
  const data = await res.json();
  const messages = data.messages || [];

  for (const m of messages) {
    const role = m.role === "user" ? "user" : "bot";
    const text = m.parts?.[0]?.text || "";
    if (text.trim()) addMessage(role, text);
  }

  if (refreshList) {
    await fetchChats();
  } else {
    renderChatList(chatsCache);
  }
}

async function createNewChat() {
  const res = await fetch("/chats", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ title: "New chat" })
  });
  const data = await res.json();
  currentChatId = data.id;
  await fetchChats();
}

async function renameCurrentChat() {
  if (!currentChatId) return;
  const newTitle = prompt("Enter new chat title:");
  if (!newTitle) return;

  await fetch(`/chats/${currentChatId}/rename`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ title: newTitle })
  });

  await fetchChats();
}

async function deleteCurrentChat() {
  if (!currentChatId) return;
  if (!confirm("Delete this chat?")) return;

  await fetch(`/chats/${currentChatId}/delete`, { method: "POST" });

  currentChatId = null;
  await fetchChats();
}

async function sendMessage(text) {
  if (!currentChatId) return;

  addMessage("user", text);
  setSending(true);

  try {
    const res = await fetch(`/chats/${currentChatId}/message`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    addMessage("bot", data.reply || "No reply.");
    await fetchChats();
  } catch {
    addMessage("bot", "❌ Error: Could not reach server.");
  } finally {
    setSending(false);
    input.focus();
  }
}

/* Events */
form.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  sendMessage(text);
});

document.querySelectorAll("[data-quick]").forEach(btn => {
  btn.addEventListener("click", () => sendMessage(btn.getAttribute("data-quick")));
});

newChatBtn.addEventListener("click", createNewChat);
renameBtn.addEventListener("click", renameCurrentChat);
deleteBtn.addEventListener("click", deleteCurrentChat);

/* Start */
fetchChats();
