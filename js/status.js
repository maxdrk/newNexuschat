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