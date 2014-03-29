import os
from flask.ext.script import Command, Option
from models import Category, Synonym, Group, db
from parser.utils import get_or_create

class Data(Command):

    UPDATE = 'update'
    VERIFY = 'verify'

    option_list = (
        Option('command', choices=[UPDATE, VERIFY]),
    )

    directory = 'data/files'
    
    def run(self, command):
        if command == self.UPDATE:
            self.update()
        elif command == self.VERIFY:
            self.verify()

    def update(self):
        def update_inner(f):
            self.insert(f)

        self.walk(update_inner)

        
    def verify(self):
        def verify_inner(f):
            lines, cats = self.check(f)
            print ('{0}:\n\tcategories: {1}\n\terrors: {2}'
                   .format(f.name, ', '.join(cats), ','.join(lines)))
        
        self.walk(verify_inner)
        
    def walk(self, func):
        filenames = os.listdir(self.directory)
        for name in filenames:
            path = os.path.join(self.directory, name)
            if path[-1] == '~':
                continue
            with open(path, 'r') as f:
                func(f)

    def insert(self, f):
        for line in f:
            parts = line.split()
            if parts:
                cat_name = parts[0]
                syns = []
                for i in xrange(1, len(parts)):
                    syns.append(' '.join(parts[i].split('_')))
                self.save(cat_name, syns)

    def save(self, cat_name, syns):
        cat = get_or_create(Category, name=cat_name)
        group = Group(category_id=cat.id)
        db.session.add(group)
        db.session.commit()

        for s in syns:
            synonym = Synonym(group_id=group.id, name=s)
            db.session.add(synonym)
        db.session.commit()
                
    def check(self, f):
        line_numbers = []
        cats = []
        n = 1
        for line in f:
            parts = line.split()
            if len(parts) < 2:
                line_numbers.append(str(n))
            if parts and parts[0] not in cats:
                cats.append(parts[0])
            n += 1
        return (line_numbers, cats)
