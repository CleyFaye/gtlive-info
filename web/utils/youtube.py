"""Youtube helper functions"""
import re
from requests import get
import urllib.parse
import urllib.request
import simplejson
from django.conf import settings
from django.core.files.base import ContentFile

API_ENDPOINT = 'https://www.googleapis.com/youtube/v3'
DURATION_RE = re.compile(r'PT(?:(?P<hour>\d+)H)?(?:(?P<minute>\d+)M)?'
                         + r'(?:(?P<second>\d+)S)?')


def getAPIEntryPoint(function):
    return API_ENDPOINT + '/' + function


def buildQuery(baseURL, arguments):
    """Create a query URL.

    arguments is a dictionary with key:value. If value is an array, the key is
    repeated.
    """
    queryArguments = []
    for key in arguments:
        value = arguments[key]
        quotedKey = urllib.parse.quote(key, safe='')
        if isinstance(value, list):
            for valueElement in value:
                queryArguments.append('%s=%s'
                                      % (quotedKey,
                                         urllib.parse.quote(valueElement,
                                                            safe='')))
        else:
            queryArguments.append('%s=%s'
                                  % (quotedKey,
                                     urllib.parse.quote(value, safe='')))
    if queryArguments:
        return '%s?%s' % (baseURL, '&'.join(queryArguments))
    return baseURL


def convertDurationToMinutes(youtube_duration):
    res = DURATION_RE.search(youtube_duration)
    if res['hour']:
        hour = int(res['hour'])
    else:
        hour = 0
    if res['minute']:
        minute = int(res['minute'])
    else:
        minute = 0
    return minute + hour * 60


def getSingleVideoResult(videoId):
    try:
        url = getAPIEntryPoint('videos')
        arguments = {'part': 'snippet,contentDetails',
                     'id': str(videoId),
                     'key': settings.YOUTUBE_KEY}
        query = buildQuery(url, arguments)
        json = simplejson.load(urllib.request.urlopen(query))
        for item in json['items']:
            snippet = item['snippet']
            resultElement = {'title': snippet['title']}
            try:
                resultElement['thumbnail'] = (
                    snippet['thumbnails']['high']['url'])
            except KeyError:
                resultElement['thumbnail'] = None
            try:
                resultElement['duration'] = convertDurationToMinutes(
                    item['contentDetails']['duration'])
            except KeyError:
                resultElement['duration'] = None
            return resultElement
    except Exception:
        pass
    return None


def getThumbnailData(thumbnailURL):
    if thumbnailURL is None:
        return None
    try:
        response = get(thumbnailURL)
        return ContentFile(response.content)
    except Exception:
        return None
