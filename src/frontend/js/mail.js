const content = document.querySelector('.content');
const sidebar = document.querySelector('.sidebar');
const showSideBar = document.querySelector('.showSideBar');

let email_datas = [];
let suggested_event = null;

async function getMails() {
    const mails = await _fetch('/api/getmails');
    if (!mails) {
        return;
    }

    email_datas = mails.mails;

    populateEmailList(email_datas);
}

async function suggestReply(id) {
    const mail = email_datas.find(email => email.id == id);

    console.log("Generating reply...");

    document.getElementById('reply-popup').style.display = 'block';

    const reply = await _fetch('/api/suggestmailreply', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            from_name: mail.from.name,
            body: mail.body,
            subject: mail.subject
        })
    }, 2);

    console.log(reply);

    if (!reply) {
        document.getElementById('reply-popup-text').innerHTML = 'No reply found';
        return;
    }

    document.getElementById('reply-popup-text').innerHTML = `<input type="text" id="reply-subject" placeholder="Subject"><textarea id="reply-content">${reply.reply}</textarea><button class="btn popup-close reply" style="display: block" onclick="addReply('${mail.from.email}')">Send</button>`;
}

async function suggestEvent(id) {
    const mail = email_datas.find(email => email.id == id);

    console.log("Generating event...");

    document.getElementById('suggestion-popup').style.display = 'block';

    const _event = await _fetch('/api/suggestevent', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            subject: mail.subject,
            body: mail.body
        })
    });

    console.log(_event);

    if (!_event || !_event.success) {
        document.getElementById('suggestion-popup-text').innerHTML = 'No events found';
        return;
    }

    const event = _event.suggested_event;

    if (event.shouldAdd) {
        suggested_event = event;

        document.getElementById('suggestion-popup-text').innerHTML = `
            <p>Title: ${event.title}</p>
            <p>Start: ${timestampToHumanReadable(event.startDate)}</p>
            <p>Stop: ${timestampToHumanReadable(event.endDate)}</p>`;

        document.getElementById('add-suggestion').style.display = 'block';
    } else {
        document.getElementById('suggestion-popup-text').innerHTML = 'No events found';
    }
}

function translateEmail(id) {
    document.getElementById('translate-popup').style.display = 'block';
    document.getElementById('translate-popup').querySelector('.popup-close').addEventListener('click', async () => {
        await _translateEmail(id, document.getElementById('translate-select').dataset.value);
        document.getElementById('translate-popup').style.display = 'none';
    })
}

async function _translateEmail(id, language) {
    const mail = email_datas.find(email => email.id == id);

    const res = await _fetch('/api/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            text: mail.body,
            language: language
        })
    });

    if (!res) {
        return;
    }

    const translation = res.translation;

    document.getElementById("current-email-body").innerHTML = translation;
}

// Function to populate the email list
function populateEmailList(emailsToShow) {
    const emailList = document.getElementById('email-list');
    emailList.innerHTML = ''; // Clear the list before populating
    emailsToShow.forEach(email => {
        const li = document.createElement('li');
        li.dataset.id = email.id;
        li.innerHTML = `
            <strong>${email.from.name}</strong><br>
            <span>${email.subject} - ${email.snippet}</span><br>
            <span class="label">#${truncateString(email.folders[0], 15)}</span>
        `;
        if (email.unread) {
            li.innerHTML = `
                <strong>${email.from.name}</strong><span class="unread"></span><br>
                <span>${email.subject} - ${email.snippet}</span><br>
                <span class="label">#${email.folders[0]}</span>
            `;
        }

        li.addEventListener('click', () => showEmailContent(email.id));
        emailList.appendChild(li);
        addAllTooltips();
    });
}

function truncateString(str, maxLength) {
    if (str.length > maxLength) {
        return str.slice(0, maxLength - 3) + '...';
    } else {
        return str;
    }
}

function showEmailContent(id) {
    // If phone view
    if (window.innerWidth < 768) {
        content.style.display = 'flex';
        sidebar.style.display = 'none';
        showSideBar.style.display = 'flex';
    }
    const email = email_datas.find(email => email.id == id);
    const emailContent = document.getElementById('email-content');
    emailContent.innerHTML = `
        <div class="showSideBar" onclick="makeResponsive()">←</div>
        <div class="icons-container">
            <img src="img/messages.png" id="messages-icon" alt="Our logo2" class="logo" width="30px" height="30px" data-tooltip="${email.subject}">
            <img src="img/ai.png" alt="Our logo3" class="logo" width="30px" height="30px" id="ai-icon">
            <img src="img/newfolder.png" alt="Our logo" id="folder-icon" class="logo" width="30px" height="30px">
            <p id="folder-name" style="opacity:0">${email.folders}</p>
        </div>
        <h2>${email.subject}</h2>
        <p class="from">From: ${email.from.name} (${email.from.email})</p>
        <p class="from">To: Me</p>
        <hr>
        <div id="current-email-body">${email.body}</div>
        <hr>
        <button class="btn" onclick="suggestReply('${email.id}')" id="ai-btn">✨ Suggest Reply</button>
        <button class="btn" onclick="suggestEvent('${email.id}')">✨ Suggest Event</button>
        <button class="btn" onclick="translateEmail('${email.id}')">✨ Translate</button>
        <button class="btn" onclick="summarize('${email.id}')">✨ Summarize</button>
    `;

    // Highlight the selected email in the sidebar
    document.querySelectorAll('.sidebar li').forEach(li => li.classList.remove('active'));
    document.querySelector(`.sidebar li[data-id="${id}"]`).classList.add('active');

    showFoldersOnClick();

    scrollToAiBtn();

    // Ajouter le tooltip à l'image avec l'ID messages-icon
    addTooltipToMessageIcon();
}

function scrollToAiBtn() {
    document.getElementById('ai-icon').addEventListener('click', function() {
        const aiBtn = document.getElementById('ai-btn');
        if (aiBtn) {
            aiBtn.scrollIntoView({ behavior: 'smooth' });
        }
    })
}

function showFoldersOnClick() {
    const folderIcon = document.getElementById('folder-icon');
    if (folderIcon) {
        folderIcon.addEventListener('click', function() {
            const folderName = document.getElementById('folder-name');
            if (folderName.style.opacity === '0') {
                folderName.style.opacity = '1';
            } else {
                folderName.style.opacity = '0';
            }
        });
    }
}

// Fonction pour ajouter un tooltip à l'élément avec l'ID messages-icon
function addTooltipToMessageIcon() {
    // Créer dynamiquement l'élément tooltip
    const tooltip = document.createElement('span');
    tooltip.id = 'tooltip';
    tooltip.className = 'tooltip';
    document.body.appendChild(tooltip);

    const messageIcon = document.getElementById('messages-icon');
    if (messageIcon) {
        messageIcon.addEventListener('mousemove', function(e) {
            tooltip.style.left = `${e.pageX +1}px`;
            tooltip.style.top = `${e.pageY -28}px`;
            tooltip.textContent = this.getAttribute('data-tooltip') || "Message Icon"; // Exemple de texte par défaut
            tooltip.classList.add('show');
        });

        messageIcon.addEventListener('mouseleave', function() {
            tooltip.classList.remove('show');
        });
    }
}

document.getElementById('search-bar').addEventListener('input', function() {
    const query = this.value.toLowerCase();
    const filteredEmails = email_datas.filter(email => 
        email.snippet.toLowerCase().includes(query) ||
        email.subject.toLowerCase().includes(query)
    );
    populateEmailList(filteredEmails);
});

function makeResponsive() {
    sidebar.style.display = 'block';
    sidebar.style.width = '100%';
    content.style.display = 'none';
}

function closePopup() {
    document.getElementById('suggestion-popup').style.display = 'none';
    document.getElementById('suggestion-popup-text').innerHTML = '<span class="loading"></span>';
    document.getElementById('add-suggestion').style.display = 'none';

    document.getElementById('reply-popup').style.display = 'none';
    document.getElementById('reply-popup-text').innerHTML = '<span class="loading"></span>';

    document.getElementById('summarize-popup').style.display = 'none';
    document.getElementById('summarize-popup-text').innerHTML = '<span class="loading"></span>';
}

function timestampToHumanReadable(timestamp) {
    const currentDate = new Date();
    const date = new Date(timestamp * 1000);

    const hours = `${date.getHours()}`.padStart(2, '0');
    const minutes = `${date.getMinutes()}`.padStart(2, "0");

    if (currentDate.getDate() === date.getDate() && currentDate.getMonth() === date.getMonth() && currentDate.getFullYear() === date.getFullYear()) {
        return `Today at ${hours}:${minutes}`;
    }

    if (currentDate.getDate() + 1 === date.getDate() && currentDate.getMonth() === date.getMonth() && currentDate.getFullYear() === date.getFullYear()) {
        return `Tomorrow at ${hours}:${minutes}`;
    }

    const year = date.getFullYear();
    const month = `${date.getMonth() + 1}`.padStart(2, '0');
    const day = `${date.getDate()}`.padStart(2, '0');

    return `${year}-${day}-${month} at ${hours}:${minutes}`;
}

async function addSuggestion() {
    if (!suggested_event) {
        return;
    }

    const res = await _fetch('/api/createevent', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: suggested_event.title,
            start_time: suggested_event.startDate,
            end_time: suggested_event.endDate
        })
    });

    if (res && res.success) {
        suggested_event = null;
        closePopup();
    }
}

async function addReply(email) {
    const subject = document.getElementById('reply-subject').value;
    const body = document.getElementById('reply-content').innerHTML;

    if (!subject) {
        alert('Please enter a email subject');
        return;
    }

    if (!body) {
        alert('Please enter a email body');
        return;
    }

    const res = await _fetch('/api/sendmail', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            body: body,
            subject: subject
        })
    });

    if (res && res.success) {
        closePopup();
    }

    console.log(res);
}

async function enhanceEmail(txt) {
    const res = await _fetch('/api/enhance', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            text: txt
        })
    });

    if (res && res.success) {
        document.getElementById('enhance-popup').style.display = 'flex';
        document.getElementById('enhance-popup-text').textContent = res.enhanced;
        document.getElementById('enhance-send').addEventListener('click', async () => {
            const send = _fetch('/api/sendmail', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: document.getElementById('to').value,
                    body: document.getElementById('enhance-popup-text').textContent,
                    subject: "Hello"
                })
            });
        })
    }

    console.log(res);
}

function closePopup2() {
    document.getElementById('enhance-popup').style.display = 'none';
    document.getElementById('enhance-popup-text').innerHTML = '<span class="loading">Enhancing your email...</span>';
}

async function summarize(id) {
    const email = email_datas.find(email => email.id == id);

    document.getElementById('summarize-popup').style.display = 'block';

    const res = await _fetch('/api/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            text: email.body
        })
    });

    if (res && res.success) {
        document.getElementById('summarize-popup-text').innerHTML = res.summary;
    }
}

getMails();

