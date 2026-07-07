function changeStatus() {
    const statusBox = document.getElementById("statusSelect").value
    const statusDiv = document.querySelector(".my-status")

    const dots = {
        "En ligne": "dot-online",
        "Absent(e)": "dot-away",
        "Occupé(e)": "dot-busy",
        "Hors ligne": "dot-off"
    }

    const dotClass = dots[statusBox] || "dot-online"
    statusDiv.innerHTML = `<span class="dot ${dotClass}"></span> ${statusBox}`
}

function loadPseudo() {
    let footerName = document.getElementById("footPseudo")
    footerName.innerHTML = `<span>Connecté en tant que : ${localStorage.getItem('username')} </span>`
}

function Initprofile() {
    loadProfil()
}

function loadProfil() {
    const username = localStorage.getItem('username')
    document.getElementById("profileUsername").innerHTML = username
    document.getElementById("profileEmail").innerHTML = localStorage.getItem('userMail')
    setAvatar('profileAvatar', username)
}