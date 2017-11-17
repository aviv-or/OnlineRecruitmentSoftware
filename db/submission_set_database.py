from . import connection, authhelper
from default import SUBMISSION_SETS
from entities.submission_set import SubmissionSet

class SubmissionSetDB():
    @staticmethod
    def db():
        client = connection.create()
        database = client[SUBMISSION_SETS]
        for doc in database:
            pass
        return database

    @staticmethod
    def all():
        db = SubmissionDB.db()
        sub_arr = [SubmissionSet(doc) for doc in db]
        return sub_arr

    @staticmethod
    def submission_set(uno=None):
        db = SubmissionSetDB.db()

        if uno:
            if uno in db:
                sub = SubmissionSet(db[uno])
                return sub
        return SubmissionSet()

    @staticmethod
    def create(data):
        db = SubmissionSetDB.db()

        sub = SubmissionSet(data)
        if not sub.valid(safe=False):
            return (False, sub)

        result = db.create_document(data)
        if not result.exists():
            return (False, sub)

        return (True, result)

    @staticmethod
    def update(sub):
        db = SubmissionSetDB.db()

        if sub['_id'] in db:
            doc = db[sub['_id']]
            doc.update(sub)
            doc.save()
            return True

        return False

    @staticmethod
    def delete(sub):
        db = SubmissionSetDB.db()

        if sub['_id'] in db:
            doc = db[sub['_id']]
            doc.delete()
            return True

        return False
