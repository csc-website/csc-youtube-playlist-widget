async function loadVideos() {
  const container = document.getElementById("videos");

  try {
    const response = await fetch("./videos.json?v=" + Date.now(), {
      cache: "no-store"
    });

    if (!response.ok) {
      throw new Error("Unable to load videos.");
    }

    const videos = await response.json();

    if (!Array.isArray(videos) || videos.length === 0) {
      throw new Error("No videos available.");
    }

    container.innerHTML = "";

    videos.slice(0, 5).forEach((video) => {
      const article = document.createElement("article");
      article.className = "video";

      const thumbnailLink = document.createElement("a");
      thumbnailLink.className = "video-thumbnail";
      thumbnailLink.href = video.link;
      thumbnailLink.target = "_blank";
      thumbnailLink.rel = "noopener noreferrer";

      const thumbnail = document.createElement("img");
      thumbnail.src = video.thumbnail;
      thumbnail.alt = video.title;
      thumbnail.loading = "lazy";

      thumbnailLink.appendChild(thumbnail);

      const info = document.createElement("div");
      info.className = "video-info";

      const title = document.createElement("h2");
      title.className = "video-title";

      const titleLink = document.createElement("a");
      titleLink.href = video.link;
      titleLink.target = "_blank";
      titleLink.rel = "noopener noreferrer";
      titleLink.textContent = video.title;

      title.appendChild(titleLink);

      const date = document.createElement("p");
      date.className = "video-date";
      date.textContent = video.date;

      info.appendChild(title);
      info.appendChild(date);

      article.appendChild(thumbnailLink);
      article.appendChild(info);

      container.appendChild(article);
    });

  } catch (error) {
    console.error("YouTube widget error:", error);
    container.innerHTML =
      '<p class="status">Unable to load videos.</p>';
  }
}

loadVideos();
