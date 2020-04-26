from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand
from app import app, db
from app.superuser import CreateSuperUser

manager = Manager(app)
manager.add_command("createsuperuser", CreateSuperUser(db))
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell)
manager.add_command('runserver', Server(
    use_debugger = False,
    use_reloader = False,
    host = app.config['HOST'],
    port = app.config['PORT']
    )
)

if __name__ == "__main__":
    manager.run()