# Project description
This project is an attempt to recreate something like Discord. But open, free, and simpler.

## Requirements
- Python 3 *(Tested on 3.8 and 3.9)* & pip

# Installation
## Running on your server
0. Install Python 3
1. Clone this repository
```shell
$ git clone https://codeberg.org/Starrysparklez/ws-messenger
```
2. Install dependencies
```shell
$ pip3 install -r req.txt
```
3. Create an admin account
```shell
$ python3 manager.py setup
```
4. Run the server
```shell
$ screen -dmS supercoolmessenger python3 manager.py runserver
```
You can also use 'rundev' instead of 'runserver' to run in development mode.

# Super awesome open source projects used in this app 👀
1. [Flask](https://github.com/pallets/flask)
   - License: [BSD-3-Clause License](https://github.com/pallets/flask/blob/main/LICENSE.rst)
3. [Flask-WTF](https://github.com/wtforms/flask-wtf)
   - License: [BSD-3-Clause License](https://github.com/wtforms/flask-wtf/blob/main/LICENSE.rst)
4. [Flask-Script](https://github.com/smurfix/flask-script)
   - License: [Yes](https://github.com/smurfix/flask-script/blob/master/LICENSE)
5. [Flask-SocketIO](https://github.com/miguelgrinberg/Flask-SocketIO)
   - License: [MIT License](https://github.com/miguelgrinberg/Flask-SocketIO/blob/main/LICENSE)
6. [Flask-Compress](https://github.com/colour-science/flask-compress)
   - License: [MIT License](https://github.com/colour-science/flask-compress/blob/master/LICENSE.txt)
8. [pyjwt](https://github.com/jpadilla/pyjwt)
   - License: [MIT License](https://github.com/jpadilla/pyjwt/blob/master/LICENSE)
9. [eventlet](https://github.com/eventlet/eventlet)
   - License: [MIT License](https://github.com/eventlet/eventlet/blob/master/LICENSE)
