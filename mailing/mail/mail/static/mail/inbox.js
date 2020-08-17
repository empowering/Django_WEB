document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

// 메일 작성하기 
function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector("#each-mail").style.display = "none";

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

// 메일함 확인하기
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector("#each-mail").style.display = "none";

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  let num = 0;
  // Find mailbox from server
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    
    emails
    .forEach(email => {

      sender = '';
      if (mailbox === 'sent') {
        sender = email.recipients;
      }
      else 
      {
        sender = email.sender;
      }
      const subject = email.subject;
      const timestamp = email.timestamp;

      const eachmail = document.createElement('div');
      eachmail.setAttribute("id", `mail_each${num}`);
      eachmail.setAttribute("class", `mail_each`);
      document.querySelector('#emails-view').append(eachmail);

      const sender_div = document.createElement('div');
      sender_div.setAttribute("id", "sender");
      sender_div.innerHTML = sender;
      eachmail.appendChild(sender_div);

      const subject_div = document.createElement('div');
      subject_div.setAttribute("id", "subject");
      subject_div.innerHTML = subject;
      eachmail.appendChild(subject_div);

      const time_stamp = document.createElement('div');
      time_stamp.setAttribute("id", "timestamp");
      time_stamp.innerHTML = timestamp;
      eachmail.appendChild(time_stamp);

      // if mail is read
      if(email.read) {
        eachmail.style.background = 'gray';
      }
      else {
        eachmail.style.background = 'white';
      }

      // if clicked, show mail
      eachmail.addEventListener("click", () => {
        show_mail(email.id, mailbox);
      });

      num = num + 1;

    });
  });
}

// 메일 읽기 
function show_mail(id, mailbox) {
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#each-mail").style.display = "block";

  // 메일 내용 불러오기 
  fetch(`/emails/${id}`)
    .then((response) => response.json())
    .then((email) => {

      const sender = email.sender;
      const subject = email.subject;
      const body = email.body;
      const timestamp = email.timestamp;
  
      let archive = (email.archived)? "Unarchive":"Archive";
      
      content = `
      <div id = mailview>
        <div><b>Sender</b> : ${sender}</div>
        <div><b>Time</b> : ${timestamp}</div>
        <div id><b>Subject</b> : ${subject}</div>
        <hr>
        <div>${body}</div>
        <hr>
        <button id=reply>Reply</button>
        <button id=archive>${archive}</button>
      </div>
      `
      document.querySelector('#each-mail').innerHTML = content;

      // to reply
      document.querySelector('#reply').addEventListener("click", () => {
        reply(sender, subject)
      });

      // to archive
      document.querySelector('#archive').addEventListener("click", () => {
        toggle_archive(id, email.archived);
        if (archive.innerText == "Archive") archive.innerText = "Unarchive";
        else archive.innerText = "Archive";
      });

      // 읽음으로 표시
      is_read(id);
    })

}

function reply(sender, subject) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector("#each-mail").style.display = "none";

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = `${sender}`;
  document.querySelector('#compose-subject').value = `Re:${subject}`;
  document.querySelector('#compose-body').value = '';
}


function toggle_archive(id, state) {
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: !state,
    }),
  });

  // 
  load_mailbox('archive');
}

function is_read(id) {
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    }),
  });
}