const placeMessagesThere = document.getElementById("messages-field");
const placeChannelsThere = document.getElementById("channel-list");
const messageField = document.getElementById("textarea");

var currentChannel;

const token = parseCookie("mysupersecrettoken");
const newMessageSoundEffect = new Audio("/static/chatrooms/new_message.mp3")

function parseCookie(name) {
    var nameEqualsTo = `${name}=`;
    var cs = document.cookie.split(';');
    for(var i=0; i < cs.length; i++) {
        var c = cs[i];
        while (c.charAt(0) == " ") c = c.substring(1, c.length);
        if (c.indexOf(nameEqualsTo) == 0)
            return c.substring(nameEqualsTo.length, c.length);
    }
    return null;
}

async function initialize(channelId) {
    await retrieveChannels(channelId, token);
    await retrieveMessages(channelId, token);

    const socket = io("ws:///", { auth: { token: token } });
    socket.emit("join", {
        "token": token,
        "channelId": channelId
    });

    socket.on("connect_error", () => {
        alert("Unable to connect to websocket.");
    });
    socket.on("channel_create", newChannel => {
        renderChannel(channelId, newChannel);
    });
    socket.on("channel_delete", deletedChannel => {
        document.getElementById(`channel-id-${deletedChannel.id}`).remove();
    });
    socket.on("channel_update", updatedChannel => {
        const channel = document.getElementById(`channel-id-${deletedChannel.id}`);
        channel.textContent = updatedChannel.name;
        divChannel.onclick = () => switchChannel(updatedChannel.id);
    });
    socket.on("message_create", newMessage => {
        newMessageSoundEffect.play();
        renderMessage(newMessage);
        placeMessagesThere.scrollTop = placeMessagesThere.scrollHeight;
    });
    socket.on("message_delete", deletedMessage => {
        console.log("Message deleted: " + deletedMessage);
    });
}

async function switchChannel(channelId) {
    window.history.pushState("", "", window.location.href.replace(/\/[^\/]*$/, `/${channelId}`));
    placeMessagesThere.innerText = "";
    placeChannelsThere.innerText = "";
    messageField.textContent = "";
    initialize(channelId);
}

async function createChannel() {
    var channelName = window.prompt("Channel name:", "new-channel");
    if (!channelName) return;

    var channelTitle = window.prompt("Channel description:", "");
    if (!channelTitle) return;

    fetch(`/api/channel`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": parseCookie("mysupersecrettoken")
        },
        body: JSON.stringify({
            "name": channelName.replace(" ", "-"),
            "title": channelTitle
        })
    }).then(r => r.status == 200 ? alert(`Channel ${channelName} created`) : alert("Error"));
}

async function sendMessage() {
    fetch(`/api/message`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": parseCookie("mysupersecrettoken")
        },
        body: JSON.stringify({
            "content": messageField.value,
            "channel_id": currentChannel.id
        })
    }).then(r => r.status == 200 ? null : alert("Error"));
}

async function renderMessage(messageData) {
    const pContent = document.createElement("p");
    pContent.className = "message-content";
    pContent.textContent = messageData.content;

    const separator = document.createElement("div");
    separator.className = "sep";

    const pNickname = document.createElement("p");
    console.log(messageData);
    //pNickname.textContent = `User ID: ${messageData.author_id}\t\tMessage ID: ${messageData.id}`;
    pNickname.textContent = `${messageData.author.username}   |   Message ID: ${messageData.id}`;

    const divNickname = document.createElement("div");
    divNickname.className = "nickname";
    divNickname.appendChild(pNickname);
    divNickname.appendChild(separator);

    const divMessageInner = document.createElement("div");
    divMessageInner.className = "inner";
    divMessageInner.appendChild(divNickname);
    divMessageInner.appendChild(pContent);

    const divMessage = document.createElement("div");
    divMessage.className = "message";
    divMessage.appendChild(divMessageInner);

    placeMessagesThere.appendChild(divMessage);
}

async function renderChannel(channelId, channel) {
    const divChannel = document.createElement("div");
    if (channelId == channel.id) {
        divChannel.classList = "channel-entry selected";
        currentChannel = channel;
        document.getElementById("channel-name").textContent = `Канал #${channel.name}`;
    } else {
        divChannel.className = "channel-entry";
    }
    divChannel.textContent = channel.name;
    divChannel.onclick = () => switchChannel(channel.id);
    divChannel.id = `channel-id-${channel.id}`;

    placeChannelsThere.appendChild(divChannel);
}

async function retrieveChannels(channelId, token) {
    fetch(`/api/channels`, {
        headers: {
            "Authorization": token
        }
    }).then(d => d.json()).then(data => {
        data.channels_data.forEach(c => renderChannel(channelId, c));
    });
}

async function retrieveMessages(channelId, token) {
    fetch(`/api/messages/${channelId}`, {
        headers: { "Authorization": token }
    }).then(d => d.json()).then(data => {
        data.messages_data.forEach(m => renderMessage(m));
        placeMessagesThere.scrollTop = placeMessagesThere.scrollHeight;
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const splittedURL = window.location.href.split("/");
    initialize(splittedURL[splittedURL.length - 1]);
});