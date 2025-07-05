import boto3
import logging

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

class DynamoDBHandler:

    def __init__(self, table_name: str):
        self.table = boto3.resource('dynamodb').Table(table_name)

    def check_if_song_exists_in_db(self, song_id: str) -> bool:
        try:
            response = self.table.get_item(Key={'spotify_id': song_id})
            return 'Item' in response
        except Exception as e:
            logging.error(f"Error checking if song exists in DB: {e}")
            raise