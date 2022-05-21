import boto3
import os
from flask import Flask, jsonify, request
from flask_restful import reqparse, Resource, Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from util.utils import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI') or 'sqlite:///sicei.db'
app.config['UPLOAD_FOLDER'] = './upload'
api = Api(app, catch_all_404s=True)

aws_bucket = 'fotos-sicei-aws'

alumno_parser = create_alumno_parser()
profesor_parser = create_profesor_parser()

db = SQLAlchemy(app)

if not os.path.exists('./upload'):
    os.mkdir('./upload')

class AlumnoEntity(db.Model):
    __tablename__ = 'Alumnos'

    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    matricula = db.Column(db.String(10), unique=True)
    promedio = db.Column(db.Float)
    fotoPerfilUrl = db.Column(db.String(100))

    def __init__(self, nombres, apellidos, matricula, promedio):
        self.nombres = nombres
        self.apellidos = apellidos
        self.matricula = matricula
        self.promedio = promedio
        self.fotoPerfilUrl = ''

    def __repr__(self):
        return f'<Alumno {self.id}>'

    def serialize(self):
        return {
            'id': self.id,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'matricula': self.matricula,
            'promedio': self.promedio,
            'fotoPerfilUrl': self.fotoPerfilUrl
        }

class ProfesorEntity(db.Model):
    __tablename__ = 'Profesores'

    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    numeroEmpleado = db.Column('numeroEmpleado', db.Integer, unique=True)
    horasClase = db.Column('horasClase', db.Integer)

    def __init__(self, nombres, apellidos, numeroEmpleado, horasClase):
        self.nombres = nombres
        self.apellidos = apellidos
        self.numeroEmpleado = numeroEmpleado
        self.horasClase = horasClase

    def __repr__(self):
        return f'<Profesor {self.id}>'

    def serialize(self):
        return {
            'id': self.id,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'numeroEmpleado': self.numeroEmpleado,
            'horasClase': self.horasClase
        }

db.create_all()


class Alumno(Resource):
    def get(self, id):
        alumno = AlumnoEntity \
            .query \
            .filter_by(id=id) \
            .first_or_404(description=f'Alumno con ID {id} no encontrado')
        return alumno.serialize()

    def put(self, id):
        args = alumno_parser.parse_args()
        alumno = AlumnoEntity \
            .query \
            .filter_by(id=id) \
            .first_or_404(description=f'Alumno con ID {id} no encontrado')
                
        for arg in args:
            setattr(alumno, arg, args[arg])
        db.session.commit()
        return alumno.serialize(), 200

    def delete(self, id):
        alumno = AlumnoEntity \
            .query \
            .filter_by(id=id) \
            .first_or_404(description=f'Alumno con ID {id} no encontrado')
        db.session.delete(alumno)
        db.session.commit()
        return 


class ListaDeAlumnos(Resource):
    def get(self):
        alumnos = AlumnoEntity.query.all()
        return [alumno.serialize() for alumno in alumnos]
    
    def post(self):
        args = alumno_parser.parse_args()
        alumno = AlumnoEntity(
            args['nombres'], 
            args['apellidos'], 
            args['matricula'], 
            args['promedio']
        )
        db.session.add(alumno)
        db.session.commit()
        return alumno.serialize(), 201


class FotoDePerfilAlumno(Resource):
    def post(self, id):
        alumno = AlumnoEntity \
        .query \
        .filter_by(id=id) \
        .first_or_404(description=f'Alumno con ID {id} no encontrado.')

        fotoUrl = ''

        if 'foto' in request.files:
            file = request.files['foto']
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            fotoUrl = upload_file_to_s3(file_path, aws_bucket)
            setattr(alumno, 'fotoPerfilUrl', fotoUrl)
            db.session.commit()

        return alumno.serialize()

class Profesor(Resource):
    def get(self, id):
        profesor = ProfesorEntity \
            .query \
            .filter_by(id=id) \
            .first_or_404(description=f'Profesor con ID {id} no encontrado.')
        return profesor.serialize()

    def put(self, id):
        args = profesor_parser.parse_args()
        profesor = ProfesorEntity \
            .query \
            .filter_by(id=id) \
            .first_or_404(description=f'Profesor con ID {id} no encontrado.')
        
        for arg in args:
            setattr(profesor, arg, args[arg])
        db.session.commit()
        return profesor.serialize(), 200

    def delete(self, id):
        profesor = ProfesorEntity \
            .query \
            .filter_by(id=id) \
            .first_or_404(description=f'Profesor con ID {id} no encontrado.')
        db.session.delete(profesor)
        db.session.commit()
        return 


class ListaDeProfesores(Resource):
    def get(self):
        profesores = ProfesorEntity.query.all()
        return [profesor.serialize() for profesor in profesores]
    
    def post(self):
        args = profesor_parser.parse_args()
        profesor = ProfesorEntity(
            args['nombres'],
            args['apellidos'],
            args['numeroEmpleado'],
            args['horasClase']
        )
        db.session.add(profesor)
        db.session.commit()
        return profesor.serialize(), 201


api.add_resource(ListaDeAlumnos, '/alumnos')
api.add_resource(Alumno, '/alumnos/<id>')
api.add_resource(FotoDePerfilAlumno, '/alumnos/<id>/fotoPerfil')

api.add_resource(ListaDeProfesores, '/profesores')
api.add_resource(Profesor, '/profesores/<id>')

@app.errorhandler(404)
def not_found(e):
    return { 'message': e }

if __name__ == '__main__':
    app.run(debug=True)