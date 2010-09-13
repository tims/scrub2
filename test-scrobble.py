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

    def testSingleScrobbleIgnored(self):
        resp = self.client.scrobble(Scrobble(artist="Unknown Artist",track="Test Track", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 0
        assert int(resp.scrobbles['ignored']) == 1

    def testSingleScrobbleAcceptedArtistSet(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist",track="Test Track", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.artist.contents == "Test Artist"

    def testSingleScrobbleAcceptedTrackSet(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist",track="Test Track", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.track.contents == "Test Track"

    def testSingleScrobbleAcceptedAlbumSet(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist", track="Test Track", album="Test Album", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.album.contents == "Test Album"

    def testSingleScrobbleAcceptedAlbumArtistSet(self):
        resp = self.client.scrobble(Scrobble(artist="Test Artist", track="Test Track", albumArtist="Test Album Artist", timestamp=str(int(time.time()))))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.albumartist.contents == "Test Album Artist"

    def testSingleScrobbleAcceptedTimestampSet(self):
        timestamp=str(int(time.time()))
        resp = self.client.scrobble(Scrobble(artist="Test Artist", track="Test Track", albumArtist="Test Album Artist", timestamp=timestamp))
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 0
        assert resp.scrobbles.scrobble.timestamp.contents == timestamp


suite = unittest.TestSuite([ unittest.TestLoader().loadTestsFromTestCase(ScrobbleTestCase)])
if __name__ == "__main__":
    #runner = xmlrunner.XMLTestRunner(sys.stdout)
    #runner.run(suite)
    unittest.main()
