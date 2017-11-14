from . import connection, authhelper
from default import TEST_MODULES
from entities.test_module import TestModule 

class TestModuleDB():
    @staticmethod
    def db():
        client = connection.create()
        database = client[TEST_MODULES]
        for doc in database:
            pass
        return database

    @staticmethod
    def all():
        db = TestModuleDB.db()
        tm_arr = [TestModule(doc) for doc in db]
        return tm_arr

    @staticmethod
    def test_module(uno=None):
        db = TestModuleDB.db()

        if uno:
            if uno in db:
                tm = TestModule(db[uno])
                return tm

        return TestModule()

    @staticmethod
    def create(data):
        db = TestModuleDB.db()

        tm = TestModule(data)
        if not tm.valid(safe=False):
            return (False, tm)

        result = db.create_document(data)
        if not result.exists():
            return (False, tm)

        return (True, result)

    @staticmethod
    def update(tm):
        db = TestModuleDB.db()

        if tm['_id'] in db:
            doc = db[tm['_id']]
            doc.update(tm)
            doc.save()
            return True

        return False

    @staticmethod
    def delete(tm):
        db = TestModuleDB.db()

        if tm['_id'] in db:
            doc = db[tm['_id']]
            doc.update(tm)
            doc.delete()
            return True

        return False
