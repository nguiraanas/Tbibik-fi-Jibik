const chatBox = document.getElementById("chat-box");
const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");

async function sendMessage() {
  const query = userInput.value.trim();
  if (!query) return;

  // Afficher le message utilisateur
  appendMessage("user", query);
  userInput.value = "";

  // Requête POST vers ton API FastAPI
  try {
    const res = await fetch("http://127.0.0.1:8000/ask?query=" + encodeURIComponent(query), {
      method: "POST"
    });
    const data = await res.json();
    appendMessage("bot", data.answer);
  } catch (error) {
    appendMessage("bot", "❌ Erreur de connexion au serveur.");
    console.error(error);
  }
}

function appendMessage(sender, text) {
  const div = document.createElement("div");
  div.classList.add("message", sender);
  div.innerText = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", e => {
  if (e.key === "Enter") sendMessage();
});
