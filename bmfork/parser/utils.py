# -*- coding: utf-8 -*-
from models import db

def create_sets_from(syns):
    ids = {}
    for s in syns:
        cid = s.group.category.id
        if cid not in ids:
            ids[cid] = set()
        ids[cid].add(s.group_id)
    return ids

    
def get_or_create(model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance is not None:
        return instance
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance
