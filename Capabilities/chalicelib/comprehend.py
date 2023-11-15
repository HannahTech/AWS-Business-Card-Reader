import boto3
import re

class Comprehend:
	def __init__(self):
		self.client = boto3.client('comprehend')
		self.website_re = r'\b((https?://)?(www\.)?[A-Za-z0-9.-]+\.[A-Za-z]{2,4}(\.[A-Za-z]{2,4})?/?[^\s]*)\b'
		self.email_re = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
		# self.phone_re = r'(?<!\d)(?:\(\d{3}\)|\d{3})[\s\-._]*(?:\d{3})[\s\-._]*(?:\d{4})(?!\d)'
		self.phone_re = r'\b\w*\s*\(?(\d{1,3})\)?[-.\s]*\d{3,4}[-.\s]*\d{4}\b'

	def custom_batch_detect_entities(self, lines):
		response = self.client.batch_detect_entities(TextList=lines, LanguageCode='en')

		result_list = response['ResultList']

		data = {'name': [], 'phone': [], 'email': [], 'website': [], 'address': [], 'other': []}

		for i in range(len(lines)):
			line = lines[i]
			entities = result_list[i]['Entities']
			dic = {'UNKNOWN': 0}
			max = 'UNKNOWN'
			for entity in entities:
				try:
					dic[entity['Type']] += entity['Score']
				except:
					dic[entity['Type']] = entity['Score']

				max = max if dic[max] >= dic[entity['Type']] else entity['Type']

			if max == 'PERSON':
				data['name'].append(line.lower())
			elif max == 'LOCATION':
				data['address'].append(line)
			elif re.findall(self.email_re, line):
				data['email'].append(line)
			elif re.findall(self.website_re, line):
				data['website'].append(line)
			elif re.findall(self.phone_re, line):
				data['phone'].append(line)
			else:
				data['other'].append(line)

		return data
