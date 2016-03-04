import os
from selenium import webdriver

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


CHROMEDRIVER_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../tools/chromedriver/chromedriver'


class BaseTestCase(StaticLiveServerTestCase):
    fixtures = ['base.json']

    def setUp(self):
        self.browser = webdriver.Chrome(CHROMEDRIVER_PATH)

    def tearDown(self):
        self.browser.close()

    def get(self, url):
        self.browser.get('{}{}'.format(self.live_server_url, url))
