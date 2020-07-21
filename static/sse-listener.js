const mailbox = document.getElementById("mailbox-body");
const eventSource = new EventSource("/mail/stream");

eventSource.onmessage = function(e) {
    const mails  = JSON.parse(e.data);
    if (mails.length === 0) {
        return
    }
    for (let mail of mails) {
        console.log(mail)
        const isRead = mail['is_read'];
        const lineNode = document.createElement('tr')
        const fromNode = document.createElement('td');
        const subjectNode = document.createElement('td');
        const dateNode = document.createElement('td');
        let textNode;

        textNode = document.createTextNode(mail.headers.from);
        fromNode.appendChild(textNode);

        textNode = document.createTextNode(mail.headers.from);
        subjectNode.appendChild(textNode);
        if (!isRead) {
            const span = document.createElement('span');
            span.className = 'new badge red right';
            span.dataset.badgeCaption = 'unread';
            subjectNode.appendChild(span);
        }

        textNode = document.createTextNode(mail.headers.from);
        dateNode.appendChild(textNode);

        lineNode.appendChild(fromNode);
        lineNode.appendChild(subjectNode);
        lineNode.appendChild(dateNode);
        lineNode.className = isRead ? 'read' : 'unread orange-text text-darken-4';

        mailbox.prepend(lineNode);
    }
};