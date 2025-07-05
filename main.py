import logging
import os
from datetime import date, datetime
from http import HTTPStatus

import boto3
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from dynamo_db_handler import DynamoDBHandler
from ssm_cache_handler import SSMCacheHandler

now = date.today()
formatted_date = now.strftime("%b %y")


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

def check_date(item):
	return item['name'] == formatted_date

def is_same_month(date_str: str) -> bool:
	track_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
	return track_date.month == now.month and track_date.year == now.year

def main():
	logger.info("Starting up")
	scope = ["user-library-read", "playlist-modify-public", "playlist-modify-private"]
	client_id = os.getenv("SPOTIFY_ID")
	client_secret = os.getenv("SPOTIFY_SECRET")
	redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
	client = boto3.client("ssm")
	try:
		logger.info("Attempting to initialize Spotify client...")
		auth_manager = SpotifyOAuth(
		scope=scope,
		client_id=client_id,
		client_secret=client_secret,
		redirect_uri=redirect_uri,
		cache_handler=SSMCacheHandler(client)
		)
		sp = spotipy.Spotify(auth_manager=auth_manager)
		backfill_songs_table = DynamoDBHandler('backfilled_songs')
		logger.info("spotipy setup initalised")
	except spotipy.SpotifyOAuthError as auth_error:
		logger.error(f"Authentication error: {str(auth_error)}")
		raise
	except Exception as e:
		logger.error(f"Unexpected error during Spotify initialization: {str(e)}")
		logger.error(f"Error type: {type(e)}")
		raise

	logger.info("Checking spotify for latest tracks")
	latest_tracks = sp.current_user_saved_tracks(20)['items']
	current_playlists = sp.current_user_playlists(50)['items']
	if not current_playlists:
		logger.info("No playlists found")
		return "No playlist found"
		
	existing_playlist = list(filter(check_date, current_playlists))
	if existing_playlist:
		logger.info("Found playlist for this month")
		playlist_id = existing_playlist[0]['id']
	else:
		logger.info("Creating a new playlist")
		info = sp.user_playlist_create("18tta2lvd65imwx89d7mqr2sv",formatted_date)
		playlist_id = info['id']


	playlist = sp.playlist(playlist_id=playlist_id, fields='tracks.items(track(id))')
	playlist_tracks = playlist['tracks']['items']
	track_ids = [item['track']['id'] for item in playlist_tracks]
	for latest_track in latest_tracks:
		track_id = latest_track['track']['id']
		added_at = latest_track["added_at"]
		track_name = latest_track['track']['name']
		logger.debug(f"Checking if track {track_name} is present in this month's playlist")
		if track_id in track_ids:
			logger.debug("Track already found, no need to add again")
		elif not is_same_month(added_at):
			logger.debug("Track was added at a different month")
		else:
			sp.playlist_add_items(playlist_id, [f'spotify:track:{track_id}'])
			logger.info(f"Added track {track_name} to the playlist")
	return "Successfully updated"

def lambda_handler(event, context):
    """
    AWS Lambda handler function
    """
    try:
        main()
        return {
            'statusCode': HTTPStatus.OK,
            'body': "Successfully updated"
        }
    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': str(e)
        }


if __name__ == "__main__":
    main()