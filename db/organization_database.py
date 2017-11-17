from . import connection, authhelper
from default import ORGANIZATIONS
from entities.organization import Organization 

class OrganizationDB():
    @staticmethod
    def db():
        client = connection.create()
        database = client[ORGANIZATIONS]
        for doc in database:
            pass
        return database

    @staticmethod
    def all():
        db = OrganizationDB().db()
        org_arr = [Organization(doc) for doc in db]
        return org_arr

    @staticmethod
    def organization(uno=None, email=None, password=None):
        db = OrganizationDB.db()
        if uno:
            return Organization(db.get(uno))

        elif email:
            for doc in db:
                if doc['email'] == email:
                    if password:
                        if doc['password'] != authhelper.crypt(password):
                            return Organization(doc)
                    return Organization(doc)
        else:
            return Organization()

    @staticmethod
    def create(data):
        db = OrganizationDB.db()

        org = Organization(data)
        if not org.valid(safe=False):
            return (False, org)

        for doc in db:
            if doc['email'] == org['email']:
                org.error = Org.Error.EMAIL_ALREADY_EXISTS
                return (False, org)

        result = db.create_document(data)
        if not result.exists():
            return (False, org)

        return (True, result)

    @staticmethod
    def update(org):
        db = OrganizationDB.db()

        if org['_id'] in db:
            doc = db[org['_id']]
            doc.update(org)
            doc.save()
            return True

        return False

    @staticmethod
    def delete(org):
        db = OrganizationDB.db()

        if org['_id'] in db:
            doc = db[org['_id']]
            doc.delete()
            return True

        return False
