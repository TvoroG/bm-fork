from flask.ext.script import Command
from .bookmakers import Betcity, Marathon

class Parser(Command):

    def run(self):
        bm = Betcity()
        bm.parse()
