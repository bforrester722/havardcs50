// CSRF protection with AJAX
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

// handle heart like toggle status
document.querySelectorAll(".fa-heart, .fa-heart-o").forEach((el) => {
  el.onclick = async function () {
    const postId = el.dataset.postId;
    // request to the to toggle the like status for the post
    await fetch(`/toggle_like/${postId}`)
      .then((response) => response.json())
      .then((data) => {
         if (data.liked) {
          el.classList.remove("fa-heart-o");
          el.classList.add("fa-heart");
        } else {
          el.classList.remove("fa-heart");
          el.classList.add("fa-heart-o");
        }
        
        // Update the like count for the post.
        const likeCountSpan = document.querySelector(`#like-count-${postId}`);
        likeCountSpan.textContent = data.like_count;
      });
  };
});

// handles edit clicked and saving 
async function editBtnClicked(postId) {
  const postElement = document.querySelector(`#post-${postId}`);
  const editForm = postElement.querySelector(".edit-form");
  const btn = postElement.querySelector(`#edit-btn-${postId}`);

  // Toggle the display of the edit form
  editForm.style.display =
    editForm.style.display === "block" ? "none" : "block";

  if (editForm.style.display === "block") {
    // Hide the post text
    const postText = postElement.querySelector(`#post-text-${postId}`);
    btn.innerHTML = "Save";
    postText.style.display = "none";
  } else {
    // Show the post text
    const postText = postElement.querySelector(`#post-text-${postId}`);
    postText.style.display = "block";
    btn.innerHTML = "Edit";
    // Save the edited content
    const editedContent = editForm.querySelector("textarea").value;
    await fetch(`/edit_post/${postId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": getCookie("csrftoken"), 
      },
      body: `edited_content=${encodeURIComponent(editedContent)}`,
    })
      .then((response) => response.json())
      .then((data) => {
        // Update the post content if the update was successful
        if (data.success) {
          postText.textContent = data.updated_text;
        }
      });
  }
}


