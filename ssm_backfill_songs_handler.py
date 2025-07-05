import json
import logging

from botocore.client import BaseClient

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

class SSMBackfillSongsHandler:
    def __init__(self, client: BaseClient):
        self.client = client
        self.parameter_name = "auto-update-spotify-backfill-songs-id"

    def get_backfill_songs(self) -> list[str]:
        logger.debug("Getting backfill songs from SSM")
        try:
            response = self.client.get_parameter(
                Name=self.parameter_name,
                WithDecryption=False
            )
            logger.debug(response)
            values = response['Parameter']['Value']
            logger.debug("Obtained values from SSM")
            return values.split(",")
        except Exception as e:
            logger.error(f"Error while getting songs from SSM: {e}")
            raise

    def set_backfill_songs(self, songs: list[str]):
        logger.debug("Setting backfill songs from SSM")
        string_songs = ','.join(songs)
        self.client.put_parameter(
            Name=self.parameter_name,
            Tier="Standard",
            Overwrite=True,
            Value=json.dumps(string_songs, ensure_ascii=False)
        )
        logger.debug("Saved backfill songs to SSM")
        return None