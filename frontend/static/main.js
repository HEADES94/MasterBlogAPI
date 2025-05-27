async function fetchPosts() {
  const res = await fetch('http://localhost:5002/api/posts');
  const posts = await res.json();
  renderPosts(posts);
}

function renderPosts(posts) {
  const container = document.getElementById('posts-container');
  container.innerHTML = '';
  posts.forEach(post => {
    const card = document.createElement('div');
    card.className = 'post-card';
    card.innerHTML = `
      <h2>${post.title}</h2>
      <p><em>by ${post.author} | ${post.category} | ${post.date}</em></p>
      <p>${post.content}</p>
      <p>❤️ Likes: <span id="likes-${post.id}">${post.likes}</span></p>
      <div class="actions">
        <button onclick="likePost(${post.id})">Like</button>
        <button onclick="deletePost(${post.id})">Delete</button>
      </div>
      <div class="comment-section">
        <input id="comment-${post.id}" placeholder="Add a comment..." />
        <button onclick="addComment(${post.id})">Comment</button>
        <ul id="comments-${post.id}"></ul>
      </div>
    `;
    container.appendChild(card);
  });
}

async function likePost(id) {
  const res = await fetch(`http://localhost:5002/api/posts/${id}/like`, { method: 'POST' });
  const data = await res.json();
  document.getElementById(`likes-${id}`).innerText = data.likes;
}

async function deletePost(id) {
  if (!confirm("Delete this post?")) return;
  await fetch(`http://localhost:5002/api/posts/${id}`, { method: 'DELETE' });
  fetchPosts();
}

function addComment(id) {
  const input = document.getElementById(`comment-${id}`);
  const list = document.getElementById(`comments-${id}`);
  if (input.value.trim() !== '') {
    const li = document.createElement('li');
    li.innerText = input.value;
    list.appendChild(li);
    input.value = '';
  }
}

function toggleDarkMode() {
  document.body.classList.toggle('dark-mode');
}

window.onload = fetchPosts;
