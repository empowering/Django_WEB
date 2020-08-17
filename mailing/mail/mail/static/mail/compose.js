document.addEventListener("DOMContentLoaded", function () { 
    const form = document.querySelector("#compose-form");
    const msg = document.querySelector("#message");

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const recipients = document.querySelector('#compose-recipients').value;
      const subject = document.querySelector('#compose-subject').value;
      const body = document.querySelector('#compose-body').value;

      // Send an email
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients, // compose-recipients
            subject: subject, // compose-subject
            body: body, // compose-body
            read: false,
            archived: false,
        }),
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result.status);
          
          // favico errorhandling
          if (result.error == undefined) {
            load_mailbox("sent");
          } else {
            msg.innerHTML = `<div class="alert alert-danger" role="alert">
            ${result.error}
          </div>`;
          }
        });
    
      // redirect
      return false;

    });
  });