from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from bmfork import app
from models import *
from parser import Parser
from data import Data


migrate = Migrate(app, db)
manager = Manager(app)


manager.add_command('db', MigrateCommand)
manager.add_command('parse', Parser())
manager.add_command('data', Data())


if __name__ == '__main__':
    manager.run()
