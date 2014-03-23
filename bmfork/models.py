from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    groups = db.relationship('Group', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category %s>' % self.name


class Synonym(db.Model):
    __tablename__ = 'synonyms'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return '<Synonym %d %s>' % (self.id, self.name)


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)

    synonyms = db.relationship('Synonym', backref='group',
                               lazy='dynamic')
    children = db.relationship('Group',
        backref=db.backref("parent", remote_side=id), lazy='dynamic')

    def __repr__(self):
        return '<Group %d %d>' % (self.id, self.category_id)

