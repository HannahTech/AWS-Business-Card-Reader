import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr


import uuid

class DynamoDB:
	def __init__(self, region_name='ca-central-1', table='Card'):
		self.resource = boto3.resource('dynamodb', region_name=region_name)
		self.table = self.resource.Table(table)

	def create(self, item):
		try:
			item["card_id"] = str(uuid.uuid4())
			self.table.put_item(Item=item)
			return True
		except:
			return False

	def read(self, name):
		# response = self.table.query(
		#     IndexName='name-index',
		#     KeyConditionExpression=Key('name').eq(name)
		# )

		response = self.table.scan(
		    # FilterExpression=Attr('name').contains(name)
		    FilterExpression=Attr('name').contains(name.lower())
		)

		for item in response['Items']:
			for field in item:
				if not isinstance(item[field], list):
					item[field] = [item[field]]
			for field in ["name", "phone", "email", "website", "address", "other"]:
				if field not in item:
					item[field] = []

		return response['Items']
