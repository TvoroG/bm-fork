from flask.ext.script import Command, Option
from .bookmakers import Betcity, Marathon

class Parser(Command):

    option_list = (
        Option('bookmaker', choices=['betcity', 'marathon']),
    )

    def run(self, bookmaker):
        if bookmaker == 'betcity':
            bm = Betcity()
        elif bookmaker == 'marathon':
            bm = Marathon()
        bm.parse()
