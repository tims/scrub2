#-*- coding: utf-8 -*-
from scrobbling import *
import unittest
import xmlrunner
import time
from BeautifulSoup import BeautifulStoneSoup

class ScrobbleTestCase(unittest.TestCase):
    def setUp(self):
        self.client = ScrobblingClient()

    def testNowPlaying(self):
        resp = self.client.updateNowPlaying(NowPlaying(artist="Test Artist",track="Test Track"))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0

    def testNowPlayingFilteredArtist(self):
        resp = self.client.updateNowPlaying(NowPlaying(artist="Unknown Artist",track="Test Track"))
        assert int(resp.scrobbles['accepted']) == 0
        assert int(resp.scrobbles['ignored']) == 1
        assert int(resp.scrobbles.scrobble.ignoredmessage['code']) == 1

    def testNowPlayingFilteredTrack(self):
        resp = self.client.updateNowPlaying(NowPlaying(artist="Test Artist",track="Track 1"))
        assert int(resp.scrobbles['accepted']) == 0
        assert int(resp.scrobbles['ignored']) == 1
        assert int(resp.scrobbles.scrobble.ignoredmessage['code']) == 2

    def testNowPlayingAcceptedArtistSet(self):
        resp = self.client.updateNowPlaying(NowPlaying(artist="Test Artist",track="Test Track"))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.artist.contents[0] == u"Test Artist"

    def testNowPlayingAcceptedTrackSet(self):
        resp = self.client.updateNowPlaying(NowPlaying(artist="Test Artist",track="Test Track"))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.track.contents[0] == u"Test Track"

    def testNowPlayingAcceptedAlbumSet(self):
        resp = self.client.updateNowPlaying(NowPlaying(artist="Test Artist", track="Test Track", album="Test Album"))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.album.contents[0] == u"Test Album"

    def testNowPlayingAcceptedAlbumArtistSet(self):
        resp = self.client.updateNowPlaying(NowPlaying(artist="Test Artist", track="Test Track", albumArtist="Test Album Artist"))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.albumartist.contents[0] == u"Test Album Artist"

    def testNowPlayingInvalidParameterArtistMissing(self):
        try:
            resp = self.client.updateNowPlaying(NowPlaying(track="Test Track"))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testNowPlayingInvalidParameterArtistEmpty(self):
        timestamp=str(int(time.time()))
        try:
            resp = self.client.updateNowPlaying(NowPlaying(artist="", track="Test Track"))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testNowPlayingInvalidParameterTrackMissing(self):
        timestamp=str(int(time.time()))
        try:
            resp = self.client.updateNowPlaying(NowPlaying(artist="Test Artist"))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testNowPlayingInvalidParameterTrackEmpty(self):
        timestamp=str(int(time.time()))
        try:
            resp = self.client.updateNowPlaying(NowPlaying(artist="Test Artist", track=""))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testNowPlayingAcceptedCorrectedArtist(self):
        resp = self.client.updateNowPlaying(NowPlaying(artist="Bjork", track="Jóga", albumArtist="Test Album Artist"))
        print resp.prettify()
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.artist.contents[0] == u"Björk"
        assert resp.scrobbles.scrobble['corrected'] == "1"

    def testNowPlayingAcceptedCorrectedArtist(self):
        resp = self.client.updateNowPlaying(NowPlaying(artist="Björk", track="Joga", albumArtist="Test Album Artist"))
        print resp.prettify()
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.track.contents[0] == u"Jóga"
        assert resp.scrobbles.scrobble['corrected'] == "1"


suite = unittest.TestSuite([ unittest.TestLoader().loadTestsFromTestCase(ScrobbleTestCase)])
if __name__ == "__main__":
    #runner = xmlrunner.XMLTestRunner(sys.stdout)
    #runner.run(suite)
    unittest.main()


