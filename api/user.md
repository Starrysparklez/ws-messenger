# User API
This api is used to register, log in, modify and do other stuff with the user's data.

## Register a new user
```
POST | /user/register
```

Example request:
```js
fetch('http://localhost:5000/api/v1/user/register', {
    method: 'POST',
    body: JSON.stringify({
        'username': 'Kapets',
        'password': 'youshallnotpass'
    })
});
```

Response:
```json
{
    "data": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOiI2OTUzMDkzMTYwMzEwNTc5MjAwIiwicGhzIjoicGJrZGYyOnNoYTI1NjoyNjAwMDAkZ2tpdktOdXhRUFhNZnFZZyRhYmVhZTQzNWRmMTAxMzRkMjc5OWZkOTIwNTQ4YzZkNGYzZWZjYWRlNjEyOTZjZjM3Mzk4OTY1MzY4YzI4YTJkIn0.ibvbYo6bqFVYTw917lhv1s5OI2sThQc1uxsT0ryVvdEU6icrrKwuCVGmhCJxcAdF-OqhvQCaNic4WQ1sMAe-Um8a-JhYTuHeZ-f83dDHcUp4P-rkKzi_UexRxaVJBquHOSfXNlfqcvq9Q_F6yUyR-YWtSmHNhKlTj-SndZcRpYA",
        "user": {
            "avatar_url": "http://127.0.0.1/static/usercontent/avatars/6953093160310579200.jpg",
            "created_at": "Thu Jul 14 04:09:51 2022",
            "discriminator": "3086",
            "id": "6953093160310579200",
            "locale": null,
            "role": "user",
            "username": "Kapets"
        }
    },
    "status": "OK"
}
```

## Log in with user name and password
```
POST | http://localhost:5000/api/v1/user/login
```

Example request:
```js
fetch('http://localhost:5000/api/v1/user/login', {
    method: 'POST',
    body: JSON.stringify({
        'username': 'Kapets',
        'password': 'youshallnotpass'
    })
});
```

Response:
```json
{
    "data": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOiI2OTUzMDkzMTYwMzEwNTc5MjAwIiwicGhzIjoicGJrZGYyOnNoYTI1NjoyNjAwMDAkZ2tpdktOdXhRUFhNZnFZZyRhYmVhZTQzNWRmMTAxMzRkMjc5OWZkOTIwNTQ4YzZkNGYzZWZjYWRlNjEyOTZjZjM3Mzk4OTY1MzY4YzI4YTJkIn0.ibvbYo6bqFVYTw917lhv1s5OI2sThQc1uxsT0ryVvdEU6icrrKwuCVGmhCJxcAdF-OqhvQCaNic4WQ1sMAe-Um8a-JhYTuHeZ-f83dDHcUp4P-rkKzi_UexRxaVJBquHOSfXNlfqcvq9Q_F6yUyR-YWtSmHNhKlTj-SndZcRpYA",
        "user": {
            "avatar_url": "http://127.0.0.1/static/usercontent/avatars/6953093160310579200.jpg",
            "created_at": "Thu Jul 14 04:09:51 2022",
            "discriminator": "3086",
            "id": "6953093160310579200",
            "locale": null,
            "role": "user",
            "username": "Kapets"
        }
    },
    "status": "OK"
}
```

## Getting user information from user token
```
GET | http://localhost:5000/api/v1/user
```

Example request:
```js
fetch('http://localhost:5000/api/v1/user', {
    method: 'GET',
    headers: {
        'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOiI2OTUzMDkzMTYwMzEwNTc5MjAwIiwicGhzIjoicGJrZGYyOnNoYTI1NjoyNjAwMDAkZ2tpdktOdXhRUFhNZnFZZyRhYmVhZTQzNWRmMTAxMzRkMjc5OWZkOTIwNTQ4YzZkNGYzZWZjYWRlNjEyOTZjZjM3Mzk4OTY1MzY4YzI4YTJkIn0.ibvbYo6bqFVYTw917lhv1s5OI2sThQc1uxsT0ryVvdEU6icrrKwuCVGmhCJxcAdF-OqhvQCaNic4WQ1sMAe-Um8a-JhYTuHeZ-f83dDHcUp4P-rkKzi_UexRxaVJBquHOSfXNlfqcvq9Q_F6yUyR-YWtSmHNhKlTj-SndZcRpYA'
    }
});
```

Response:
```json
{
    "data": {
        "avatar_url": "http://127.0.0.1/static/usercontent/avatars/6953093160310579200.jpg",
        "created_at": "Thu Jul 14 04:09:51 2022",
        "discriminator": "3086",
        "id": "6953093160310579200",
        "locale": "en_US",
        "role": "user",
        "username": "Kapets"
    },
    "status": "OK"
}
```

## Modify user information
```
PATCH | http://localhost:5000/api/v1/user
```

Example request:
```js
fetch('http://localhost:5000/api/v1/user', {
    method: 'PATCH',
    headers: {
        'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOiI2OTUzMDkzMTYwMzEwNTc5MjAwIiwicGhzIjoicGJrZGYyOnNoYTI1NjoyNjAwMDAkZ2tpdktOdXhRUFhNZnFZZyRhYmVhZTQzNWRmMTAxMzRkMjc5OWZkOTIwNTQ4YzZkNGYzZWZjYWRlNjEyOTZjZjM3Mzk4OTY1MzY4YzI4YTJkIn0.ibvbYo6bqFVYTw917lhv1s5OI2sThQc1uxsT0ryVvdEU6icrrKwuCVGmhCJxcAdF-OqhvQCaNic4WQ1sMAe-Um8a-JhYTuHeZ-f83dDHcUp4P-rkKzi_UexRxaVJBquHOSfXNlfqcvq9Q_F6yUyR-YWtSmHNhKlTj-SndZcRpYA'
    },
    body: JSON.stringify({
        'username': 'I am KAPETS',
        'password': 'ush@l1n0tp@5s',
        'discriminator': '1010'
    })
});
```

Response:
```json
{
    "data": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOiI2OTUzMDkzMTYwMzEwNTc5MjAwIiwicGhzIjoicGJrZGYyOnNoYTI1NjoyNjAwMDAkVG1TOWk1d0t3ZVFlQUp4aiQxOWJhOWY0ZThlNGM2ZTRmMjNmOGEzNWFlMThhMWFhYjU1OTU4NjBmNzdiMjVjODYyYWFhNzUyYWJhNGIwM2E5In0.YUbBBTQl6FTMG6eQ8KYhIVLuG3LyCu-V6b7PrMjLS-9QCm7MSoXubI51Zqy57pqpQ7pJyS7Mh9-OY-kN7CBlMvhWJfeUfnBoN5nIQTLywAhb0PPNjIDtyZgCNKUawhHEpO3-aG4TGvzKcPvgIGLKwJ8AFwYL365TYijTMDYtNvo",
        "user": {
            "avatar_url": "http://127.0.0.1/static/usercontent/avatars/6953093160310579200.jpg",
            "created_at": "Thu Jul 14 04:09:51 2022",
            "discriminator": "1010",
            "id": "6953093160310579200",
            "locale": "en_US",
            "role": "user",
            "username": "I am KAPETS"
        }
    },
    "status": "OK"
}
```
