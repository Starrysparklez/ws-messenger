var channelList;
var messageList;
var messageField;

/**
 * Parse cookies.
 * @param {string} name Name of the cookie.
 * @returns Cookie value if exists, else null.
 */
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

const token = parseCookie("mysupersecrettoken");
const socket = io("ws:///", { auth: { token: token } });
const newMessageSoundEffect = new Audio("/static/chatrooms/new_message.mp3")
var currentChannelId;

/**
 * Place a new channel to the web page using JSON data.
 * @param {*} channelId Current channel id
 * @param {*} newChannelData New channel data in JSON
 */
async function renderChannel(channelId, newChannelData) {
    const channelDeletion = document.createElement("i");
    channelDeletion.classList = "fas fa-trash-alt to-right channel-del";
    channelDeletion.id = `textchannel-delete-id-${newChannelData.id}`;

    const channelDeletionOuter = document.createElement("span");
    channelDeletionOuter.className = "channel-deletion";
    channelDeletionOuter.setAttribute("aria-label", "Delete");
    channelDeletionOuter.setAttribute("data-microtip-position", "left");
    channelDeletionOuter.setAttribute("role", "tooltip");
    channelDeletionOuter.appendChild(channelDeletion);

    const channelName = document.createElement("span");
    channelName.id = `textchannel-name-id-${newChannelData.id}`;
    channelName.textContent = newChannelData.name;

    const hashIcon = document.createElement("i");
    hashIcon.classList = "fas fa-hashtag";

    const mainDiv = document.createElement("div");
    mainDiv.id = `textchannel-id-${newChannelData.id}`;
    if (newChannelData.id == channelId) mainDiv.classList = "textchannel selected";
    else mainDiv.className = "textchannel";
    mainDiv.onmouseenter = () => channelHover(newChannelData.id, true);
    mainDiv.onmouseleave = () => channelHover(newChannelData.id, false);
    mainDiv.onclick = () => changeChannel(newChannelData.id);

    mainDiv.appendChild(hashIcon);
    mainDiv.appendChild(channelName);
    mainDiv.appendChild(channelDeletionOuter);
    channelList.appendChild(mainDiv);
}
/**
 * Retrieve a list of channels from the API.
 * @param {*} channelId Current channel id
 */
async function retrieveChannels(channelId) {
    fetch(`/api/channels`, {
        headers: { "Authorization": token }
    }).then(d => d.json()).then(data => {
        data.channels_data.forEach(c => renderChannel(channelId, c));
    });
}
/**
 * Place a new message to the web page using JSON data.
 * @param {*} messageData New message data in JSON
 * @param {*} currentUser Current user information in JSON
 */
async function renderMessage(messageData, currentUser) {
    var buttons;

    if (messageData.author.id == currentUser.id) {
        const buttonEditIcon = document.createElement("i");
        buttonEditIcon.classList = "fas fa-edit";

        const buttonEdit = document.createElement("div");
        buttonEdit.className = "button";
        buttonEdit.id = `message-edit-button-id-${messageData.id}`;
        buttonEdit.setAttribute("aria-label", "Edit message");
        buttonEdit.setAttribute("data-microtip-position", "top-left");
        buttonEdit.setAttribute("role", "tooltip");

        const buttonDeleteIcon = document.createElement("i");
        buttonDeleteIcon.classList = "fas fa-trash-alt";

        const buttonDelete = document.createElement("div");
        buttonDelete.className = "button";
        buttonDelete.id = `message-delete-button-id-${messageData.id}`;
        buttonDelete.setAttribute("aria-label", "Delete message");
        buttonDelete.setAttribute("data-microtip-position", "top");
        buttonDelete.setAttribute("role", "tooltip");

        buttons = document.createElement("div");
        buttons.className = "buttons";
        buttons.id = `message-buttons-container-id-${messageData.id}`;

        buttonDelete.appendChild(buttonDeleteIcon);
        buttons.appendChild(buttonDelete);
        buttonEdit.appendChild(buttonEditIcon);
        buttons.appendChild(buttonEdit);
    }

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.style.backgroundImage = `url(${messageData.author.avatar_url})`;
    console.log(messageData.author);

    const userName = document.createElement("span");
    userName.className = "username";
    userName.id = `message-username-id-${messageData.id}`;
    userName.textContent = messageData.author.username;

    const br = document.createElement("br");

    const content = document.createElement("span");
    content.className = "message-content";
    content.id = `message-content-id-${messageData.id}`;
    content.textContent = messageData.content;

    const mainPart = document.createElement("div");
    mainPart.className = "main-part";

    mainPart.appendChild(userName);
    mainPart.appendChild(br);
    mainPart.appendChild(content);

    const mainDiv = document.createElement("div");
    mainDiv.className = "message";
    mainDiv.id = `message-container-id-${messageData.id}`;
    mainDiv.onmouseenter = () => makeButtonsVisible(messageData.id, true);
    mainDiv.onmouseleave = () => makeButtonsVisible(messageData.id, false);

    if (messageData.author.id == currentUser.id) mainDiv.appendChild(buttons);
    mainDiv.appendChild(avatar);
    mainDiv.appendChild(mainPart);

    messageList.appendChild(mainDiv);
}
/**
 * Retrieve all messages for current channel from the API.
 * @param {*} channelId Current channel id
 */
async function retrieveMessages(channelId, currentUser) {
    fetch(`/api/messages/${channelId}`, {
        headers: { "Authorization": token }
    }).then(d => d.json()).then(data => {
        data.messages_data.forEach(m => renderMessage(m, currentUser));
    });
    messageList.scrollTop = messageList.scrollHeight;
}
/**
 * Send message from the textarea to the API.
 */
async function sendMessage() {
    fetch(`/api/message`, {
        method: "PUT",
        headers: { "Content-Type": "application/json", "Authorization": token },
        body: JSON.stringify({ "content": messageField.value, "channel_id": currentChannel.id })
    }).then(r => r.status == 200 ? null : alert("Error"));
}

const retrieveUser = () => new Promise(res => {
    fetch(`/api/user`, {
        method: "GET",
        headers: { "Authorization": token }
    }).then(r => r.json()).then(d => res(d)).catch(() => res(null));
});

/**
 * Change current channel, connect to another room, receive messages and update channel and member list.
 * @param {*} newChannelId New channel id
 */
async function changeChannel(newChannelId) {
    window.history.pushState("", "", window.location.href.replace(/\/[^\/]*$/, `/${newChannelId}`));
    messageList.innerText = "";
    channelList.innerText = "";
    messageField.textContent = "";

    const currentUser = await retrieveUser();
    if (!currentUser) {
        alert("Cannot retrieve current user.");
        return;
    }

    await retrieveMessages(newChannelId, currentUser);
    await retrieveChannels(newChannelId);

    // leave previous channel to avoid getting useless events
    if (currentChannelId) socket.emit("leave", {
        "token": token,
        "channelId": currentChannelId
    });

    // lets connect to the new channel
    socket.emit("join", {
        "token": token,
        "channelId": newChannelId
    });
    // if there's an error then alert it to the user
    socket.on("connect_error", () => {
        alert("Unable to connect to websocket.");
    });
    socket.on("channel_create", newChannel => {
        renderChannel(channelId, newChannel);
    });
    socket.on("channel_delete", deletedChannel => {
        document.getElementById(`textchannel-id-${deletedChannel.id}`).remove();
    });
    socket.on("channel_update", updatedChannel => {
        const channel = document.getElementById(`textchannel-name-id-${updatedChannel.old_channel.id}`);
        channel.textContent = updatedChannel.new_channel.name;
    });
    socket.on("message_create", newMessage => {
        newMessageSoundEffect.play();
        renderMessage(newMessage, currentUser);
        messageList.scrollTop = messageList.scrollHeight;
    });
    socket.on("message_delete", deletedMessage => {
        document.getElementById(`message-container-id-${deletedMessage.id}`).remove();
    });
    socket.on("message_update", updatedMessage => {
        const msg = document.getElementById(`message-content-id-${updatedMessage.before.id}`);
        msg.textContent = updatedMessage.after.content;
    });
}

/**
 * Called when you move cursor on the message.
 * @param {*} id Message id
 * @param {boolean} show Show buttons (true) or hide (false)
 */
async function makeButtonsVisible(id, show) {
    const container = document.getElementById(`message-buttons-container-id-${id}`);
    if (container)
        container.style.display = show ? "flex" : "none";
}
/**
 * Same as the makeButtonsVisible for messages, but for channels.
 * @param {*} id Channel id
 * @param {*} show Show buttons (true) or hide (false)
 */
async function channelHover(id, show) {
    const container = document.getElementById(`textchannel-delete-id-${id}`);
    container.style.display = show ? "block" : "none";
}

/**
 * Main function, called when event DOMContentLoaded triggered.
 */
async function main() {
    channelList = document.getElementById("place-channels-there");
    messageList = document.getElementById("place-messages-there");
    messageField = document.getElementById("message-area");

    MicroModal.init();
    document.getElementById("overlay").style.display = "none";

    document.getElementById("create-channel-button").onclick = () => {
        MicroModal.show("modal-channel-creation");
    };
    document.getElementById("username").onclick = () => {
        MicroModal.show("modal-user-edit");
    };

    const splittedURL = window.location.href.split("/");
    changeChannel(splittedURL[splittedURL.length - 1]);
}

/**
 * Execute 'main' function when the DOMContentLoaded event triggered.
 */
window.addEventListener("DOMContentLoaded", () => main());
