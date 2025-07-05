import boto3


class DynamoDBHandler:

    def __init__(self, table_name: str):
        self.table = boto3.resource('dynamodb').Table(table_name)

    def check_if_song_exists_in_db(self, song_id: str) -> bool:
        response = self.table.get_item(Key={'spotify_id': song_id})
        return 'Item' in response