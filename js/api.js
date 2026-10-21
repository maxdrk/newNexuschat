function InitPage() {
    let idUser = parseInt(localStorage.getItem('idUser'))

    const xhr = new XMLHttpRequest()
    xhr.open("POST", `http://localhost:8000/users/getUser/`)
    xhr.setRequestHeader('content-type', 'application/json')

    xhr.onload = function() {
        if (xhr.status === 200) {
            const result = JSON.parse(xhr.responseText)

            localStorage.setItem('username', result.username)
            localStorage.setItem('userMail', result.mail)
            if (result.avatar) localStorage.setItem('avatar', result.avatar)

            document.getElementById('username').innerHTML = result.username
            document.getElementById('usermail').innerHTML = result.mail
            setAvatar('myAvatar', result.username)
            loadPseudo()
        }
    }
    xhr.send(JSON.stringify({ id: idUser }))
    getContacts()
}

function getContacts() {
    const idUser = parseInt(localStorage.getItem('idUser'))
    const xhr = new XMLHttpRequest()
    xhr.open("POST", "http://localhost:8000/users/getContacts")
    xhr.setRequestHeader('content-type', 'application/json')
    xhr.onload = function() {
        if (xhr.status === 200) {
            const result = JSON.parse(xhr.responseText)
            renderContacts(Array.isArray(result) ? result : [])
        }
    }
    xhr.send(JSON.stringify({ id: idUser }))
}

function Login(form) {
    let vmail = form.mail.value
    let vmdp = form.mdp.value

    const xhr = new XMLHttpRequest()
    xhr.open('POST', 'http://localhost:8000/users/login')
    xhr.setRequestHeader('content-type', 'application/json')
    xhr.onload = function() {

        if (xhr.status == 200) {
            const result = JSON.parse(xhr.responseText)
            let message = document.getElementById('message')
            if (result.success === true) {
                console.log(result)
                idUser = result.idUser
                localStorage.setItem('idUser', result.idUser)
                message.innerHTML = 'connexion réussie'
                message.classList.remove('messagePasOk')
                message.classList.add('messageOk')
                setTimeout(() => { window.location.href = "pages/loading.html" }, 2000);


            } else {
                message.innerHTML = 'Email ou mot de passe incorrects'
                message.classList.remove("messageOk")
                message.classList.add("messagePasOk")

            }
        }
    }
    xhr.send(JSON.stringify({ email: vmail, password: vmdp }))

}

function createUser(form) {
    let vusername = form.pseudo.value
    let vmail = form.mail.value
    let vmdp = form.mdp.value

    const xhr = new XMLHttpRequest()
    xhr.open('POST', 'http://localhost:8000/users/createUser')
    xhr.setRequestHeader('content-type', 'application/json')
    xhr.onload = function() {
        if (xhr.status == 200) {
            const result = JSON.parse(xhr.responseText)
            let message = document.getElementById('message')

            idUser = result.idUser
            localStorage.setItem('idUser', result.idUser)
            message.innerHTML = 'Compte créé avec succès'
            message.classList.remove('messagePasOk')
            message.classList.add('messageOk')
            setTimeout(() => { Login(form) }, 2000)
        }
        else {
            const message = document.getElementById('message')
            const result = JSON.parse(xhr.responseText || '{}')
            message.innerHTML = result.detail || 'Impossible de créer le compte'
            message.classList.remove('messageOk')
            message.classList.add('messagePasOk')
        }
    }
    xhr.send(JSON.stringify({ username: vusername, email: vmail, password: vmdp }))
}

function selectUser(query = '') {

    const xhr = new XMLHttpRequest()
    xhr.open("POST", "http://localhost:8000/users/selectUser")
    xhr.setRequestHeader('content-type', 'application/json')
    xhr.onload = function() {
        if (xhr.status === 200) {
            const result = JSON.parse(xhr.responseText)
            renderSearchResults(Array.isArray(result) ? result : [result])
        }
    }
    xhr.send(JSON.stringify({ nom: query }))
}

function getDemandes(callback) {
    const idUser = parseInt(localStorage.getItem('idUser'))
    const xhr = new XMLHttpRequest()
    xhr.open("POST", "http://localhost:8000/users/getDemandes")
    xhr.setRequestHeader('content-type', 'application/json')
    xhr.onload = function() {
        if (xhr.status === 200) {
            const result = JSON.parse(xhr.responseText)
            callback(Array.isArray(result) ? result : [])
        }
    }
    xhr.send(JSON.stringify({ id: idUser }))
}

function createDemande(idTo, button) {
    const xhr = new XMLHttpRequest()
    xhr.open("POST", "http://localhost:8000/users/createDemande")
    xhr.setRequestHeader('content-type', 'application/json')
    xhr.onload = function() {
        if (xhr.status === 200) {
            if (button) {
                button.disabled = true
                button.textContent = 'En attente'
            }
            getDemandes(renderNotifications)
        } else if (button) {
            const result = JSON.parse(xhr.responseText || '{}')
            button.textContent = result.detail || 'Erreur'
        }
    }
    xhr.send(JSON.stringify({ idFrom: Number(localStorage.getItem('idUser')), idTo: Number(idTo) }))
}

function updateStatusDemande(idDemande, status, callback) {
    const xhr = new XMLHttpRequest()
    xhr.open("POST", "http://localhost:8000/users/updateStatusDemande")
    xhr.setRequestHeader('content-type', 'application/json')
    xhr.onload = function() {
        if (xhr.status === 200 && callback) callback()
    }
    xhr.send(JSON.stringify({ status: status, idConv: idDemande }))
}
