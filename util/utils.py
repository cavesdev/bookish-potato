import boto3
import botocore
import os
from botocore.exceptions import ClientError
from botocore.config import Config
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

def upload_file_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(
            file_name, 
            bucket, 
            object_name,
            ExtraArgs={'ACL': 'public-read'}
        )
    except ClientError as e:
        # logging.error(e)
        return ''

    # Get URL
    config = Config(signature_version=botocore.UNSIGNED)
    fotoUrl = boto3.client('s3', config=config) \
    .generate_presigned_url(
        'get_object', 
        ExpiresIn=0, 
        Params={'Bucket': bucket, 'Key': object_name}
    )

    return fotoUrl
