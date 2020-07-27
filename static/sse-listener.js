/*
 * Copyright (c) 2020  Ngô Ngọc Đức Huy
 */

function getCookie(name) {
    return document.cookie.split('; ').reduce((r, v) => {
        const parts = v.split('=');
        return parts[0] === name ? decodeURIComponent(parts[1]) : r;
    }, '');
}

const mailbox = document.getElementById("mailbox-body");
const eventSource = new EventSource("/mail/stream");

eventSource.onmessage = function(e) {
    let expiration = getCookie('exp');
    let now = new Date();
    if (now > expiration) {
        eventSource.removeEventListener('message', this);
    }
    const mails  = JSON.parse(e.data);
    mailbox.innerHTML = '';
    for (let mail of mails) {
        const isRead = mail['is_read'];
        const lineNode = document.createElement('tr')
        const fromNode = document.createElement('td');
        const subjectNode = document.createElement('td');
        const dateNode = document.createElement('td');
        let textNode;

        textNode = document.createTextNode(mail.headers.from);
        fromNode.appendChild(textNode);

        textNode = document.createTextNode(mail.headers['subject']);
        subjectNode.appendChild(textNode);
        if (!isRead) {
            const span = document.createElement('span');
            span.className = 'new badge red right';
            span.dataset.badgeCaption = 'unread';
            subjectNode.appendChild(span);
        }

        textNode = document.createTextNode(mail.headers['date']);
        dateNode.appendChild(textNode);

        lineNode.appendChild(fromNode);
        lineNode.appendChild(subjectNode);
        lineNode.appendChild(dateNode);
        lineNode.className = isRead ? 'read' : 'unread orange-text text-darken-4';
        lineNode.className += ' link'
        lineNode.addEventListener('click', function () {
            window.location.href = '/mail/' + mail['id'];
        })

        mailbox.prepend(lineNode);
    }
};