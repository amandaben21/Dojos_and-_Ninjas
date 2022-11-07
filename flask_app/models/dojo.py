from flask_app.config.mysqlconnection import connectToMySQL
from .ninja import Ninja #instead of saying "from flask_app.models.ninja" you can write "from .ninja" to import b/c its coming from the same folder/file

class Dojo:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas = []


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"

        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query)
        dojos = []

        for d in results:
            dojos.append( cls(d) )
        return dojos

    @classmethod
    def save(cls, data):
        query= "INSERT INTO dojos (name) VALUES (%(name)s);"
        # it's "result" and not "results" b/c its coming back with one id
        result = connectToMySQL('dojos_and_ninjas_schema').query_db(query,data)
        return result

    @classmethod
    def get_one_with_ninjas(cls, data ):
        query = "SELECT * FROM dojos LEFT JOIN ninjas on dojos.id = ninjas.dojo_id WHERE dojos.id = %(id)s;"
        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query,data)
        print(results)
        dojo = cls(results[0])
        for r in results:
            n = {
                'id': r['ninjas.id'],
                'first_name': r['first_name'],
                'last_name': r['last_name'],
                'age': r['age'],
                'created_at': r['ninjas.created_at'],
                'updated_at': r['ninjas.updated_at']
            }
            dojo.ninjas.append( Ninja(n) )
        return dojo