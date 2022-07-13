from app import create_flask, db
from flask_script import Manager
from traceback import format_exc as format_exception
from textwrap import indent
from psycopg2._psycopg import connection, cursor

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
    admin_user = db.get_user(username=ADMIN_LOGIN)
    if not admin_user:
        print("Can't save a fake dataset, because admin user doesn't exist."\
              "\nRun the 'setup' command first.")
        return

    fake_channel_data = (
        ("general", "Основной канал"),
        ("chill", "Канал для расслабленного и не напряженного общения"),
        ("gaming", "Игровой канал"),
        ("coding", "Капец"),
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
            'а вообще, это неправда ... блин, что бы такого придумать еще, чтобы просто заполнить каналы фейковыми данными "чтобы было" ? :(',
        ),
        "coding": (
            "если вы находитесь в этом канале и видите это сообщение - это знак того, что в плане кодинга я не стою на месте, ведь я написала этот чат!",
        ),
    }
    from app.models.channel import Channel
    from app.models.message import Message

    admin = db.get_user(role='admin')
    if not admin:
        print('Can not process your command because admin role does not exist.\nPlease, use "manager.py setup" first.')
        return

    for name, title in fake_channel_data:
        print(f"Creating channel #{name}...", end="\t")
        channel = db.create_channel(Channel(name=name, topic=title, type='text'))
        print(f"OK")
        for text in fake_message_data[name]:
            print(f"Creating message...", end="\t")
            db.create_message(
                Message(channel=channel, author=admin, content=text)
            )
            print(f"OK")
    print("Fake data generation complete.")


@manager.command
def setup():
    print("Creating admin user...", end="\t")
    try:
        from app.models.user import User
        admin = User(username=ADMIN_LOGIN, role='admin')
        admin.password = ADMIN_PASSWORD
        db.create_user(admin, ignore_admin_limit=True)
    except Exception:
        print("FAIL")
        print(indent(format_exception(), "\t"))
        return
    else:
        print(f"OK\nAdmin credentials:\nUsername: {ADMIN_LOGIN}\nPassword: {ADMIN_PASSWORD}"\
              f"\nAPI token: {admin.generate_auth_token()}")

    print("Setup complete.")

@manager.command
def updateadmin():
    print("Admin user update...")
    new_username = input("New username: ")
    new_password = input("New password: ")
    admin = db.get_user(role=101)
    admin.username = new_username
    admin.password = new_password
    db.modify_user(admin)
    print("OK")

@manager.command
def cleardb():
    print("Deleting tables...")
    for table_name in ("users", "messages", "channels"):
        with db.connection.cursor() as cur:
            cur: cursor
            cur.execute("DROP TABLE " + table_name)
        db.connection.commit()


if __name__ == "__main__":
    manager.run()
