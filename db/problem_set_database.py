from . import connection, authhelper
from default import PROBLEM_SETS
from entities.problem_set import ProblemSet 

class ProblemSetDB():
    @staticmethod
    def db():
        client = connection.create()
        database = client[PROBLEM_SETS]
        for doc in database:
            pass
        return database

    @staticmethod
    def all():
        db = ProblemSetDB.db()
        ps_arr = [ProblemSet(doc) for doc in db]
        return ps_arr

    @staticmethod
    def problem_set(uno=None):
        db = ProblemSetDB.db()

        if uno:
            if uno in db:
                ps = ProblemSet(db[uno])
                return ps
        ps = ProblemSet()
        return ps

    @staticmethod
    def create(data):
        db = ProblemSetDB.db()

        ps = ProblemSet(data)
        if not ps.valid(safe=False):
            return (False, ps)

        result = db.create_document(data)
        if not result.exists():
            return (False, ps)

        return (True, result)

    @staticmethod
    def update(ps):
        db = ProblemSetDB.db()

        if ps['_id'] in db:
            doc = db[ps['_id']]
            doc.update(ps)
            doc.save()
            return True

        return False

    @staticmethod
    def delete(ps):
        db = ProblemSetDB.db()

        if ps['_id'] in db:
            doc = db[ps['_id']]
            doc.update(ps)
            doc.delete()
            return True

        return False









