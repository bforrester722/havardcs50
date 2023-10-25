// builts alerts with bootstrap
const messages = [];

function addMessage(text, type) {
  const messageObj = { text, type };
  messages.push(messageObj);
  renderMessages();

  // Schedule the removal of the message after 5000 ms (5 seconds)
  setTimeout(() => {
    removeMessage(messageObj);
  }, 3000);
}

function removeMessage(message) {
  const alertWrapper = document.getElementById("alertWrapper");
  const alertDiv = alertWrapper.querySelector(".alert");

  // If there are no messages or no alertDiv, return
  if (messages.length === 0 || !alertDiv) {
    return;
  }

  alertDiv.offsetHeight;
  alertDiv.style.opacity = 0;

  setTimeout(() => {
    const index = messages.indexOf(message);
    if (index !== -1) {
      messages.splice(index, 1);
      renderMessages();
    }
  }, 500);
}

function renderMessages() {
  const alertWrapper = document.getElementById("alertWrapper");
  alertWrapper.innerHTML = ""; // Clear existing messages

  messages.forEach((message) => {
    const alertDiv = document.createElement("div");
    alertDiv.className = `alert ${message.type} alert-dismissible fade show m-3`;
    alertDiv.setAttribute("role", "alert");

    const closeButton = document.createElement("button");
    closeButton.type = "button";
    closeButton.className = "close";
    closeButton.setAttribute("data-dismiss", "alert");
    closeButton.setAttribute("aria-label", "Close");

    const closeSymbol = document.createElement("span");
    closeSymbol.setAttribute("aria-hidden", "true");
    closeSymbol.innerHTML = "&times;";

    closeButton.appendChild(closeSymbol);
    alertDiv.appendChild(closeButton);

    const messageText = document.createTextNode(message.text);
    alertDiv.appendChild(messageText);

    closeButton.addEventListener("click", () => {
      removeMessage(message);
    });

    alertWrapper.appendChild(alertDiv);

    alertDiv.offsetHeight;
    alertDiv.style.opacity = 1;
  });
}
