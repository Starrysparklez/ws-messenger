async function makeButtonsVisible(id, show) {
    const container = document.getElementById(`message-buttons-container-id-${id}`);
    if (container)
        container.style.display = show ? "flex" : "none";
}
async function channelHover(id, show) {
    const container = document.getElementById(`textchannel-delete-id-${id}`);
    container.style.display = show ? "block" : "none";
}


MicroModal.init();