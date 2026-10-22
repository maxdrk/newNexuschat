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
    let footerName = document.getElementById("profileStatusBar")
    footerName.innerHTML = localStorage.getItem('username')
}

function Initprofile() {
    loadProfil()
    loadPseudo()
}

function loadProfil() {
    const username = localStorage.getItem('username')
    document.getElementById("profileUsername").innerHTML = username
     document.getElementById("profileId").innerHTML = username
      document.getElementById("profilePseudo").innerHTML = username
    document.getElementById("profileEmail").innerHTML = localStorage.getItem('userMail')
    document.getElementById("profileEmailDetail").innerHTML = localStorage.getItem('userMail')
    document.getElementById("profileMailVerify").innerHTML = "false"
    document.getElementById("profileSince").innerHTML = "Aucune donnée"
    const mood = localStorage.getItem('userMood') || '...'
    document.getElementById('profileMood').textContent = `"${mood}"`
    setAvatar('profileAvatar', username)
}

function editProfileMood() {
    const currentMood = localStorage.getItem('userMood') || ''
    const newMood = window.prompt('Ton message personnel :', currentMood)

    if (newMood === null) return

    const mood = newMood.trim()
    localStorage.setItem('userMood', mood)
    document.getElementById('profileMood').textContent = `"${mood || '...'}"`
}
