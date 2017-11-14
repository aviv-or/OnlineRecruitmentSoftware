from . import connection, authhelper
from default import USERS
from entities.user import User 

class UserDB():
    @staticmethod
    def db():
        client = connection.create()
        database = client[USERS]
        for doc in database:
            pass
        return database

    @staticmethod
    def all():
        db = UserDB.db()
        user_arr = [User(doc) for doc in db]
        return user_arr

    @staticmethod
    def user(uno=None, email=None, password=None):
        db = UserDB.db()

        if uno:
            return User(db.get(uno))

        elif email:
            for doc in db:
                if doc['email'] == email:
                    if password:
                        if doc['password'] != authhelper.crypt(password):
                            return User()
                    return User(doc)

        return User()

    @staticmethod
    def create(data):
        db = UserDB.db()

        user = User(data)
        if not user.valid(safe=False):
            return (False, user)

        for doc in db:
            if doc['email'] == user['email']:
                user.error = User.Error.EMAIL_ALREADY_EXISTS
                return (False, user)

        result = db.create_document(data)
        if not result.exists():
            return (False, user)

        return (True, result)

    @staticmethod
    def update(user):
        db = UserDB.db()

        if user['_id'] in db:
            doc = db[user['_id']]
            doc.update(user)
            doc.save()
            return True

        return False

    @staticmethod
    def delete(user):
        db = UserDB.db()

        if user['_id'] in db:
            doc = db[user['_id']]
            doc.update(user)
            doc.delete()
            return True

        return False







