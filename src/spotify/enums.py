from enum import StrEnum


class ContentType(StrEnum):
    none = ''
    Track = 'track'
    Artist = 'artist'
    Album = 'album'
    Playlist = 'playlist'
    User = 'user'
    Podcast = 'podcast'
    PodcastEpisode = 'podcast_episode'

