import requests

from config import constants as c

def get_uploads_playlist_id(api_key, channel_id):
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        'key': api_key,
        'id': channel_id,
        'part': 'contentDetails',
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        playlist_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        return playlist_id
    else:
        print(f"Failed to fetch playlist ID. Status code: {response.status_code}")
        return None

def fetch_all_video_ids_from_playlist(api_key, playlist_id):
    youtube_playlist_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    video_ids = []
    next_page_token = ''

    while True:
        params = {
            'key': api_key,
            'playlistId': playlist_id,
            'part': 'contentDetails',
            'maxResults': 50,  # Max allowed by API
            'pageToken': next_page_token
        }

        # Make the API request
        response = requests.get(youtube_playlist_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            for item in data.get('items', []):
                # Append each video ID to the list
                video_ids.append(item['contentDetails']['videoId'])

            # Check if there's a next page
            next_page_token = data.get('nextPageToken')
            if not next_page_token:
                break  # Exit loop if no more pages
        else:
            print(f"Failed to fetch videos. Status code: {response.status_code}")
            break

    return video_ids

uploads_playlist_id = get_uploads_playlist_id(c.YOUTUBE_API_KEY, c.CHANNEL_ID)

if uploads_playlist_id:
    video_ids = fetch_all_video_ids_from_playlist(c.YOUTUBE_API_KEY, uploads_playlist_id)
    print(f"Total videos fetched: {len(video_ids)}")
else:
    print("Could not retrieve the uploads playlist ID.")