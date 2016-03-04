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

    def login_as_admin(self):
        self.get(url='/admin')
        self.set_field('id_username', 'admin')
        self.set_field('id_password', 'admin')
        self.submit()

    def get_by_id(self, idx):
        return self.browser.find_element_by_id(idx)

    def set_field(self, field_id, value):
        field = self.get_by_id(field_id)
        field.clear()
        field.send_keys(value)

    def submit(self):
        form = self.browser.find_element_by_tag_name('form')
        form.submit()
