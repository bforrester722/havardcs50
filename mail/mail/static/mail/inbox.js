document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);
  document.querySelector("#compose-form").onsubmit = compose_submitted;
  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views
  hide_show("compose-view");

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function load_mailbox(mailbox) {
  hide_show("emails-view");

  const emailsView = document.querySelector("#emails-view");
  // Show the mailbox name
  emailsView.innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      const ulEl = document.createElement("ul");
      // Iterate through the emails
      emails.forEach((email) => {
        const listItem = createEmailListItem(email, mailbox);
        ulEl.appendChild(listItem);
      });
      emailsView.appendChild(ulEl);
    });
}

// creats an li for emails
function createEmailListItem(email, mailbox) {
  const listItem = document.createElement("li");
  listItem.classList.add(
    "list-group-item",
    email.read ? "bg-light" : "bg-white"
  );
  listItem.addEventListener("click", () => load_email(email, mailbox));

  listItem.innerHTML = `
    <span class="font-weight-bold pr-3">${email.sender}</span>
    <span>${email.subject}</span>
    <span class="float-right text-secondary">${email.timestamp}</span>
  `;
  return listItem;
}

// submits email form on submit
function compose_submitted(event) {
  event.preventDefault();
  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      body: document.querySelector("#compose-body").value,
      recipients: document.querySelector("#compose-recipients").value,
      subject: document.querySelector("#compose-subject").value,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      result.error
        ? addMessage(result.error, "alert-danger")
        : (addMessage("Email sent successfully", "alert-success"),
          load_mailbox("sent"));
    });
}

// shows single email
function load_email(email, mailbox) {
  hide_show("email-view");
  mark_as_read(email);
  const email_view = document.querySelector("#email-view");
  email_view.innerHTML = `<div>
                            Sender: ${email.sender}<br>
                            Recipients: ${email.recipients}<br>
                            Subject: ${email.subject}<br>
                            Time: ${email.timestamp} 
                          </div>`;

  const archiveBtn = create_btn(
    email.archived ? "Unarchive" : "Archive",
    archive_clicked,
    email
  );
  const replyBtn = create_btn("Reply", reply_clicked, email);
  const emailBody = document.createElement("div");
  emailBody.innerHTML = email.body;
  const childElements =
    mailbox === "sent"
      ? [document.createElement("hr"), emailBody]
      : [archiveBtn, replyBtn, document.createElement("hr"), emailBody];
  childElements.forEach((child) => email_view.appendChild(child));
}

// creates a btn
function create_btn(label, onClick, passed) {
  const btn = document.createElement("button");
  btn.classList.add(
    "btn",
    "btn-sm",
    label === "Reply" ? "btn-primary" : "btn-outline-primary",
    "m-2"
  );
  btn.addEventListener("click", (event) => onClick(event, passed));
  btn.innerText = label;
  return btn;
}

// marks a email as read if unread
function mark_as_read(email) {
  const { id, read } = email;
  if (read) return;
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    }),
  });
}

// Ran when archive clicked in email-view
function archive_clicked(event, email) {
  const { id, archived } = email;
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: !archived,
    }),
  }).then((result) => {
    result.error
      ? addMessage(result.error, "alert-danger")
      : (addMessage(
          archived ? "Email Unarchived" : "Email Archived",
          "alert-success"
        ),
        load_mailbox("inbox"));
  });
}

// Ran when reply clicked in email-view
function reply_clicked(event, email) {
  hide_show("compose-view");
  const { body, sender, subject, timestamp } = email;

  document.querySelector("#compose-recipients").value = sender;
  document.querySelector(
    "#compose-body"
  ).value = `On ${timestamp} ${sender} wrote: \n${body}\n`;
  //check if Re: is at start of subject and adds if not
  document.querySelector("#compose-subject").value = /^re:/i.test(subject)
    ? subject
    : `Re: ${subject}`;
}

function hide_show(view) {
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector(`#${view}`).style.display = "block";
}
