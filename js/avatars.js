function getAvatar(seed) {
    let link = `https://api.dicebear.com/9.x/thumbs/svg?seed=${encodeURIComponent(seed)}`
    return link
}

function setAvatar(elementId, seed) {
    const el = document.getElementById(elementId)
    if (!el) return

    const cached = localStorage.getItem('avatar')
    if (cached) {
        console.log(cached)
        el.innerHTML = `<img src="${cached}" style="width:100%;height:100%;object-fit:cover;" alt="${seed}">`
        return
    }

    fetch(getAvatar(seed))
        .then(r => r.blob())
        .then(blob => {
            const reader = new FileReader()
            reader.onloadend = () => {
                const base64 = reader.result
                localStorage.setItem('avatar', base64)
                el.innerHTML = `<img src="${base64}" style="width:100%;height:100%;object-fit:cover;" alt="${seed}">`
                saveAvatarToDB(base64)
            }
            reader.readAsDataURL(blob)
        })
}

function saveAvatarToDB(base64) {
    const idUser = parseInt(localStorage.getItem('idUser'))
    if (!idUser) return
    console.log(localStorage.getItem('avatar'))
    const xhr = new XMLHttpRequest()
    xhr.open('POST', 'http://localhost:8000/avatar/setAvatar')
    xhr.setRequestHeader('content-type', 'application/json')
    xhr.send(JSON.stringify({ idUser: idUser, avatar: base64 }))
}

function getAvatarUrl(seed) {
    return getAvatar(seed)
}