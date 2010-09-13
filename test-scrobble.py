#-*- coding: utf-8 -*-
from scrobbling import *
import unittest
import xmlrunner
import time
from BeautifulSoup import BeautifulStoneSoup

class ScrobbleTestCase(unittest.TestCase):
    def setUp(self):
        self.client = ScrobblingClient()

    def testSingleScrobbleAccepted(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist",track="Test Track", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0

    def testSingleScrobbleFilteredArtist(self):
        resp = self.client.scrobble(Scrobble(artist="Unknown Artist",track="Test Track", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 0
        assert int(resp.scrobbles['ignored']) == 1
        assert int(resp.scrobbles.scrobble.ignoredmessage['code']) == 1

    def testSingleScrobbleFilteredTrack(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist",track="Track 1", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 0
        assert int(resp.scrobbles['ignored']) == 1
        assert int(resp.scrobbles.scrobble.ignoredmessage['code']) == 2

    def testSingleScrobbleFilteredTimestampPast(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist",track="Test Track", timestamp="0"))
        assert int(resp.scrobbles['accepted']) == 0
        assert int(resp.scrobbles['ignored']) == 1
        assert int(resp.scrobbles.scrobble.ignoredmessage['code']) == 3

    def testSingleScrobbleFilteredTimestampFuture(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist",track="Test Track", timestamp=str(pow(2, 32)-1)))
        assert int(resp.scrobbles['accepted']) == 0
        assert int(resp.scrobbles['ignored']) == 1
        assert int(resp.scrobbles.scrobble.ignoredmessage['code']) == 4

    def testSingleScrobbleAcceptedArtistSet(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist",track="Test Track", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.artist.contents[0] == u"Test Artist"

    def testSingleScrobbleAcceptedTrackSet(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist",track="Test Track", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.track.contents[0] == u"Test Track"

    def testSingleScrobbleAcceptedAlbumSet(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist", track="Test Track", album="Test Album", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.album.contents[0] == u"Test Album"

    def testSingleScrobbleAcceptedAlbumArtistSet(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist", track="Test Track", albumArtist="Test Album Artist", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.albumartist.contents[0] == u"Test Album Artist"

    def testSingleScrobbleAcceptedTimestampSet(self):
        timestamp=str(int(time.time()))
        resp = self.client.scrobble(Scrobble(artist="Test Artist", track="Test Track", albumArtist="Test Album Artist", timestamp=timestamp))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert str(resp.scrobbles.scrobble.timestamp.contents[0]) == timestamp

    def testSingleScrobbleInvalidParameterArtistMissing(self):
        timestamp=str(int(time.time()))
        try:
            resp = self.client.scrobble(Scrobble(track="Test Track", timestamp=str(int(time.time()))))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testSingleScrobbleInvalidParameterArtistEmpty(self):
        timestamp=str(int(time.time()))
        try:
            resp = self.client.scrobble(Scrobble(artist="", track="Test Track", timestamp=str(int(time.time()))))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testSingleScrobbleInvalidParameterTrackMissing(self):
        timestamp=str(int(time.time()))
        try:
            resp = self.client.scrobble(Scrobble(artist="Test Artist", timestamp=str(int(time.time()))))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testSingleScrobbleInvalidParameterTrackEmpty(self):
        timestamp=str(int(time.time()))
        try:
            resp = self.client.scrobble(Scrobble(artist="Test Artist", track="", timestamp=str(int(time.time()))))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testSingleScrobbleInvalidParameterTimestampMissing(self):
        timestamp=str(int(time.time()))
        try:
            resp = self.client.scrobble(Scrobble(artist="Test Artist", track="Test Track"))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testSingleScrobbleInvalidParameterTimestampEmpty(self):
        timestamp=str(int(time.time()))
        try:
            resp = self.client.scrobble(Scrobble(artist="Test Artist", track="Test Track", timestamp=""))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testSingleScrobbleAcceptedCorrectedArtist(self):
        resp = self.client.scrobble(Scrobble(artist="Bjork", track="Jóga", albumArtist="Test Album Artist", timestamp=str(int(time.time()))))
        print resp.prettify()
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.artist.contents[0] == u"Björk"
        assert resp.scrobbles.scrobble['corrected'] == "1"

    def testSingleScrobbleAcceptedCorrectedArtist(self):
        resp = self.client.scrobble(Scrobble(artist="Björk", track="Joga", albumArtist="Test Album Artist", timestamp=str(int(time.time()))))
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

