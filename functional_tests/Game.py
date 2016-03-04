from ._Base import BaseTestCase

from main.models import SHIPS


SILVER = 'rgba(192, 192, 192, 1)'
GREEN = 'rgba(0, 128, 0, 1)'


class TestGameStart(BaseTestCase):

    def setUp(self):
        super(TestGameStart, self).setUp()

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
                    field = self.browser.find_element_by_id('id_userfield_{}_{}'.format(line, j))
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


class TestGamePlay(BaseTestCase):

    def test_can_play(self):
        # Florence launches a new game.
        # She clicks on one of the boxes on opponent's board.
        # Clicked element becomes white and the log says "You missed!".
        # Florence waits until the opponent finishes his move (or many moves if it manages to hit one of her ships).
        # She notices that at least one box on her board changed its color from silver.
        # She also notices at least one new log message.
        # She clicks on another box on opponent's board.
        # Clicked element becomes red and the log says "You hit a ship!"
        # Opponent does not perform any moves, Florence has another turn.
        # Florence clicks on yet another box and make one of opponent's ships sink.
        # Opponent's still not moving.
        # Florence clicks on a different box and misses.
        # Opponent finally performs his move(s).
        self.fail()
