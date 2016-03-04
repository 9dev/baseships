from ._Base import BaseTestCase

from main.models import SHIPS


SILVER = 'rgba(192, 192, 192, 1)'
GREEN = 'rgba(0, 128, 0, 1)'


class TestStartGame(BaseTestCase):

    def setUp(self):
        super(TestStartGame, self).setUp()

        # Florence logs in as an admin.
        self.login_as_admin()

    def create_ship_part(self, x, y):
        field = self.browser.find_element_by_id('id_field_{}_{}'.format(x, y))
        field.click()

    def assert_can_create_ships(self):
        # Florence clicks on the buttons until she creates all the ships.
        line = 0
        for length, n in SHIPS.items():
            for i in range(n):
                for j in range(length):
                    self.create_ship_part(line, j)
                line += 1

    def assert_ships_are_present(self):
        # Florence makes sure she sees all her ships on her board.
        line = 0
        for length, n in SHIPS.items():
            for i in range(n):
                for j in range(length):
                    field = self.browser.find_element_by_id('id_field_{}_{}'.format(line, j))
                    self.assertEqual(field.value_of_css_property('background-color'), GREEN)
                line += 1

    def test_cannot_start_with_too_few_ships(self):
        # Florence hits the homepage.
        self.get('/')

        # She clicks on a link to start a new game.
        self.browser.find_element_by_link_text('New game').click()

        # She is taken to a game creator.
        self.assertEqual(self.browser.current_url, '{}/new'.format(self.live_server_url))

        # She sees a board.
        self.browser.find_element_by_id('id_board')

        # She clicks on one of the fields on the board and it changes its color to green.
        field = self.browser.find_element_by_id('id_field_2_2')
        self.assertEqual(field.value_of_css_property('background-color'), SILVER)
        field.click()
        self.assertEqual(field.value_of_css_property('background-color'), GREEN)

        # Florence submits the board.
        self.browser.find_element_by_tag_name('form').submit()

        # She is being redirected to the same page.
        self.assertEqual(self.browser.current_url, '{}/new'.format(self.live_server_url))

        # She sees an error.
        self.assertIn('Too few ships!', self.browser.page_source)

    def test_can_start_new_game(self):
        # Florence hits the homepage.
        self.get('/')

        # She clicks on a link to start a new game.
        self.browser.find_element_by_link_text('New game').click()

        # She is taken to a game creator.
        self.assertEqual(self.browser.current_url, '{}/new'.format(self.live_server_url))

        # She sees a board.
        self.browser.find_element_by_id('id_board')

        # She creates her ships.
        self.assert_can_create_ships()

        # Florence submits the board.
        self.browser.find_element_by_tag_name('form').submit()

        # She is being redirected to a page with actual game.
        self.assertEqual(self.browser.current_url, '{}/game/1'.format(self.live_server_url))

        # She sees her ships on her board.
        self.assert_ships_are_present()
