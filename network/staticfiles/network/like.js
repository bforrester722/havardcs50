document.querySelectorAll(".fa-heart").forEach((div) => {
  div.onclick = function () {
    likeDislike(this);
  };
});

async function likeDislike(element) {
  await fetch(`/toggle_like/${element.dataset.id}`)
    .then((response) => response.json())
    .then((data) => {
      element.className = data.css_class;
      element.querySelector("small").innerHTML = data.total_likes;
    });
}
