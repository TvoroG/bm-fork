from models import Synonym

class Header(object):

    @classmethod
    def create_header(cls, bg):
        return None

    def make_heads(self, head_sel):
        heads = head_sel.get_text(strip=True).split('.')
        return [h.strip() for h in heads]

    def find_heads_ids(self):
        syns = Synonym.query.filter(Synonym.name.in_(self.heads))
        return {s.group.category.id: s.group_id for s in syns}


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


        
