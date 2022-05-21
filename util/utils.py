from flask_restful import reqparse

def create_alumno_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('nombres', required=True, nullable=False)
    parser.add_argument('apellidos', required=True, nullable=False)
    parser.add_argument('matricula', required=True, nullable=False)
    parser.add_argument('promedio', type=float, required=True, nullable=False)
    return parser

def create_profesor_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('nombres', required=True, nullable=False)
    parser.add_argument('apellidos', required=True, nullable=False)
    parser.add_argument('numeroEmpleado', type=int, required=True, nullable=False)
    parser.add_argument('horasClase', type=int)
    return parser
