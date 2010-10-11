#-*- coding: utf-8 -*-
from scrobbling import *
import unittest
import xmlrunner
import time
from BeautifulSoup import BeautifulStoneSoup

class ScrobbleBatchTestCase(unittest.TestCase):
    def setUp(self):
        self.client = ScrobblingClient()
        self.scrobble0 = Scrobble(artist="Test Artist 0",track="Test Track 0", timestamp=str(int(time.time())))
        self.scrobble1 = Scrobble(artist="Test Artist 1",track="Test Track 1", timestamp=str(int(time.time())))


    def testScrobbleAccepted(self):
        resp = self.client.scrobbleBatch([self.scrobble0, self.scrobble1])
        assert int(resp.scrobbles['accepted']) == 2
        assert int(resp.scrobbles['ignored']) == 0

    def testScrobbleAccepted50(self):
        batch = []
        for i in range(0,50):
            batch.append(self.scrobble0)
        resp = self.client.scrobbleBatch(batch)
        assert int(resp.scrobbles['accepted']) == 50
        assert int(resp.scrobbles['ignored']) == 0

    def testScrobbleRejected51(self):
        batch = []
        for i in range(0,51):
            batch.append(self.scrobble0)
        try:
            resp = self.client.scrobbleBatch(batch)
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()
 
    def testScrobbleFilteredAll(self):
        self.scrobble0.timestamp = "0"
        self.scrobble1.artist = "Unknown Artist"
        resp = self.client.scrobbleBatch([self.scrobble0, self.scrobble1])
        assert int(resp.scrobbles['accepted']) == 0
        assert int(resp.scrobbles['ignored']) == 2
        s0,s1 = resp.findAll("scrobble")
        assert int(s0.ignoredmessage['code']) == 3
        assert int(s1.ignoredmessage['code']) == 1

    def testScrobbleFilteredArtist(self):
        self.scrobble1.artist = "Unknown Artist"
        resp = self.client.scrobbleBatch([self.scrobble0, self.scrobble1])
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 1
        s0,s1 = resp.findAll("scrobble")
        assert int(s1.ignoredmessage['code']) == 1

    def testScrobbleFilteredTrack(self):
        self.scrobble1.track = "Track 1"
        resp = self.client.scrobbleBatch([self.scrobble0, self.scrobble1])
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 1
        s0,s1 = resp.findAll("scrobble")
        assert int(s1.ignoredmessage['code']) == 2

    def testScrobbleFilteredTimestampPast(self):
        self.scrobble1.timestamp = "0"
        resp = self.client.scrobbleBatch([self.scrobble0, self.scrobble1])
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 1
        s0,s1 = resp.findAll("scrobble")
        assert int(s1.ignoredmessage['code']) == 3

    def testScrobbleFilteredTimestampFuture(self):
        self.scrobble1.timestamp = str(pow(2, 31)-1)
        resp = self.client.scrobbleBatch([self.scrobble0, self.scrobble1])
        assert int(resp.scrobbles['accepted']) == 1
        assert int(resp.scrobbles['ignored']) == 1
        s0,s1 = resp.findAll("scrobble")
        assert int(s1.ignoredmessage['code']) == 4

    def testScrobbleParamsSet(self):
        self.scrobble0.album = "Test Album 0"
        self.scrobble0.albumArtist = "Test Album Artist 0"
        self.scrobble1.album = "Test Album 1"
        self.scrobble1.albumArtist = "Test Album Artist 1"
        try:
            resp = self.client.scrobbleBatch([self.scrobble0, self.scrobble1])
            print resp.prettify()
        except HTTPError, e:
            print e,"\n",e.read()
            raise e
        assert int(resp.scrobbles['accepted']) == 2
        assert int(resp.scrobbles['ignored']) == 0

        s0,s1 = resp.findAll("scrobble")
        assert s0.artist.contents[0] == u"Test Artist 0"
        assert s0.track.contents[0] == u"Test Track 0"
        assert s0.album.contents[0] == u"Test Album 0"
        assert s0.albumartist.contents[0] == u"Test Album Artist 0"
        assert str(s0.timestamp.contents[0]) == self.scrobble0.timestamp

        assert s1.artist.contents[0] == u"Test Artist 1"
        assert s1.track.contents[0] == u"Test Track 1"
        assert s1.album.contents[0] == u"Test Album 1"
        assert s1.albumartist.contents[0] == u"Test Album Artist 1"
        assert str(s1.timestamp.contents[0]) == self.scrobble1.timestamp

    def testScrobbleInvalidParameterArtistMissing(self):
        self.scrobble0.artist = None
        try:
            resp = self.client.scrobbleBatch([self.scrobble0, self.scrobble1])
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testScrobbleInvalidParameterArtistEmpty(self):
        self.scrobble0.artist = ""
        timestamp=str(int(time.time()))
        try:
            resp = self.client.scrobbleBatch([self.scrobble0, self.scrobble1])
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testScrobbleInvalidParameterTrackMissing(self):
        self.scrobble0.track = None
        try:
            resp = self.client.scrobbleBatch([self.scrobble0, self.scrobble1])
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testScrobbleInvalidParameterTrackEmpty(self):
        self.scrobble0.track = ""
        try:
            resp = self.client.scrobbleBatch([self.scrobble0, self.scrobble1])
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testScrobbleInvalidParameterTimestampMissing(self):
        self.scrobble0.timestamp = None
        try:
            resp = self.client.scrobbleBatch([self.scrobble0, self.scrobble1])
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testScrobbleInvalidParameterTimestampEmpty(self):
        self.scrobble0.timestamp = ""
        try:
            resp = self.client.scrobbleBatch([self.scrobble0, self.scrobble1])
            print resp
            assert 1 == 2, "exception should be thrown"
        except HTTPError, e:
            assert e.code == 400
            soup = BeautifulStoneSoup(e.read())
            assert int(soup.error['code']) == 6
            print soup.prettify()

    def testScrobbleAcceptedCorrectedArtist(self):
        self.scrobble1.artist="Bjork"
        self.scrobble1.track="Jóga"
        resp = self.client.scrobbleBatch([self.scrobble0, self.scrobble1])
        print resp.prettify()
        assert int(resp.scrobbles['accepted']) == 2
        assert int(resp.scrobbles['ignored']) == 0
        s0,s1 = resp.findAll("scrobble")
        assert s1.artist.contents[0] == u"Björk"
        assert s1.artist['corrected'] == "1"

    def testScrobbleAcceptedCorrectedTrack(self):
        self.scrobble1.artist="Björk"
        self.scrobble1.track="Joga"
        resp = self.client.scrobbleBatch([self.scrobble0, self.scrobble1])
        print resp.prettify()
        assert int(resp.scrobbles['accepted']) == 2
        assert int(resp.scrobbles['ignored']) == 0
        s0,s1 = resp.findAll("scrobble")
        assert s1.track.contents[0] == u"Jóga"
        assert s1.track['corrected'] == "1"

    def testScrobbleAcceptedCorrectedArtistAndTrack(self):
        scrobble0 = Scrobble(artist="Björk", track="Joga", timestamp=str(int(time.time())))
        scrobble1 = Scrobble(artist="Bjork", track="Jóga", timestamp=str(int(time.time())))
        scrobble2 = Scrobble(artist="Bjork", track="Joga", timestamp=str(int(time.time())))
        
        resp = self.client.scrobbleBatch([scrobble0,scrobble1,scrobble2])
        print resp.prettify()
        assert int(resp.scrobbles['accepted']) == 3
        assert int(resp.scrobbles['ignored']) == 0
        s0,s1,s2 = resp.findAll("scrobble")
        assert s0.track.contents[0] == u"Jóga"
        assert s0.track['corrected'] == "1"
        assert s1.artist.contents[0] == u"Björk"
        assert s1.artist['corrected'] == "1"
        assert s2.track.contents[0] == u"Jóga"
        assert s2.track['corrected'] == "1"
        assert s2.artist.contents[0] == u"Björk"
        assert s2.artist['corrected'] == "1"

def suite():
    suite = unittest.TestSuite([ unittest.TestLoader().loadTestsFromTestCase(ScrobbleBatchTestCase)])
    #suite = unittest.TestSuite()
    #suite.addTest(ScrobbleBatchTestCase("testScrobbleParamsSet"))
    #suite.addTest(ScrobbleBatchTestCase("testScrobbleInvalidParameterArtistEmpty"))

    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    #runner = xmlrunner.XMLTestRunner(sys.stdout)
    runner.run(suite())
    #unittest.main()


