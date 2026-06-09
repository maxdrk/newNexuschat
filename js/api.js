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

            document.getElementById('username').innerHTML = result.username
            document.getElementById('usermail').innerHTML = result.mail
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
                message.classList.add('messageOk')
                setTimeout(() => { window.location.href = "../pages/dashboard.html" }, 2000);


            } else {
                message.innerHTML = 'Email ou mot de passe incorrects'
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