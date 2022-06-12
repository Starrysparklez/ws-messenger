# Registration with API
```
POST | /api/register
```

### Example request:
```json
fetch("/api/register", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "username": "Starrysparklez",
        "password": "youshallnotpass"
    })
})
```

### Success response:
```json
{
    "user": {
        "avatar_url": "http://127.0.0.1/static/usercontent/avatar_6941753682170126336.jpg",
        "created_at": "1655043049.376583",
        "id": "6941753682170126336",
        "locale": null,
        "username": "Starrysparklez"
    },
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjY5NDE3NTM2ODIxNzAxMjYzMzYsInBocyI6InBia2RmMjpzaGEyNTY6MjYwMDAwJEFneFNWYklmTVM1cm9wZW4kYmQ0NzlhMWY0Yjg5NDBjYjlhMWQ4YTdhZTA1MzFmZjA3YzQ2MWUyM2M4OGE5ZTY0NWZiMDY5NzZhZmUxMGJmZSJ9.i97TrUgtimUn3M0zIBiV9tPPV4D34-5ZmcmoytzVpg0"
}
```

### Error response (user with this username is exist):
```json
{
    "error": "User is already registered. Try to log in."
}
```

# Log In with API
```
POST | /api/login
```

### Example request:
```json
fetch("/api/login", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "username": "Starrysparklez",
        "password": "youshallnotpass"
    })
})
```

### Success response:
```json
{
    "user": {
        "avatar_url": "http://127.0.0.1/static/usercontent/avatar_6941753682170126336.jpg",
        "created_at": "1655043049.376583",
        "id": "6941753682170126336",
        "locale": null,
        "username": "Starrysparklez"
    },
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjY5NDE3NTM2ODIxNzAxMjYzMzYsInBocyI6InBia2RmMjpzaGEyNTY6MjYwMDAwJEFneFNWYklmTVM1cm9wZW4kYmQ0NzlhMWY0Yjg5NDBjYjlhMWQ4YTdhZTA1MzFmZjA3YzQ2MWUyM2M4OGE5ZTY0NWZiMDY5NzZhZmUxMGJmZSJ9.i97TrUgtimUn3M0zIBiV9tPPV4D34-5ZmcmoytzVpg0"
}
```

### Error response (incorrect password or unknown username):
```json
{
    "error": "Incorrect credentials"
}
```

# Update user with API
```
POST | /api/update_user
```

### Example request:
```json
fetch("/api/update_user", {
    method: "POST",
    headers: {
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjY5NDE3NTM2ODIxNzAxMjYzMzYsInBocyI6InBia2RmMjpzaGEyNTY6MjYwMDAwJEFneFNWYklmTVM1cm9wZW4kYmQ0NzlhMWY0Yjg5NDBjYjlhMWQ4YTdhZTA1MzFmZjA3YzQ2MWUyM2M4OGE5ZTY0NWZiMDY5NzZhZmUxMGJmZSJ9.i97TrUgtimUn3M0zIBiV9tPPV4D34-5ZmcmoytzVpg0",
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "username": "Starrysparklez",
        "password": "youshallnotpass"
    })
})
```

### Success response:
```json
{
    "user": {
        "avatar_url": "http://127.0.0.1/static/usercontent/avatar_6941753682170126336.jpg",
        "created_at": "1655043049.376583",
        "id": "6941753682170126336",
        "locale": null,
        "username": "Starrysparklez"
    },
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjY5NDE3NTM2ODIxNzAxMjYzMzYsInBocyI6InBia2RmMjpzaGEyNTY6MjYwMDAwJEFneFNWYklmTVM1cm9wZW4kYmQ0NzlhMWY0Yjg5NDBjYjlhMWQ4YTdhZTA1MzFmZjA3YzQ2MWUyM2M4OGE5ZTY0NWZiMDY5NzZhZmUxMGJmZSJ9.i97TrUgtimUn3M0zIBiV9tPPV4D34-5ZmcmoytzVpg0"
}
```

### Error response (tried to set username that is already registered):
```json
{
    "error": "This username is already used. Try to use other username."
}
```

# Get user info with API
```
GET | /api/user
```

### Example request:
```json
fetch("/api/user", {
    method: "GET",
    headers: {
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjY5NDE3NTM2ODIxNzAxMjYzMzYsInBocyI6InBia2RmMjpzaGEyNTY6MjYwMDAwJEFneFNWYklmTVM1cm9wZW4kYmQ0NzlhMWY0Yjg5NDBjYjlhMWQ4YTdhZTA1MzFmZjA3YzQ2MWUyM2M4OGE5ZTY0NWZiMDY5NzZhZmUxMGJmZSJ9.i97TrUgtimUn3M0zIBiV9tPPV4D34-5ZmcmoytzVpg0"
    }
})
```

### Success response:
```json
{
    "user": {
        "avatar_url": "http://127.0.0.1/static/usercontent/avatar_6941753682170126336.jpg",
        "created_at": "1655043049.376583",
        "id": "6941753682170126336",
        "locale": null,
        "username": "Starrysparklez"
    }
}
```

### Error response (token is invalid):
```json
{
    "error": "Invalid credentials."
}
```

# Get channel list from API
```
GET | /api/channels
```

### Example request:
```json
fetch("/api/channels", {
    method: "GET",
    headers: {
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjY5NDE3NTM2ODIxNzAxMjYzMzYsInBocyI6InBia2RmMjpzaGEyNTY6MjYwMDAwJEFneFNWYklmTVM1cm9wZW4kYmQ0NzlhMWY0Yjg5NDBjYjlhMWQ4YTdhZTA1MzFmZjA3YzQ2MWUyM2M4OGE5ZTY0NWZiMDY5NzZhZmUxMGJmZSJ9.i97TrUgtimUn3M0zIBiV9tPPV4D34-5ZmcmoytzVpg0"
    }
})
```

### Success response:
```json
{
    "total_channels": 2,
    "channels_data": [
        {
            "id": "6941711225088811008",
            "name": "chill",
            "description": "Канал для расслабленного и не напряженного общения~",
            "created_at": "1655044226.913701",
        },
        {
            "id": "6941711227139825664",
            "name": "gaming",
            "description": "Игровой канал! Общение на игровые темы - здесь!",
            "created_at": "1655044256.264429",
        }
    ],
}
```

### Error response (token is invalid):
```json
{
    "error": "Invalid credentials."
}
```

# Get information about channel from API
```
GET | /api/channel
```

### Example request:
```json
fetch("/api/channel", {
    method: "GET",
    headers: {
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjY5NDE3NTM2ODIxNzAxMjYzMzYsInBocyI6InBia2RmMjpzaGEyNTY6MjYwMDAwJEFneFNWYklmTVM1cm9wZW4kYmQ0NzlhMWY0Yjg5NDBjYjlhMWQ4YTdhZTA1MzFmZjA3YzQ2MWUyM2M4OGE5ZTY0NWZiMDY5NzZhZmUxMGJmZSJ9.i97TrUgtimUn3M0zIBiV9tPPV4D34-5ZmcmoytzVpg0",
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "id": "6941711225088811008"
    })
})
```

### Success response:
```json
{
    "id": "6941711225088811008",
    "name": "chill",
    "description": "Канал для расслабленного и не напряженного общения~",
    "created_at": "1655044226.913701",
}
```

### Error response (token is invalid):
```json
{
    "error": "Invalid credentials."
}
```

# Create a new channel with API
```
PUT | /api/channel
```

### Example request:
```json
fetch("/api/channel", {
    method: "PUT",
    headers: {
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjY5NDE3NTM2ODIxNzAxMjYzMzYsInBocyI6InBia2RmMjpzaGEyNTY6MjYwMDAwJEFneFNWYklmTVM1cm9wZW4kYmQ0NzlhMWY0Yjg5NDBjYjlhMWQ4YTdhZTA1MzFmZjA3YzQ2MWUyM2M4OGE5ZTY0NWZiMDY5NzZhZmUxMGJmZSJ9.i97TrUgtimUn3M0zIBiV9tPPV4D34-5ZmcmoytzVpg0",
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "name": "general",
        "description": "Основной текстовый канал"
    })
})
```

### Success response:
```json
{
    "message": "OK"
}
```

### Error response (token is invalid):
```json
{
    "error": "Invalid credentials."
}
```

### Error response (cannot create channel due to internal error):
```json
{
    "error": "ERR"
}
```

# Delete channel with API
```
DELETE | /api/channel
```

### Example request:
```json
fetch("/api/channel", {
    method: "DELETE",
    headers: {
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjY5NDE3NTM2ODIxNzAxMjYzMzYsInBocyI6InBia2RmMjpzaGEyNTY6MjYwMDAwJEFneFNWYklmTVM1cm9wZW4kYmQ0NzlhMWY0Yjg5NDBjYjlhMWQ4YTdhZTA1MzFmZjA3YzQ2MWUyM2M4OGE5ZTY0NWZiMDY5NzZhZmUxMGJmZSJ9.i97TrUgtimUn3M0zIBiV9tPPV4D34-5ZmcmoytzVpg0",
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "id": "6941711225088811008"
    })
})
```

### Success response:
```json
{
    "message": "OK"
}
```

### Error response (token is invalid):
```json
{
    "error": "Invalid credentials."
}
```

### Error response (cannot create channel due to internal error):
```json
{
    "error": "ERR"
}
```

# Modify channel with API
```
PATCH | /api/channel
```

### Example request:
```json
fetch("/api/channel", {
    method: "PATCH",
    headers: {
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjY5NDE3NTM2ODIxNzAxMjYzMzYsInBocyI6InBia2RmMjpzaGEyNTY6MjYwMDAwJEFneFNWYklmTVM1cm9wZW4kYmQ0NzlhMWY0Yjg5NDBjYjlhMWQ4YTdhZTA1MzFmZjA3YzQ2MWUyM2M4OGE5ZTY0NWZiMDY5NzZhZmUxMGJmZSJ9.i97TrUgtimUn3M0zIBiV9tPPV4D34-5ZmcmoytzVpg0",
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "id": "6941711225088811008",
        "name": "master",
        "description": "Невероятно горячие обсуждения системы контроля версий Git. Main, или все-таки master?"
    })
})
```

### Success response:
```json
{
    "message": "OK"
}
```

### Error response (token is invalid):
```json
{
    "error": "Invalid credentials."
}
```

### Error response (cannot create channel due to internal error):
```json
{
    "error": "ERR"
}
```

# Receive a message list from the channel with API
```
GET | /api/messages/<channel_id>
```

### Example request:
```json
fetch("/api/messages/6941711225088811008", {
    method: "GET",
    headers: {
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjY5NDE3NTM2ODIxNzAxMjYzMzYsInBocyI6InBia2RmMjpzaGEyNTY6MjYwMDAwJEFneFNWYklmTVM1cm9wZW4kYmQ0NzlhMWY0Yjg5NDBjYjlhMWQ4YTdhZTA1MzFmZjA3YzQ2MWUyM2M4OGE5ZTY0NWZiMDY5NzZhZmUxMGJmZSJ9.i97TrUgtimUn3M0zIBiV9tPPV4D34-5ZmcmoytzVpg0"
    }
})
```

### Success response:
```json
{
    "total_messages": 1,
    "messages_data": [
        {
            "message": {
                "id": "7546271728395627382",
                "channel_id": "6941711225088811008",
                "content": "так все-таки давайте решимся, использовать `master` или `main`? лично я за `master`",
                "author_id": "8472635462718293716",
                "created_at": "1655045051.258762"
            },
            "author": {
                "id": "6941753682170126336",
                "username": "Starrysparklez"
                "avatar_url": "http://127.0.0.1/static/usercontent/avatar_6941753682170126336.jpg",
                "locale": null,
                "created_at": "1655043049.376583",
            },
            "channel": {
                "id": "6941711225088811008",
                "name": "chill",
                "description": "Канал для расслабленного и не напряженного общения~",
                "created_at": "1655044226.913701",
            }
        }
    ]
}
```

### Error response (token is invalid):
```json
{
    "error": "Invalid credentials."
}
```

### Error response (cannot create channel due to internal error):
```json
{
    "error": "ERR"
}
```

# Operations with messages
I am too lazy to write this documentation, but I can say that you can edit, create and delete messages same as you can do it with channels.

# Websocket events

### `message_create`
A new message has just been created. Here it is.

```json
{
    "message": { message data },
    "channel": { channel data },
    "author": { author data }
}
```

### `message_delete`
The message was deleted, that's all.

```json
{
    "message": { message data },
    "channel": { channel data },
    "author": { author data }
}
```

### `message_update`
The message has been edited.

```json
{
    "message": { message data },
    "channel": { channel data },
    "author": { author data }
}
```

### `channel_create`
A new text channel has been created.

```json
{ channel data }
```

### `channel_delete`
The text channel has been deleted.

```json
{ channel data }
```

### `channel_update`
The event of editing a text channel.

```json
{ channel data }
```
