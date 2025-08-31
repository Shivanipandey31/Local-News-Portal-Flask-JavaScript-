const API = "http://127.0.0.1:5000";

// ---------------- SIGN UP ----------------
document.querySelector("#signup-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.querySelector("#signup-username").value.trim();
  const password = document.querySelector("#signup-password").value.trim();

  const res = await fetch(`${API}/api/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await res.json();
  alert(data.message || data.error);
});

// ---------------- LOGIN ----------------
document.querySelector("#login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.querySelector("#login-username").value.trim();
  const password = document.querySelector("#login-password").value.trim();

  const res = await fetch(`${API}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await res.json();

  if (data.success) {
    localStorage.setItem("jwt_token", data.access_token);
    alert("Logged in!");
    loadArticles();
  } else {
    alert(data.error || "Login failed");
  }
});

// ---------------- CREATE ARTICLE ----------------
document.querySelector("#create-article-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const token = localStorage.getItem("jwt_token");
  if (!token) return alert("Please login first.");

  const title = document.querySelector("#article-title").value.trim();
  const source = document.querySelector("#article-source").value.trim();
  const content = document.querySelector("#article-content").value.trim();

  const res = await fetch(`${API}/api/articles`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    body: JSON.stringify({ title, source, content }),
  });
  const data = await res.json();

  if (data.success) {
    alert("Article published!");
    loadArticles(); 
  } else {
    alert(data.error || "Failed to publish");
  }
});

// ---------------- LOAD ARTICLES ----------------
async function loadArticles() {
  try {
    const res = await fetch(`${API}/api/articles`);
    const data = await res.json();
    if (!data.success) return alert("Failed to load articles");
    renderArticles(data.data || []);
  } catch (err) {
    console.error("Error loading articles:", err);
  }
}

function renderArticles(articles) {
  const el = document.querySelector("#articles-container");
  el.innerHTML = (articles || []).map(a => `
    <div class="article-card">
      <h3>${a.title}</h3>
      <p>${a.content}</p>
      <small>Source: ${a.source} | By: ${a.username || "unknown"}</small>
    </div>
  `).join("");
}

// ---------------- AUTO LOAD ON PAGE OPEN ----------------
document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("jwt_token");
  if (token) {
    loadArticles();
  }
});
