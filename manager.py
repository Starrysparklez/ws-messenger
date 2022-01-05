from app import create_flask, db
from flask_script import Manager
from traceback import format_exc as format_exception
from textwrap import indent

from config import ADMIN_LOGIN, ADMIN_PASSWORD, SERVER_ADDRESS, SERVER_PORT

app, socketio = create_flask()
manager = Manager(app)

@manager.command
def runserver():
    socketio.run(app, host=SERVER_ADDRESS, port=SERVER_PORT)

@manager.command
def rundev():
    app.config["ENV"] = "development"
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    socketio.run(app, host=SERVER_ADDRESS, port=SERVER_PORT, debug=True)

@manager.command
def makefake():
    fake_channel_data = (
        ("general", "Основной канал для основного общения. Хорошо сказано!!!!!"),
        ("chill",   "Канал для расслабленного и не напряженного общения~"),
        ("gaming",  "Игровой канал! Общение на игровые темы - здесь!"),
        ("coding",  "Темы касаемо программирования и разработки чего-либо крутого!")
    )
    fake_message_data = {
        "general": (
            "ой, привет !",
            "как вы тут поживаете ?",
            "никак ? я так и поняла, извините ...",
            "...",
            "лорем ипсум долор сит амет ... или как там оно было, та заглушка текстовая которую используют вечно в веб разработке",
            "пофиг, думаю что для демонстрации фейковых данных, генерируемых командой `python3 manager.py makefake` этих сообщений хватит :)",
        ),
        "chill": (
            "сегодня я наконец-то выспалась как следует ... правда проспала аж до 6 часов вечера!",
            "пойду покушаю пожалуй ...",
        ),
        "gaming": (
            "сегодня наконец-то достигла 100 побед в vampirez на hypixel !",
            "это было сложно, но у меня получилось !~",
            "а вообще, это неправда ... блин, что бы такого придумать еще, чтобы просто заполнить каналы фейковыми данными \"чтобы было\" ? :(",
        ),
        "coding": (
            "если вы находитесь в этом канале и видите это сообщение - это знак того, что в плане кодинга я не стою на месте, ведь я написала этот чат!",
        )
    }
    from app.models.channel import TextChannel
    from app.models.message import Message
    for name, title in fake_channel_data:
        print(f"Creating text channel #{name}...", end="\t")
        channel = TextChannel(name=name, title=title)
        db.session.add(channel)
        db.session.commit()
        print(f"OK")
        for text in fake_message_data[name]:
            print(f"Creating message...", end="\t")
            message = Message(channel_id=channel.id, author_id=1, content=text)
            db.session.add(message)
            db.session.commit()
            print(f"OK")
    print("Fake data generation complete.")

@manager.command
def setup():
    print("Creating tables...", end="\t")
    try:
        db.create_all()
        db.session.commit()
    except Exception:
        print("FAIL")
        print(indent(format_exception(), "\t"))
        return
    else:
        print("OK")

    print("Creating admin user...", end="\t")
    try:
        from app.models.user import User
        admin = User(username=ADMIN_LOGIN)
        admin.password = ADMIN_PASSWORD
        db.session.add(admin)
        db.session.commit()
    except Exception:
        print("FAIL")
        print(indent(format_exception(), "\t"))
        return
    else:
        print("OK")

    print("Setup complete.")

if __name__ == "__main__":
    manager.run()
