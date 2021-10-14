from xplur.database import db

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def create(data, model):
        obj = model(**data)
        db.session.add(obj)
        db.session.commit()
        return obj

    def delete(instance):
        db.session.delete(instance)
        db.session.commit()
        return True

    def update(instance, data): 
        instance.update(data)
        db.session.commit()
        return True

    def bulk_create(data):
        db.session.bulk_save_objects(data)
        db.session.commit()
        return True
