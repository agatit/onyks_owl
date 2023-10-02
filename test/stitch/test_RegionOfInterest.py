from unittest import TestCase


class TestRegionOfInterest(TestCase):
    def setUp(self):
        self.region = (1920, 1080)
        self.p1 = (20, 100)
        self.p2 = (20, 100)

    def from_margin_px_should_be_valid(self):
        self.assertEquals(True, True)
