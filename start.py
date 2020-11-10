# Works only on linux since ffmpeg code is not cross platform
# not used -  check movie.py
# refer commit e42d20d043695dd8e475da54d18ffffe9e252f5f for more details
import unicodedata
import praw
from praw.models import MoreComments
import urllib.request
from urllib.error import HTTPError
import subprocess
import spotipy
import sys
import os
import spotipy.util as util

from spotipy.oauth2 import SpotifyClientCredentials
import pprint

def getPopularity(elem):
    return int(elem["popularity"])
def redditWriteCommentsToFile(reddit, url="https://www.reddit.com/r/AskReddit/comments/jr8gqt/what_songs_make_you_feel_like_you_could_take_on_a/",  filename="output.txt"):
    print(reddit.read_only)
    submission = reddit.submission(url=url)
    submission.comment_sort = "top"
    submission.comments.replace_more(limit=20)
    with open(filename, 'a') as the_file:
        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, MoreComments):
                continue
            print(top_level_comment.body)
            the_file.write(top_level_comment.body+'\n')

def readFileVal(sp,filename="output.txt"):

    track_ids = []
    with open(filename) as f:
        content = f.readlines()
        for search_str in content:
            result = sp.search(search_str,limit=2,type="track")
            tracks = result["tracks"]["items"]
            tracks.sort(key=getPopularity, reverse=True)
            try:
                track_ids = track_ids + [tracks[0]['id']]
            except IndexError:
                pass
    sp.user_playlist_add_tracks(os.environ["username"],os.environ["playlist_id"],track_ids)

def main():

    scope = 'playlist-modify-public'
    reddit = praw.Reddit(client_id=os.environ["client_id"],
                        client_secret=os.environ["client_secret"],
                        user_agent=os.environ["user_agent"])
    token = util.prompt_for_user_token(
            username=os.environ["username"],
            scope=scope,
            client_id=os.environ["SPOTIPY_CLIENT_ID"],
            client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
            redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"])
    sp = spotipy.Spotify(auth=token)
    redditWriteCommentsToFile(reddit)
    readFileVal(sp)
if __name__ == "__main__":
    main()
