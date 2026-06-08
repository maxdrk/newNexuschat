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
            if (result === true) {
                message.innerHTML = 'connexion réussie'
                message.classList.add('messageOk')
                setTimeout(2)
                window.location.href = "../pages/dashboard.html"

            } else {
                message.innerHTML = 'Email ou mot de passe incorrects'
                message.classList.add("messagePasOk")

            }
        }
    }
    xhr.send(JSON.stringify({ email: vmail, password: vmdp }))

}

function getUserInfo() {}