from . import connection, authhelper
from default import SUBMISSIONS
from entities.submission import Submission 

class SubmissionDB():
    @staticmethod
    def db():
        client = connection.create()
        database = client[SUBMISSIONS]
        for doc in database:
            pass
        return database

    @staticmethod
    def all():
        db = SubmissionDB.db()
        sub_arr = [Submission(doc) for doc in db]
        return sub_arr

    @staticmethod
    def submission(uno=None):
        db = SubmissionDB.db()

        if uno:
            if uno in db:
                sub = Submission(db[uno])
                return sub
        return Submission()

    @staticmethod
    def create(data):
        db = SubmissionDB.db()

        sub = Submission(data)
        if not sub.valid(safe=False):
            print("Submission Not Valid")
            print(sub.error.name)
            return (False, sub)

        result = db.create_document(data)
        if not result.exists():
            return (False, sub)

        return (True, result)

    @staticmethod
    def update(sub):
        db = SubmissionDB.db()

        if sub['_id'] in db:
            doc = db[sub['_id']]
            doc.update(sub)
            doc.save()
            return True

        return False

    @staticmethod
    def delete(sub):
        db = SubmissionDB.db()

        if sub['_id'] in db:
            doc = db[sub['_id']]
            doc.delete()
            return True

        return False
