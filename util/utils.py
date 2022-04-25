from flask import abort
from flask_restful import reqparse

def create_alumno_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('id')
    parser.add_argument('nombres')
    parser.add_argument('apellidos')
    parser.add_argument('matricula')
    parser.add_argument('promedio', required=True, type=float)
    return parser

def create_profesor_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('id', )
    parser.add_argument('nombres')
    parser.add_argument('apellidos')
    parser.add_argument('numeroEmpleado')
    parser.add_argument('horasClase', required=True, type=int)
    return parser

def abort_if_entity_doesnt_exist(id, entities):
    if id not in entities:
        abort(404, description=f'ID: {id} not found')

def create_alumno(args):
    if (args['promedio'] < 0 
    or args['matricula'][0] != 'A'):
        abort(400)

    alumno = {
        'id': args['id'],
        'nombres': args['nombres'],
        'apellidos': args['apellidos'],
        'matricula': args['matricula'],
        'promedio': args['promedio']
    }
    return alumno

def create_profesor(args):
    if args['horasClase'] < 0:
        abort(400)
    
    profesor = {
        'id': args['id'],
        'numeroEmpleado': args['numeroEmpleado'],
        'nombres': args['nombres'],
        'apellidos': args['apellidos'],
        'horasClase': args['horasClase']
    }
    return profesor
