import os
from datetime import date, datetime

import spotipy
from spotipy.oauth2 import SpotifyOAuth


def main():
	print("Checking spotify for latest saved tracks")
	scope = ["user-library-read", "playlist-modify-public", "playlist-modify-private"]
	client_id = os.getenv("SPOTIFY_ID")
	client_secret = os.getenv("SPOTIFY_SECRET")
	redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))
	latest_tracks = sp.current_user_saved_tracks(20)['items']
	current_playlists = sp.current_user_playlists(12)['items']
	now = date.today()
	formatted_date = now.strftime("%b %y")
	def checkDate(item):
		return item['name'] == formatted_date
	def is_same_month(date_str: str) -> bool:
		track_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
		return track_date.month == now.month and track_date.year == now.year
	existing_playlist = list(filter(checkDate, current_playlists))
	if existing_playlist != []:
		print("Found playlist for this month")
		playlist_id = existing_playlist[0]['id']
	else:
		print("Creating a new playlist")
		info = sp.user_playlist_create("18tta2lvd65imwx89d7mqr2sv",formatted_date)
		playlist_id = info['id']
	
	playlist = sp.playlist(playlist_id=playlist_id, fields='tracks.items(track(id))')
	playlist_tracks = playlist['tracks']['items']
	track_ids = [item['track']['id'] for item in playlist_tracks]
	for latest_track in latest_tracks:
		track_id = latest_track['track']['id']
		added_at = latest_track["added_at"]
		if track_id in track_ids:
			print("Track already found, no need to add again")
		elif not is_same_month(added_at):
			print("Track was added at a different month")
		else:
			sp.playlist_add_items(playlist_id, [f'spotify:track:{track_id}'])
			print(f"Added track ${track_id} to the playlist")
	return "Successfully updated"

def lambda_handler(event, context):
    """
    AWS Lambda handler function
    """
    try:
        result = main()
        return {
            'statusCode': 200,
            'body': result
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

if __name__ == "__main__":
    main()