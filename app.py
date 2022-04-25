from flask import Flask, jsonify
from flask_restful import reqparse, Resource, Api
from util.utils import *

app = Flask(__name__)
api = Api(app, catch_all_404s=True)

ALUMNOS = []
PROFESORES = []

alumno_parser = create_alumno_parser()
profesor_parser = create_profesor_parser()

class Alumno(Resource):
    def get(self, id):
        found = list(filter(lambda i: i['id'] == id, ALUMNOS))
        return found[0] if found else abort(404)

    def put(self, id):
        args = alumno_parser.parse_args()
        new_alumno = create_alumno(args)
        found = list(filter(lambda i : i['id'] == id, ALUMNOS))
        if found:
            ALUMNOS.remove(found[0])
        ALUMNOS.append(new_alumno)
        return new_alumno

    def delete(self, id):
        found = list(filter(lambda i: i['id'] == id, ALUMNOS))
        if found: 
            ALUMNOS.remove(found[0])
            return found[0]
        abort(404)


class ListaDeAlumnos(Resource):
    def get(self):
        return ALUMNOS
    
    def post(self):
        args = alumno_parser.parse_args()
        alumno = create_alumno(args)
        ALUMNOS.append(alumno)
        return alumno, 201


class Profesor(Resource):
    def get(self, id):
        found = list(filter(lambda i: i['id'] == id, PROFESORES))
        return found[0] if found else abort(404)

    def put(self, id):
        args = profesor_parser.parse_args()
        new_profesor = create_profesor(args)
        found = list(filter(lambda i : i['id'] == id, PROFESORES))
        if found:
            PROFESORES.remove(found[0])
        PROFESORES.append(new_profesor)
        return new_profesor

    def delete(self, id):
        found = list(filter(lambda i: i['id'] == id, PROFESORES))
        if found:
            PROFESORES.remove(found[0])
            return found[0]
        abort(404)


class ListaDeProfesores(Resource):
    def get(self):
        return PROFESORES
    
    def post(self):
        args = profesor_parser.parse_args()
        profesor = create_profesor(args)
        PROFESORES.append(profesor)
        return profesor, 201


api.add_resource(ListaDeAlumnos, '/alumnos')
api.add_resource(Alumno, '/alumnos/<id>')

api.add_resource(ListaDeProfesores, '/profesores')
api.add_resource(Profesor, '/profesores/<id>')

@app.errorhandler(404)
def not_found(e):
    return { 'message': e }

if __name__ == '__main__':
    app.run(debug=True)