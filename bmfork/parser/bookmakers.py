# -*- coding: utf-8 -*-
import mechanize
import urllib2
from bs4 import BeautifulSoup

class Bookmaker(object):
    def __init__(self):
        self.url = None
        super(Bookmaker, self).__init__()

    def parse(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        
        bgs = self.get_bet_groups(soup)
        for bg in bgs:
            header = self.parse_header(bg)
            if header is not None:
                self.found_header(header)

            events = self.get_bet_group_events(bg)
            for e in events:
                event = self.parse_event(e)
                if event is not None:
                    self.found_event(event)

    def parse_header(self, bg):
        return None

    def found_header(self, ph):
        return None

    def parse_event(self, e):
        return None

    def found_event(self, pe):
        return None

    def get_html(self):
        return ''

    def open_connection(self):
        br = mechanize.Browser()
        br.open(self.url)
        return br

    def get_bet_groups(self, soup):
        return []

    def get_bet_group_events(self, bg):
        return []


class Betcity(Bookmaker):
    def __init__(self):
        super(Betcity, self).__init__()
        self.url = 'http://betcityru.com/bets/bets.php'

    def parse_header(self, bg):
        sel = bg.select('thead b')
        if not sel:
            return None

        return sel[0].get_text(strip=True)

    def found_header(self, ph):
        return None

    def parse_event(self, e):
        fields = e.select('tr.tc')
        fields.extend(e.select('tr.tcl'))
        if not fields:
            return None

        field = fields[0]
        team1 = field.contents[1].get_text(strip=True)
        team2 = field.contents[4].get_text(strip=True)
        return (team1, team2)

    def found_event(self, pe):
        print pe[0] + ' - ' + pe[1]
    
    def get_html(self):
        br = self.open_connection()
        br.select_form(name='bets')
        
        # пока не выбираем долгосрочные ставки
        checkboxes = br.find_control(name='line_id[]').items
        for ch in checkboxes:
            ch.selected = True

        response = br.submit()
        return response.read()

    def get_bet_groups(self, soup):
        return soup.select('body > table')

    def get_bet_group_events(self, bg):
        return bg.select('#line')


class Marathon(Bookmaker):
    def __init__(self):
        super(Marathon, self).__init__()
        self.url = 'http://www.marathonbet.com/su/betting/all'

    def parse_header(self, bg):
        sel = bg.select('.category-path')
        if not sel:
            return None
        return sel[0].get_text(strip=True)

    def found_header(self, ph):
        print '------------------'
        print ph
        print ''
        return None

    def parse_event(self, e):
        fields = e.select('div.member-name')
        fields.extend(e.select('div.today-member-name'))
        if not fields:
            return None

        team1 = fields[0].get_text(strip=True)
        team2 = fields[1].get_text(strip=True)
        return (team1, team2)

    def found_event(self, pe):
        print pe[0] + ' - ' + pe[1]

    def get_html(self):
        html = urllib2.urlopen(self.url)
        return html

    def get_bet_groups(self, soup):
        return soup.select('#container_EVENTS > .main-block-events')

    def get_bet_group_events(self, bg):
        return bg.select('table.foot-market tbody')


if __name__ == '__main__':
    m = Marathon()
    m.parse()
