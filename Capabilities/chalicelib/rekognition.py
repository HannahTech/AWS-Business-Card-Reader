import boto3

class Rekognition:
	def __init__(self):
		self.client = boto3.client('rekognition')

	def extract_lines(self, image_bytes):
		response = self.client.detect_text(Image={'Bytes': image_bytes})
		text_detections = response['TextDetections']

		return [item['DetectedText'] for item in text_detections if item['Type']=='LINE']
