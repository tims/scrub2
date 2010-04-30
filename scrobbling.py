import urllib, urllib2
from urllib2 import HTTPError
import hashlib
from BeautifulSoup import BeautifulStoneSoup
import webbrowser
import time
import yaml
import sys

class Scrobble(object):
    def __init__(self, **kwargs):
        self.timestamp=kwargs.get('timestamp')
        self.artist=kwargs.get('artist')
        self.album=kwargs.get('album')
        self.track=kwargs.get('track')
        self.albumArtist=kwargs.get('albumArtist')
        self.duration=kwargs.get('duration')
        self.mbid=kwargs.get('mbid')
        self.streamId=kwargs.get('streamId')
        self.streamAuth=kwargs.get('streamAuth')
        self.context=kwargs.get('context')
        self.contextUrl=kwargs.get('contextUrl')

class NowPlaying(object):
    def __init__(self, **kwargs):
        self.timestamp=kwargs.get('timestamp')
        self.artist=kwargs.get('artist')
        self.album=kwargs.get('album')
        self.track=kwargs.get('track')
        self.albumArtist=kwargs.get('albumArtist')
        self.duration=kwargs.get('duration')
        self.mbid=kwargs.get('mbid')
        self.context=kwargs.get('context')
        self.contextUrl=kwargs.get('contextUrl')

class ScrobblingAPI(object):
    def __init__(self):
        self.configFile = 'config.yaml'
        self.authUrl = 'http://www.last.fm/api/auth/'
        self.webServicesUrl = 'http://ws.audioscrobbler.com/2.0/'
        self.scrobblingUrl = 'http://post.audioscrobbler.com/2.0/'
        self.apiKey, self.apiSecret, self.sessionKey = self.loadConfig(self.configFile)
        if not self.sessionKey:
            self.sessionKey = self.createNewSession()
        self.saveConfig(self.configFile)

    def md5(self, word):
        md5 = hashlib.md5()
        md5.update(word)
        return md5.hexdigest()

    def getRequest(self, url, params):
        items = params.items()
        items.sort()
        url = url + '?' + urllib.urlencode(items)
        request = urllib2.Request(url)
        print "Sending request to " + url
        try:
            response = urllib2.urlopen(request)
        except HTTPError, e:
            soup = BeautifulStoneSoup(e)
            raise Exception('Webservice call not ok. Got:\n' + str(soup))
        soup = BeautifulStoneSoup(response)
        return soup

    def postRequest(self, url, params):
        items = params.items()
        items.sort()
        data = urllib.urlencode(items)
        request = urllib2.Request(url, data)
        print "Sending request to " + url + " with data " + data
        try:
            response = urllib2.urlopen(request)
        except HTTPError, e:
            soup = BeautifulStoneSoup(e)
            raise Exception('Webservice call not ok. Got:\n' + str(soup))
        soup = BeautifulStoneSoup(response)
        return soup

    def sign(self, params):
        items = params.items()
        items.sort()
        methodSig = ''
        for k,v in items:
            methodSig += k + v
        return self.md5(methodSig + self.apiSecret)

    def loadConfig(self, configFile):
        print "Loading api config file " + configFile
        config = {}
        try:
            f = open(configFile, 'r')
            config = yaml.load(f)
            f.close()
        except:
            raise Exception("Couldn't open config.yaml")
        apiKey = config.get('apiKey')
        apiSecret = config.get('apiSecret')
        sessionKey = config.get('sessionKey')
        return apiKey, apiSecret, sessionKey

    def saveConfig(self, configFile):
        config = self.__dict__
        if not config.get('apiKey'):
            print "Api key missing, not saving config."
            return
        if not config.get('apiSecret'):
            print "Api secret missing, not saving config."
            return
        if not config.get('sessionKey'):
            print "Session key missing, not saving config."
            return
        print "Saving api config file " + configFile
        f = open(configFile,'w')
        yaml.dump(config, f)
        f.close()

    def createNewSession(self):
        print "Getting auth token..."
        method = 'auth.getToken'
        params = {'method': method, 'api_key': self.apiKey}
        response = self.getRequest(self.webServicesUrl, params)
        token = response.token.string
        print "Received token: " + token
        print "Asking for user permission..."
        webbrowser.open(self.authUrl + "?api_key=" + self.apiKey + "&token=" + token)
        time.sleep(2)
        raw_input("\nPress enter when done:")

        print "Getting session key..."
        method = 'auth.getSession'
        params = {'method':method, 'token':token, 'api_key': self.apiKey}
        params['api_sig'] = self.sign(params)
        response = self.getRequest(self.webServicesUrl, params)
        sessionKey = str(response.session.key.string)
        print "Received session key: " + sessionKey
        return sessionKey

    def updateNowPlaying(self, nowPlaying):
        params = dict((k, v) for (k, v) in nowPlaying.__dict__.iteritems() if not v is None)
        params['method'] = 'User.updateNowPlaying'
        params['api_key'] = self.apiKey
        params['sk'] = self.sessionKey
        params['api_sig'] = self.sign(params)
        print params
        response = self.postRequest(self.scrobblingUrl, params)
        # check for artist corrections
        artist = response.lfm.artist.string
        track = response.lfm.track.string
        if artist != nowPlaying.artist:
            print "Artist correction returned: " + nowPlaying.artist + " -> " + artist
        if track != nowPlaying.track:
            print "Track correction returned: " + nowPlaying.track + " -> " + track


    def scrobble(self, scrobble):
        params = dict((k, v) for (k, v) in scrobble.__dict__.iteritems() if not v is None)
        params['method'] = 'Track.scrobble'
        params['api_key'] = self.apiKey
        params['sk'] = self.sessionKey
        params['api_sig'] = self.sign(params)
        print params
        return self.postRequest(self.scrobblingUrl, params)

    def scrobbleBatch(self, scrobbles):
        params = {}
        i = 1
        for scrobble in scrobbles:
            params.update(dict(("%s[%s]" % (k,i), v) for (k, v) in scrobble.__dict__.iteritems() if not v is None))
            i += 1
        params['method'] = 'Track.scrobbleBatch'
        params['api_key'] = self.apiKey
        params['sk'] = self.sessionKey
        params['api_sig'] = self.sign(params)
        print params
        return self.postRequest(self.scrobblingUrl, params)

if __name__ == '__main__':
    api = ScrobblingAPI()
    time.sleep(1)
    #send a now playing update
    np = NowPlaying(artist="Test Artist", track="Test Track", timestamp=str(int(time.time())))
    api.updateNowPlaying(np)
    time.sleep(1)
    #send a single scrobble
    s = Scrobble(artist="Test Artist", track="Test Track", timestamp=str(int(time.time())))
    api.scrobble(s)
    time.sleep(1)
    #send a batch of scrobbles
    s0 = Scrobble(artist="Test Artist 0", track="Test Track 0", timestamp=str(int(time.time())))
    s1 = Scrobble(artist="Test Artist 1", track="Test Track 1", timestamp=str(int(time.time())))
    api.scrobbleBatch([s0,s1])

