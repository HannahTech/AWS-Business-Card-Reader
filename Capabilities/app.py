from chalice import Chalice
from chalicelib import rekognition, comprehend, dynamodb

from base64 import b64decode
from urllib.parse import unquote

#####
# chalice app configuration
#####
app = Chalice(app_name='cml proj')
app.debug = True

#####
# services initialization
#####
rekognition = rekognition.Rekognition()
comprehend = comprehend.Comprehend()
dynamodb = dynamodb.DynamoDB()

#####
# RESTful endpoints
#####
@app.route('/extract', methods=['POST'], cors=True)
def extract():
	data = app.current_request.json_body
	encoded_image = data['filebytes']
	image_bytes = b64decode(encoded_image)

	lines = rekognition.extract_lines(image_bytes)
	data = comprehend.custom_batch_detect_entities(lines)

	return {'data': data}

@app.route('/create', methods=['POST'], cors=True)
def create():
	data = app.current_request.json_body

	status = dynamodb.create(data)

	return {'status': status}

@app.route('/read/{name}', methods=['GET'], cors=True)
def read(name):
	items = dynamodb.read(unquote(name))

	return items
