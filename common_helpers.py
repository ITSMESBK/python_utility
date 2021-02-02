# =========================================================================================
# !/usr/bin/env python3
# Filename: common_helpers.py
# Description: Re-usable functions/methods
# Author: Bharathkumar Sivakumar <BHARATH SBK @ITSMESBK>
# Python Environment - Python3
# Usage: To be used as a helper functionality to support for all the other modules / scripts 
# ===========================================================================================

#PACKAGES

from collections import defaultdict
import requests
import boto3
import logging
import re

# IN HOUSE PACKAGES 

from constants import *
from config import *

class helper_module():
	
	#FETCH CREDINTIALS 
	def get_credentials(self,aws_keys=None):
		'''
		Get credentials details from the json
		:return: credentials

		'''
		try:
			with open(CREDENTIALS_INFO, 'r') as fp:
				credentials = json.load(fp)
		except:
			logging.error("Issue in get credentials")

		return credentials

	#UPLOAD DATA TO S3 BUCKET
	def upload_s3(self,args):
		"""
		Upload Objects to S3 buckets to a particular bucket using botoi, Uploads as
		a public URL
		:param args: contains filename, s3_filename, bucket, region
		:return:
		"""
		logging.info("Uploading file `{}` in s3 bucket: `{}`".format(
			args[1], args[2]))
		credentials = get_credentials()
		AWS_ACCESS_KEY_ID = credentials.get('AWS_ACCESS_KEY_ID')
		AWS_ACCESS_KEY_SECRET = credentials.get('AWS_ACCESS_KEY_SECRET')
		credentials = {
			'aws_access_key_id': AWS_ACCESS_KEY_ID,
			'aws_secret_access_key': AWS_ACCESS_KEY_SECRET
		}

		if len(args) > 0 and len(args) < 4:
			filename = args[0]
			s3_filename = args[1]
			s3_bucket = args[2]

		if len(args) == 4:
			filename = args[0]
			s3_filename = args[1]
			s3_bucket = args[2]

			region = args[3]
		else:
			region = 'ap-southeast-1'
		try:
			s3 = get_service('s3')
			client = boto3.client('s3', region, **credentials)
			transfer = S3Transfer(client)
			# bucket = s3.Bucket("testbank-nc")
			# bucket.upload_file("C:\Users\henin\Downloads\captcha-600.png", "captcha2.png")
			transfer.upload_file(
				filename,
				s3_bucket,
				s3_filename,
				extra_args={'ACL': 'public-read'})
		except :
			logging.error("Issue in uploading data in s3")
		# except botocore.exceptions.EndpointConnectionError as error:
		#     logger.error(error)

	def get_s3_file(self,s3, bucket_name, filename):
		"""
		Get s3 object
		:param s3:
		:param bucket_name:
		:param filename:
		:return: S3 obj
		"""
		try:
			obj = s3.Object(bucket_name, filename)
		except:
			logging.error("Error In fetch data")
		return obj

	def delete_bucket_s3(self,client, bucket_name, region):
		"""
		Delete a specific bucket
		:param client:
		:param bucket_name:
		:param region:
		:return:
		"""
		try:
			response = client.delete_bucket(Bucket=bucket_name)
		except:
			logging.error("Error in deletion")

		return response

	def delete_s3_objects(self,bucket_name, region, objects):
		"""
		Deletes a specific or list of objects
		:param client:
		:param bucket_name:
		:param region:
		:return:
		"""
		client = get_service('s3', 'client')
		try:
			if isinstance(objects, list):
				response = client.delete_objects(
					Delete={
						'Objects': [
							{
								'Key': objects,
								'VersionId': 'string'
							},
						],
						'Quiet': True | False
					},
					MFA='string',
					RequestPayer='requester')
			else:
				client.delete_object(Bucket=bucket_name, Key=objects)
			logging.info("Deleted `{}` object from {}".format(objects, bucket_name))
		except Exception as error:
			logging.error("Error in deletion")

	def list_buckets_s3(self,client, bucket_name, region):
		"""
		List buckets
		:param s3:
		:param bucket_name:
		:param region:
		:return:
		"""
		response = client.list_buckets()
		return

	def create_bucket_s3(self,s3, bucket_name, region):
		"""
		Create Bucket in s3
		:param s3:
		:param bucket_name:
		:param region:
		:return: response
		"""
		try:
			response = s3.create_bucket(
				ACL='private' | 'public-read' | 'public-read-write'
					| 'authenticated-read',
				Bucket=bucket_name,
				CreateBucketConfiguration={
					'LocationConstraint':
						'EU' | 'eu-west-1' | 'us-west-1' | 'us-west-2' | 'ap-south-1'
						| 'ap-southeast-1' | 'ap-southeast-2' | 'ap-northeast-1'
						| 'sa-east-1' | 'cn-north-1' | 'eu-central-1'
				},
				GrantFullControl='string',
				GrantRead='string',
				GrantReadACP='string',
				GrantWrite='string',
				GrantWriteACP='string')
			return response
		except Exception as error:
			logging.error("Error in bucket creation")
			
	#GET NAMED ENTITIES 
	def predict_named_entities(self,listofnames, entities=None):
		# Create a Default dict
		names_entity = defaultdict(list)
		for name in listofnames:
			try:
				# Api Approcach
				#url = "https://demo.allennlp.org/predict/named-entity-recognition"
				
				url = "https://demo.allennlp.org/api/fine-grained-ner/predict"
				
				# defining a params dict for the parameters to be sent to the API
				payload = {"sentence": name}
				
				# sending get request and saving the response as response object
				try:
					post_response = requests.post(url=url, json=payload)

				except:
					time.sleep(1)
					post_response = requests.post(url=url, json=payload)

				if post_response.status_code != 200:
					print("Unable to hit ALLEN NLP API!!!!")
					exit(1)

				results = post_response.json()
				tags = results["tags"]
				words = results["words"]
				
				if results:
					for word, tag in zip(results["words"], results["tags"]):
						try:
							word = word.strip()
							if tag == 'O':
								tag = 'OTHERS' 
							names_entity[tag].append(word)
						except:
							continue
				else:
					continue
			except:
				continue

			if entities:
				requested_entities = {}

				for entity in entities:
					requested_entities[entity] = names_entity[entity]
			else:
				dict(names_entity)

		return dict(names_entity)

		#sample list of names added in a list
		listofnames = ["JOHN","TRUMP","INDIA","UNITED STATES","GOOGLE"]
		get_prediction = predict_named_entities(listofnames, entities=None)
		print(get_prediction)
		return get_prediction

	#GET PROPER DATA FROM A FILE 
	def entity_data_clean(self,filename):
		per_tag = []
		list_names = []
		pan_card = []
		try:
			names_entity = defaultdict(list)
			listofnames = []
			with open(filename, 'r') as filehandle:
				# Data cleaning
				for line in filehandle:
					file = line.replace(',', ' ')
					file = file.split()
					for each_word in file:
						data = re.sub(r'\w*\d\w*', '', each_word).strip()
						data = re.sub('[^A-Za-z\b\t\n,' '\0+ ]+', '', data)
						# remove the special characters and words with special characters
						data = re.sub(r'\W+', "1", data)
						if not data.startswith("1"):
							data = data.title()
							data_dup = re.findall(r'((\w)\2{2,})', data)
							if data_dup == []:
								listofnames.append(data)
				return listofnames
		except:
			logging.error("something went wrong onn cleaning")

	#GET DATA WITHOUT SPECIAL CHARACTERS AND DIGITS 
	def remove_special_chars_digits(self,list_items):
		for ind, item in enumerate(list_items):
			try:
				item = re.sub(",", "", item)
				try:
					count_decimal = item.count('.')
					if count_decimal > 1:
						item = re.findall("\d+\.\d+", item)
						if item:
							item = item[0]
				except:
					continue
				# @TODO: Remove list of special digits, or conversions : Ex:  zero
				# to 0, or 5 to S
				if item:
					loc_last_decimal = item.rfind('.')
					if loc_last_decimal != -1:
						list_items[ind] = item[:loc_last_decimal].replace(
							'.', '') + item[loc_last_decimal:]
					else:
						list_items[ind] = item
				else:
					continue
			except :
				continue
		return list_items

	#SEARCH ALGORITHMS USING FOR EFFECTIVE AND OPTIMIZED SEARCH
	
	#LINEAR SEARCH IN OPTIMAL WAY
	'''
	O(n)
	'''
	def get_linearSearch(self,list_items, element):
		def ls_mapper(iter_val):
			if list_items[iter_val] == element:
				return iter_val   
		output_val = list(map(ls_mapper,range(len(list_items))))
		if None in output_val:
			output_val = list(filter(None, output_val)) 
		return output_val  

	#SEARCH NUMBERS
	'''
	log2(n)

	length of the array is 'n' 
	
	Iterarion based steps :

	step 01 :
	len_array = n
	
	step 02 :
	len_array = n/2 
	
	step 03 :
	len_array = n/2 /2 = n/2**2

	step 04 :
	n/2 k = 1
	apply log on both sides
	log2(n) = k log2 (2)  
	''' 
	def get_binarySearch(self,list_items, val):
		first = 0
		last = len(list_items)-1
		index = -1
		while (first <= last) and (index == -1):
			mid = (first+last)//2
			if list_items[mid] == val:
				index = mid
			else:
				if val<list_items[mid]:
					last = mid -1
				else:
					first = mid +1
		return index    
