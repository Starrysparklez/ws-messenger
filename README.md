# Hello world, welcome to my world's best messenger!!!!!!!!!!!
~~This project is just a ridiculous copy of Discord, but (so far) without support for servers, bots, no normal interface, no application for PCs and smartphones, and without much more!~~  
**THIS IS SIMPLY THE BEST MESSENGER YOU'VE EVER SEEN IN YOUR LIFE!!!! DROP DISCORD, DOWNLOAD THIS AWESOME MESSENGER!!!!**

## Requirements
- python 3 *(tested on `3.9`)* and pip
- gaming computer with intel xeon e5 cpu
- 10 gbps internet

# Installation
anyway, this stuff can be installed by several methods, e.g. through a docker or just with a python command !!!! choose!!

## Running without Docker
1. clone this super cool repository !!!
```shell
$ git clone https://github.com/Starrysparklez/my-stupid-messenger.git
```
2. install dependencies 👀
```shell
$ pip3 install -r req.txt
```
3. and now we need to prepare the application for the first run 😍😍😍
```shell
$ python3 manager.py setup
```
4. RUN THIS ~~SHIT~~ using `tmux`, `screen` or something similar 😍
```shell
$ screen -dmS supercoolmessenger python3 manager.py runserver
```
or use `rundev` instead of `runserver` to run development server 👀

5. ENJOY !!!!!!!!!!!!

## Running with Docker
1. clone this super cool repository AGAIN !!!!
```shell
$ git clone https://github.com/Starrysparklez/my-stupid-messenger.git
```
2. build docker image !!!
```shell
$ cd my-stupid-messenger && docker build .
```
3. run image !! and dont forget to open port 5000 !!!
```shell
$ docker run -d --net host <id-of-the-image-that-was-displayed-after-the-build>
```

# Super awesome open source projects used in this app 👀
1. [Flask](https://github.com/pallets/flask)
   - License: [BSD-3-Clause License](https://github.com/pallets/flask/blob/main/LICENSE.rst)
2. [Flask-Login](https://github.com/maxcountryman/flask-login)
   - License: [MIT License](https://github.com/maxcountryman/flask-login/blob/main/LICENSE)
3. [Flask-WTF](https://github.com/wtforms/flask-wtf)
   - License: [BSD-3-Clause License](https://github.com/wtforms/flask-wtf/blob/main/LICENSE.rst)
4. [Flask-Script](https://github.com/smurfix/flask-script)
   - License: [Yes](https://github.com/smurfix/flask-script/blob/master/LICENSE)
5. [Flask-SocketIO](https://github.com/miguelgrinberg/Flask-SocketIO)
   - License: [MIT License](https://github.com/miguelgrinberg/Flask-SocketIO/blob/main/LICENSE)
6. [Flask-Compress](https://github.com/colour-science/flask-compress)
   - License: [MIT License](https://github.com/colour-science/flask-compress/blob/master/LICENSE.txt)
7. [Flask-SQLAlchemy](https://github.com/pallets/flask-sqlalchemy)
   - License: [BSD-3-Clause License](https://github.com/pallets/flask-sqlalchemy/blob/main/LICENSE.rst)
8. [pyjwt](https://github.com/jpadilla/pyjwt)
   - License: [MIT License](https://github.com/jpadilla/pyjwt/blob/master/LICENSE)
9. [eventlet](https://github.com/eventlet/eventlet)
   - License: [MIT License](https://github.com/eventlet/eventlet/blob/master/LICENSE)
