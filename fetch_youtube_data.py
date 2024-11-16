import json
import os
import logging
import re
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)

load_dotenv()  # Load environment variables from .env file

# Client credentials
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# YouTube playlist details
PLAYLIST_ID = "PL5ErBr2d3QJH0kbwTQ7HSuzvBb4zIWzhy"

def fetch_youtube_playlist_data(api_key, playlist_id):
    youtube = build("youtube", "v3", developerKey=api_key)
    videos = []
    next_page_token = None

    while True:
        playlist_request = youtube.playlistItems().list(
            part="snippet,contentDetails", playlistId=playlist_id, maxResults=10, pageToken=next_page_token
        )
        playlist_response = playlist_request.execute()

        if "items" not in playlist_response or not playlist_response["items"]:
            logging.error("No items found in the playlist response.")
            break

        for item in playlist_response["items"]:
            video_id = item["contentDetails"]["videoId"]

            # Fetch additional video details including duration, likes, views, and comments
            video_request = youtube.videos().list(
                part="contentDetails,statistics",
                id=video_id
            )
            video_response = video_request.execute()

            if "items" not in video_response or not video_response["items"]:
                logging.error(f"No video details found for video ID: {video_id}")
                continue

            video_details = video_response["items"][0]
            duration = convert_duration(video_details["contentDetails"]["duration"])
            likes = int(video_details["statistics"].get("likeCount", 0))
            views = int(video_details["statistics"].get("viewCount", 0))
            comments = int(video_details["statistics"].get("commentCount", 0))

            title = item["snippet"]["title"]
            description = item["snippet"]["description"].strip() or "No description available"
            publishedAt = item["snippet"]["publishedAt"]
            position = item["snippet"].get("position", None)
            thumbnails = item["snippet"]["thumbnails"]
            channel_title = item["snippet"]["channelTitle"]
            channel_id = item["snippet"]["channelId"]

            # Map to the blueprint structure for YouTube video
            videos.append({
                "identifier": video_id,
                "blueprint": "youtube_video",
                "title": title,
                "properties": {
                    "link": f"https://www.youtube.com/watch?v={video_id}",
                    "videoDescription": description,
                    "duration": duration,
                    "publishedAt": publishedAt,
                    "position": position,
                    "likes": likes,
                    "views": views,
                    "comments": comments,
                    "thumbnails": {
                        "default": thumbnails["default"]["url"],
                        "medium": thumbnails["medium"]["url"],
                        "high": thumbnails["high"]["url"],
                        "standard": thumbnails.get("standard", {}).get("url", ""),
                        "maxres": thumbnails.get("maxres", {}).get("url", "")
                    },
                    "videoOwnerChannelTitle": channel_title,
                    "videoOwnerChannelId": channel_id
                },
                "relations": {
                    "playlist": playlist_id
                }
            })

        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break

    return videos

def fetch_youtube_playlist_info(api_key, playlist_id):
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        id=playlist_id
    )
    response = request.execute()

    if "items" not in response or not response["items"]:
        logging.error("No items found in the playlist info response.")
        return None

    item = response["items"][0]
    
    # Fallback for missing or empty fields
    playlist_description = item["snippet"].get("description", "").strip() or "No description available"
    published_at = item["snippet"].get("publishedAt", "")
    channel_id = item["snippet"].get("channelId", "No channel ID")
    channel_title = item["snippet"].get("channelTitle", "No channel title")
    thumbnails = item["snippet"].get("thumbnails", {})
    playlist_link = f"https://www.youtube.com/playlist?list={playlist_id}"

    # Handling localized title and description
    localized_title = item["snippet"].get("localized", {}).get("title", "No Localized Title")
    localized_description = item["snippet"].get("localized", {}).get("description", "").strip() or "No Localized Description"

    # Map to the blueprint structure for YouTube playlist
    return {
        "identifier": playlist_id,
        "blueprint": "youtube_playlist",
        "title": item["snippet"].get("title", "No Title"),
        "properties": {
            "link": playlist_link,
            "playlistDescription": playlist_description,
            "publishedAt": published_at,
            "channelId": channel_id,
            "channelTitle": channel_title,
            "thumbnails": {
                "default": thumbnails.get("default", {}).get("url", ""),
                "medium": thumbnails.get("medium", {}).get("url", ""),
                "high": thumbnails.get("high", {}).get("url", ""),
                "standard": thumbnails.get("standard", {}).get("url", "")
            },
            "localized": {
                "title": localized_title,
                "description": localized_description
            }
        }
    }

def convert_duration(duration):
    match = re.match(r'PT((?P<hours>\d+)H)?((?P<minutes>\d+)M)?((?P<seconds>\d+)S)?', duration)
    if not match:
        return "0:00"

    hours = int(match.group('hours') or 0)
    minutes = int(match.group('minutes') or 0)
    seconds = int(match.group('seconds') or 0)

    # Format the duration as "H:MM:SS" or "MM:SS" if no hours are present
    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes}:{seconds:02}"

def main():
    # Fetch the playlist and video data
    playlist_data = fetch_youtube_playlist_info(YOUTUBE_API_KEY, PLAYLIST_ID)
    if playlist_data is None:
        logging.error("Failed to fetch playlist data. Exiting.")
        return

    videos_data = fetch_youtube_playlist_data(YOUTUBE_API_KEY, PLAYLIST_ID)
    
    # Combine Playlist and Video data for BULK_UPSERT
    all_data = [playlist_data] + videos_data
    with open("port_entities.json", "w") as f:
        json.dump(all_data, f, indent=4)
    logging.info("Fetched YouTube data and saved to port_entities.json")

if __name__ == "__main__":
    main()