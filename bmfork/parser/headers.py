from models import Synonym
from utils import create_sets_from

class Header(object):

    @classmethod
    def create_header(cls, bg):
        return None

    def make_heads(self, head_sel):
        heads = head_sel.get_text(strip=True).split('.')
        return [h.strip() for h in heads]

    def find_heads_ids(self):
        syns = Synonym.query.filter(Synonym.name.in_(self.heads))
        hids = create_sets_from(syns)
        return hids

    def __eq__(self, h):
        for cat in self.heads_ids:
            if cat in h.heads_ids:
                if not self.heads_ids[cat] & h.heads_ids[cat]:
                    return False
        return True
                


class BetcityHeader(Header):

    def __init__(self, head_sel, bet_pos):
        self.heads = self.make_heads(head_sel)
        self.bet_pos = bet_pos
        self.heads_ids = self.find_heads_ids()


class MarathonHeader(Header):

    def __init__(self, head_sel, bet_pos):
        self.heads = self.make_heads(head_sel)
        self.bet_pos = bet_pos
        self.heads_ids = self.find_heads_ids()


        
