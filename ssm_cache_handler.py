import json
import logging

import spotipy
from botocore.client import BaseClient

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

class SSMCacheHandler(spotipy.CacheHandler):
	def __init__(self, client: BaseClient):
		logger.debug("Initalising cache handler")
		self.client = client
		self.parameter_name = "auto-update-spotify-cache-token"
	
	def get_cached_token(self):
		logger.debug("Trying to get cached token from parameter store")
		response = self.client.get_parameter(
			Name=self.parameter_name,
			WithDecryption=False
		)
		return json.loads(response['Parameter']['Value'])

	def save_token_to_cache(self, token_info):
		logger.debug("Trying to save cached token to parameter store")
		self.client.put_parameter(
			Name=self.parameter_name,
			Value=json.dumps(token_info, ensure_ascii=False),
			Overwrite=True,
			Tier='Standard'
		)
		logger.debug("Saved token to cache")
		return None