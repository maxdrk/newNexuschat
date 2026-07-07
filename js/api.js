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
        }
    }
    xhr.send(JSON.stringify({ id: idUser }))
    loadPseudo()
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

            console.log(result.detail)
            idUser = result.idUser
            localStorage.setItem('idUser', result.idUser)
            message.innerHTML = 'Compte créé avec succès'
            message.classList.add('messageOk')
            setTimeout(() => { Login(form) }, 2000)
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
            let idDestinataire = localStorage.setItem('idDestinataire', result.id)
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
            let idConv = localStorage.setItem('idConv', result.idConv)
            callback(Array.isArray(result) ? result : [result])
        }
    }
    xhr.send(JSON.stringify({ id: idUser }))
}

function createDemande() {
    const xhr = new XMLHttpRequest()
    xhr.open("POST", "http://localhost:8000/users/createDemande")
    xhr.setRequestHeader('content-type', 'application/json')
    xhr.onload = function() {
        if (xhr.status === 200) {
            const result = JSON.parse(xhr.responseText)
            let idDestinataire = localStorage.setItem('idDestinataire', result.id)
            renderSearchResults(Array.isArray(result) ? result : [result])
        }
    }
    xhr.send(JSON.stringify({ idFrom: localStorage.getItem('idUser'), idTo: localStorage.getItem("idDestinaire") }))
}

function updateStatusDemande(idConv, status, callback) {
    const xhr = new XMLHttpRequest()
    xhr.open("POST", "http://localhost:8000/users/updateStatusDemande")
    xhr.setRequestHeader('content-type', 'application/json')
    xhr.onload = function() {
        if (xhr.status === 200 && callback) callback()
    }
    xhr.send(JSON.stringify({ status: status, idConv: idConv }))
}