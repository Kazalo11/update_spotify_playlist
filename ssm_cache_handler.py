import json

import boto3
import spotipy


class SSMCacheHandler(spotipy.CacheHandler):
	def __init__(self):
		print("Initalising cache handler")
		self.client = boto3.client("ssm")
		self.parameter_name = "auto-update-spotify-cache-token"
	
	def get_cached_token(self):
		print("Trying to get cached token from parameter store")
		response = self.client.get_parameter(
			Name=self.parameter_name,
			WithDecryption=False
		)
		return json.loads(response['Parameter']['Value'])

	def save_token_to_cache(self, token_info):
		print("Trying to save cached token to parameter store")
		self.client.put_parameter(
			Name=self.parameter_name,
			Value=json.dumps(token_info, ensure_ascii=False),
			Overwrite=True,
			Tier='Standard'
		)