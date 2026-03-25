const feed = document.getElementById("feed");

// sample images (you can replace with API later)
const images = [
  "https://picsum.photos/id/1015/600/900",
  "https://picsum.photos/id/1016/600/900",
  "https://picsum.photos/id/1018/600/900",
  "https://picsum.photos/id/1020/600/900",
  "https://picsum.photos/id/1024/600/900"
];

// function to create post
function createPost(src) {
  const post = document.createElement("div");
  post.className = "post";

  post.innerHTML = `
    <img src="${src}">
    <div class="caption">
      <h4>@user</h4>
      <p>Nice post 🔥</p>
    </div>
  `;

  feed.appendChild(post);
}

// load initial posts
function loadPosts() {
  for (let i = 0; i < images.length; i++) {
    createPost(images[i]);
  }
}

loadPosts();

// INFINITE SCROLL (horizontal)
feed.addEventListener("scroll", () => {
  if (feed.scrollLeft + feed.clientWidth >= feed.scrollWidth - 5) {
    // add more posts when reaching end
    loadPosts();
  }
});



document.getElementById("home").onclick = () => {
  alert("Home clicked 🏠");
};

document.getElementById("search").onclick = () => {
  alert("Search clicked 🔍");
};

document.getElementById("reels").onclick = () => {
  alert("Reels clicked 🎬");
};

document.getElementById("like").onclick = () => {
  alert("Notifications ❤️");
};

document.getElementById("message").onclick = () => {
  alert("Messages 💬");
};

document.getElementById("profile").onclick = () => {
  alert("Profile 👤");
};






