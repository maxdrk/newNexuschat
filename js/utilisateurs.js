let searchTimeout = null

function LoadContact() {
    selectUser()
}

function renderContacts(contacts) {
    const container = document.getElementById('contactList')
    if (!container) return

    if (!contacts || contacts.length === 0) {
        container.innerHTML = `
            <div class="group-title">Contacts (0)</div>
            <div class="contact-item" style="font-size:11px;color:#888;padding:8px;">Aucun contact</div>
        `
        return
    }

    const items = contacts.map(c => {
        return `
            <div class="contact-item" onclick="openConversation(${c.idContact}, '${c.contact}')" style="cursor:pointer;">
                <span class="dot dot-off"></span>
                <div class="c-avatar" style="overflow:hidden;"><img src="${getAvatar(c.contact)}" style="width:100%;height:100%;object-fit:cover;" alt="${c.contact}"></div>
                <div class="c-info">
                    <div class="c-name">${c.contact}</div>
                    <div class="c-msg">Hors ligne</div>
                </div>
            </div>
        `
    }).join('')

    container.innerHTML = `
        <div class="group-title">
            <i class="ti ti-chevron-down" style="font-size:12px;"></i> Contacts (${contacts.length})
        </div>
        ${items}
    `
}

function searchDebounce(query) {
    clearTimeout(searchTimeout)
    if (query.trim() === '') {
        document.getElementById('searchResults').innerHTML = ''
        return
    }
    searchTimeout = setTimeout(() => selectUser(query), 400)
}

function loadForm() {
    const panel = document.getElementById('selectUser')
    if (panel.style.display === 'block') {
        panel.style.display = 'none'
        panel.innerHTML = ''
        return
    }
    panel.innerHTML = `
        <div class="search-contact-panel">
            <div class="search-contact-title">
                <i class="ti ti-user-search"></i> Rechercher un utilisateur
                <span class="search-close" onclick="loadForm()">✕</span>
            </div>
            <div class="search-contact-body">
                <input
                    class="input-win98"
                    type="text"
                    id="searchInput"
                    placeholder="Pseudo..."
                    oninput="searchDebounce(this.value)"
                />
                <div id="searchResults" class="search-results"></div>
            </div>
        </div>
    `
    panel.style.display = 'block'
    document.getElementById('searchInput').focus()
}

function renderSearchResults(users) {
    const container = document.getElementById('searchResults')
    if (!container) return

    if (!users || users.length === 0 || users[0] === false || users[0] === null) {
        container.innerHTML = '<div class="search-empty">Aucun utilisateur trouvé</div>'
        return
    }

    const currentUser = localStorage.getItem('username')

    container.innerHTML = users
        .filter(u => u.pseudo !== currentUser)
        .map(u => `
            <div class="search-result-row">
                <div class="c-avatar" style="overflow:hidden;"><img src="${getAvatar(u.pseudo)}" style="width:100%;height:100%;object-fit:cover;" alt="${u.pseudo}"></div>
                <span class="search-result-name">${u.pseudo}</span>
                <button class="btn-win98 btn-add" onclick="addContact(${u.id}, '${u.pseudo}')">
                    <i class="ti ti-user-plus"></i> Ajouter
                </button>
            </div>
        `).join('')
}

function addContact(idUser, username) {
    console.log(`Ajout du contact : ${username} (id: ${idUser})`)
        // à brancher sur l'API quand la route sera prête
}

function loadNotifications() {
    const panel = document.getElementById('notifications')
    if (panel.style.display === 'block') {
        panel.style.display = 'none'
        panel.innerHTML = ''
        return
    }

    panel.innerHTML = `
        <div class="search-contact-panel">
            <div class="search-contact-title">
                <i class="ti ti-bell"></i> Notifications
                <span class="search-close" onclick="loadNotifications()">✕</span>
            </div>
            <div id="notifList" class="search-results">
                <div class="search-empty">Chargement...</div>
            </div>
        </div>
    `
    panel.style.display = 'block'

    getDemandes(renderNotifications)
}

function renderNotifications(demandes) {
    const container = document.getElementById('notifList')
    if (!container) return

    if (!demandes || demandes.length === 0 || demandes[0] === false || demandes[0] === null) {
        container.innerHTML = '<div class="search-empty">Aucune notification</div>'
        return
    }

    const currentUser = localStorage.getItem('username')

    container.innerHTML = demandes.map(d => {
                const isReceived = d.destinataire === currentUser
                return `
            <div class="notif-row">
                <div class="notif-text">
                    ${isReceived
                        ? `<b>${d.expediteur}</b> souhaite vous ajouter`
                        : `Demande envoyée à <b>${d.destinataire}</b>`}
                </div>
                ${isReceived ? `
                <div class="notif-actions">
                    <button class="btn-win98" onclick="acceptDemande(${d.idDemande})">✓</button>
                    <button class="btn-win98 btn-danger" onclick="refuserDemande(${d.idDemande})">✕</button>
                </div>` : `<span class="notif-pending">En attente</span>`}
            </div>
        `
    }).join('')
}

function acceptDemande(idDemande) {
    updateStatusDemande(idDemande, 'accepted', () => {
        getDemandes(renderNotifications)
    })
}

function refuserDemande(idDemande) {
    updateStatusDemande(idDemande, 'refused', () => {
        getDemandes(renderNotifications)
    })
}