#-*- coding: utf-8 -*-
from scrobbling import *
import unittest
import xmlrunner
import time
from BeautifulSoup import BeautifulStoneSoup

class ScrobbleTestCase(unittest.TestCase):
    def setUp(self):
        self.client = ScrobblingClient()

    def testScrobbleAccepted(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist",track="Test Track", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0

    def testScrobbleFilteredArtist(self):
        resp = self.client.scrobble(Scrobble(artist="Unknown Artist",track="Test Track", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 0
        assert int(resp.scrobbles['ignored']) == 1
        assert int(resp.scrobbles.scrobble.ignoredmessage['code']) == 1

    def testScrobbleFilteredTrack(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist",track="Track 1", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 0
        assert int(resp.scrobbles['ignored']) == 1
        assert int(resp.scrobbles.scrobble.ignoredmessage['code']) == 2

    def testScrobbleFilteredTimestampPast(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist",track="Test Track", timestamp="0"))
        assert int(resp.scrobbles['accepted']) == 0
        assert int(resp.scrobbles['ignored']) == 1
        assert int(resp.scrobbles.scrobble.ignoredmessage['code']) == 3

    def testScrobbleFilteredTimestampFuture(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist",track="Test Track", timestamp=str(pow(2, 31)-1)))
        assert int(resp.scrobbles['accepted']) == 0
        assert int(resp.scrobbles['ignored']) == 1
        assert int(resp.scrobbles.scrobble.ignoredmessage['code']) == 4

    def testScrobbleAcceptedArtistSet(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist",track="Test Track", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.artist.contents[0] == u"Test Artist"

    def testScrobbleAcceptedTrackSet(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist",track="Test Track", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.track.contents[0] == u"Test Track"

    def testScrobbleAcceptedAlbumSet(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist", track="Test Track", album="Test Album", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.album.contents[0] == u"Test Album"

    def testScrobbleAcceptedAlbumArtistSet(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist", track="Test Track", albumArtist="Test Album Artist", timestamp=str(int(time.time()))))
        print resp.prettify()
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.albumartist.contents[0] == u"Test Album Artist"

    def testScrobbleAcceptedTimestampSet(self):
        timestamp=str(int(time.time()))
        resp = self.client.scrobble(Scrobble(artist="Test Artist", track="Test Track", albumArtist="Test Album Artist", timestamp=timestamp))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert str(resp.scrobbles.scrobble.timestamp.contents[0]) == timestamp

    def testScrobbleInvalidParameterArtistMissing(self):
        timestamp=str(int(time.time()))
        try:
            resp = self.client.scrobble(Scrobble(track="Test Track", timestamp=str(int(time.time()))))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testScrobbleInvalidParameterArtistEmpty(self):
        timestamp=str(int(time.time()))
        try:
            resp = self.client.scrobble(Scrobble(artist="", track="Test Track", timestamp=str(int(time.time()))))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testScrobbleInvalidParameterTrackMissing(self):
        timestamp=str(int(time.time()))
        try:
            resp = self.client.scrobble(Scrobble(artist="Test Artist", timestamp=str(int(time.time()))))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testScrobbleInvalidParameterTrackEmpty(self):
        timestamp=str(int(time.time()))
        try:
            resp = self.client.scrobble(Scrobble(artist="Test Artist", track="", timestamp=str(int(time.time()))))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testScrobbleInvalidParameterTimestampMissing(self):
        try:
            resp = self.client.scrobble(Scrobble(artist="Test Artist", track="Test Track"))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testScrobbleInvalidParameterTimestampEmpty(self):
        try:
            resp = self.client.scrobble(Scrobble(artist="Test Artist", track="Test Track", timestamp=""))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testScrobbleAcceptedCorrectedArtist(self):
        resp = self.client.scrobble(Scrobble(artist="Bjork", track="Jóga", albumArtist="Test Album Artist", timestamp=str(int(time.time()))))
        print resp.prettify()
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.artist.contents[0] == u"Björk"
        assert resp.scrobbles.scrobble['corrected'] == "1"

    def testScrobbleAcceptedCorrectedTrack(self):
        resp = self.client.scrobble(Scrobble(artist="Björk", track="Joga", albumArtist="Test Album Artist", timestamp=str(int(time.time()))))
        print resp.prettify()
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.track.contents[0] == u"Jóga"
        assert resp.scrobbles.scrobble['corrected'] == "1"

    def testScrobbleUnavailable(self):
        try:
            resp = self.client.scrobble(Scrobble(artist="Test Artist", track="Test Track", timestamp=str(int(time.time())), context="fm.last.commons.artifactory.exception.UnavailableException"))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            soup = BeautifulStoneSoup(e.read())
            print soup.prettify()
            assert e.code == 503
            assert int(soup.error['code']) == 16

    def testScrobbleRuntimeError(self):
        try:
            resp = self.client.scrobble(Scrobble(artist="Test Artist", track="Test Track", timestamp=str(int(time.time())), context="java.lang.RuntimeException"))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            soup = BeautifulStoneSoup(e.read())
            print soup.prettify()
            assert e.code == 503
            assert int(soup.error['code']) == 16

    def testScrobbleBadRequest(self):
        try:
            resp = self.client.scrobble(Scrobble(artist="Test Artist", track="Test Track", timestamp=str(int(time.time())), context="fm.last.commons.artifactory.exception.BadRequestException"))
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            soup = BeautifulStoneSoup(e.read())
            print soup.prettify()
            assert e.code == 400
            assert int(soup.error['code']) == 6


def suite():
    suite = unittest.TestSuite([ unittest.TestLoader().loadTestsFromTestCase(ScrobbleTestCase)])
    #suite = unittest.TestSuite()
    #suite.addTest(ScrobbleTestCase("testScrobbleBadRequest"))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    #runner = xmlrunner.XMLTestRunner(sys.stdout)
    runner.run(suite())
    #unittest.main()



