let ws = null
let currentConvId = null
let currentToUser = null

function openConversation(idContact, usernameContact) {
    const idUser = parseInt(localStorage.getItem('idUser'))
    if (ws) {
        ws.close()
        ws = null
    }

    currentToUser = idContact

    const xhr = new XMLHttpRequest()
    xhr.open('POST', 'http://localhost:8000/conversations/create')
    xhr.setRequestHeader('content-type', 'application/json')
    xhr.onload = function() {
        if (xhr.status === 200) {
            const result = JSON.parse(xhr.responseText)
            currentConvId = result.convId
            loadHistory(currentConvId)
            connectWebSocket(currentConvId, idUser)
            updatePartnerBar(usernameContact)
        }
    }
    xhr.send(JSON.stringify({ idUser1: idUser, idUser2: idContact }))
}

function connectWebSocket(convId, idUser) {
    const pseudo = localStorage.getItem('username')
    ws = new WebSocket(`ws://localhost:8000/conversations/ws/${convId}/${idUser}/${pseudo}`)

    ws.onopen = () => console.log(`WS connecté — conv ${convId}`)

    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data)
        appendMessage(msg)
    }

    ws.onclose = () => console.log('WS déconnecté')
    ws.onerror = (e) => console.error('WS erreur', e)
}

function loadHistory(convId) {
    const xhr = new XMLHttpRequest()
    xhr.open('GET', `http://localhost:8000/conversations/history/${convId}`)
    xhr.onload = function() {
        if (xhr.status === 200) {
            const messages = JSON.parse(xhr.responseText)
            const container = document.getElementById('messages')
            container.innerHTML = ''
            messages.forEach(m => appendMessage(m))
        }
    }
    xhr.send()
}

function sendMessage() {
    const input = document.querySelector('.input-box')
    const contenu = input.value.trim()
    console.log('sendMessage appelé — contenu:', contenu, '| ws:', ws ? ws.readyState : 'null')
    if (!contenu) { console.warn('input vide'); return }
    if (!ws) { console.warn('pas de WebSocket — ouvre une conversation d\'abord'); return }
    if (ws.readyState !== WebSocket.OPEN) { console.warn('WS pas encore ouvert, état:', ws.readyState); return }

    const now = new Date()
    const heure = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`

    ws.send(JSON.stringify({
        contenu: contenu,
        toUser: currentToUser,
        heure: heure
    }))

    input.value = ''
}

function appendMessage(msg) {
    const currentUser = localStorage.getItem('username')
    const isMe = msg.auteur === currentUser
    const container = document.getElementById('messages')

    const div = document.createElement('div')
    div.className = 'msg-row'
    div.innerHTML = `
        <div class="msg-header">
            <span class="msg-author ${isMe ? 'me' : 'them'}">${msg.auteur} :</span>
            <span class="msg-time-inline">(${msg.heure})</span>
        </div>
        <div class="msg-text">${msg.contenu}</div>
    `
    container.appendChild(div)
    container.scrollTop = container.scrollHeight
}

function updatePartnerBar(username) {
    document.getElementById('welcomeScreen').style.display = 'none'
    document.getElementById('messages').style.display = 'flex'
    document.getElementById('partnerBar').style.display = 'flex'
    document.getElementById('partnerName').textContent = username
    document.getElementById('partnerAvatar').innerHTML = `<img src="${getAvatar(username)}" style="width:100%;height:100%;object-fit:cover;" alt="${username}">`
}