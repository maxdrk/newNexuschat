function waitForData() {
    const idUser = parseInt(localStorage.getItem('idUser'))

    if (!idUser && idUser !== 0) {
        window.location.href = '../index.html'
        return
    }

    let progress = 0
    const fill = document.getElementById('progressFill')
    const text = document.getElementById('loadingText')

    const interval = setInterval(() => {
        progress += 15
        fill.style.width = progress + '%'

        if (progress === 45) text.innerHTML = 'Récupération du profil...'
        if (progress === 75) text.innerHTML = 'Chargement des contacts...'

        if (progress >= 100) {
            clearInterval(interval)
            text.innerHTML = 'Prêt !'
            setTimeout(() => {
                window.location.href = '../pages/dashboard.html'
            }, 300)
        }
    }, 400)

    InitPage()
}