import json

import boto3
import spotipy


class S3CacheHandler(spotipy.CacheHandler):
	def __init__(self):
		print("initalising cache handler")
		self.s3_client = boto3.client('s3')
		self.bucket_name = "kazalo11-spotify-bucket"
		self.cache_key = 'cache-key.json'
	def get_cached_token(self):
		try:
			print("Trying to get cached token from s3 bucket")
			response = self.s3_client.get_object(
				Bucket=self.bucket_name,
				Key=self.cache_key
			)
			return json.loads(response['Body'].read().decode('utf-8'))
		except self.s3_client.exceptions.NoSuchKey:
			return None
		except Exception as e:
			print(f"Error reading from S3: {str(e)}")
			return None
		

	def save_token_to_cache(self, token_info):
		try:
			print("Saving cache to s3 bucket")
			response = self.s3_client.put_object(
				Bucket=self.bucket_name,
				Key=self.cache_key,
				Body=json.dumps(token_info, ensure_ascii=False).encode('utf-8')
			)
			return response['ETag']
		except self.s3_client.exceptions.NoSuchKey:
			return None
		except Exception as e:
			print(f"Error uploading to S3: {str(e)}")
			return None