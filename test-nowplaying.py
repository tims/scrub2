#-*- coding: utf-8 -*-
from scrobbling import *
import unittest
import xmlrunner
import time
from BeautifulSoup import BeautifulStoneSoup

class NowPlayingTestCase(unittest.TestCase):
    def setUp(self):
        self.client = ScrobblingClient()


    def testNowPlayingFilteredArtist(self):
        resp = self.client.updateNowPlaying(NowPlaying(artist="Unknown Artist",track="Test Track"))
        assert int(resp.nowplaying.ignoredmessage['code']) == 1

    def testNowPlayingFilteredTrack(self):
        resp = self.client.updateNowPlaying(NowPlaying(artist="Test Artist",track="Track 1"))
        print resp.prettify()
        assert int(resp.nowplaying.ignoredmessage['code']) == 2

    def testNowPlayingAcceptedParamsSet(self):
        resp = self.client.updateNowPlaying(NowPlaying(artist="Test Artist",track="Test Track", album="Test Album", albumArtist="Test Album Artist"))
        print resp.prettify()
        assert resp.nowplaying.artist.contents[0] == u"Test Artist"
        assert resp.nowplaying.track.contents[0] == u"Test Track"
        assert resp.nowplaying.album.contents[0] == u"Test Album"
        assert resp.nowplaying.albumartist.contents[0] == u"Test Album Artist"

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
            print resp.prettify()
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testNowPlayingAcceptedCorrectedArtist(self):
        resp = self.client.updateNowPlaying(NowPlaying(artist="Bjork", track="Jóga"))
        print resp.prettify()
        assert resp.nowplaying.artist.contents[0] == u"Björk"
        assert resp.nowplaying['corrected'] == "1"

    def testNowPlayingAcceptedCorrectedTrack(self):
        resp = self.client.updateNowPlaying(NowPlaying(artist="Björk", track="Joga"))
        print resp.prettify()
        assert resp.nowplaying.track.contents[0] == u"Jóga"
        assert resp.nowplaying['corrected'] == "1"


def suite():
    suite = unittest.TestSuite([ unittest.TestLoader().loadTestsFromTestCase(NowPlayingTestCase)])
    #suite = unittest.TestSuite()
    #suite.addTest(NowPlayingTestCase("testNowPlayingAcceptedParamsSet"))
    #suite.addTest(NowPlayingTestCase("testNowPlayingAcceptedCorrectedTrack"))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    #runner = xmlrunner.XMLTestRunner(sys.stdout)
    runner.run(suite())


