import json
from selenium.webdriver.support.ui import Select
from time import sleep

from django.contrib.auth.models import User

from main.models import BOARD_SIZE, Game, SHIPS, State

from ._Base import BaseTestCase


BLUE = 'rgba(0, 0, 255, 1)'
GREEN = 'rgba(0, 128, 0, 1)'
RED = 'rgba(255, 0, 0, 1)'
SILVER = 'rgba(192, 192, 192, 1)'
WHITE = 'rgba(255, 255, 255, 1)'


def create_new_game(finished=False):
    player = User.objects.get(username='admin')

    ship_state = str(State.SUNK if finished else State.FILLED)
    empty_state = str(State.MISSED if finished else State.EMPTY)

    board = [empty_state * BOARD_SIZE] * BOARD_SIZE
    ships = []

    for line, ship in enumerate(SHIPS):
        parts = int(ship)
        board[line] = ship_state * parts + board[line][parts:]
        ships.append([])

        for part in range(parts):
            ships[line].append([line, part])

    board, ships = json.dumps(board), json.dumps(ships)
    return Game.objects.create(player=player, player_board=board, ai_board=board, player_ships=ships, ai_ships=ships)


class TestGameStart(BaseTestCase):

    def setUp(self):
        super(TestGameStart, self).setUp()

        # Florence logs in as an admin.
        self.login_as_admin()

    def create_ship_part(self, x, y):
        field = self.browser.find_element_by_id('id_field_{}_{}'.format(x, y))
        field.click()

    def assert_can_create_ships(self):
        line = 0
        ship_list = Select(self.get_by_id('id_ships_list'))

        # Florence selects ship by ship and clicks on the buttons until she creates them all.
        for ship in ship_list.options:
            ship_list.select_by_value(str(line))
            length, _ = ship.text.split('-element ship')
            for i in range(int(length)):
                self.create_ship_part(line, i)
            line += 1

    def assert_ships_are_present(self):
        # Florence makes sure she sees all her ships on her board.
        line = 0
        for ship in SHIPS:
            for i in range(int(ship)):
                field = self.browser.find_element_by_id('id_playerfield_{}_{}'.format(line, i))
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
        pk = Game.objects.last().pk
        self.assertEqual(self.browser.current_url, '{}/game/{}'.format(self.live_server_url, pk))

        # She sees her ships on her board.
        self.assert_ships_are_present()


class TestGamePlay(BaseTestCase):

    def test_can_play(self):
        game = create_new_game()

        # Florence logs in as an admin.
        self.login_as_admin()

        # Florence launches a new game.
        self.get('/game/{}'.format(game.pk))

        # She clicks on one of the fields on opponent's board.
        field = self.get_by_id('id_aifield_9_9')
        field.click()

        # Clicked element becomes white and the log says "You missed!".
        log = self.get_by_id("log")
        self.assertTrue(log.text.endswith('You missed!'))
        self.assertEqual(field.value_of_css_property('background-color'), WHITE)

        # Florence waits until the opponent finishes his move (or many moves if it manages to hit one of her ships).
        sleep(5)

        # She notices that at least one box on her board changed its color from silver to white.
        fields = self.browser.find_elements_by_css_selector('#board_player button')
        self.assertTrue(any(f.value_of_css_property('background-color') == WHITE for f in fields))

        # She also notices at least one new log message.
        self.assertTrue(log.text.endswith('Opponent missed!'))

        # She clicks on another field on opponent's board.
        field = self.get_by_id('id_aifield_4_0')
        field.click()

        # Clicked element becomes red and the log says "You hit a ship!"
        sleep(2)
        self.assertTrue(log.text.endswith('You hit a ship!'))
        self.assertEqual(field.value_of_css_property('background-color'), RED)

        # Opponent does not perform any moves, Florence has another turn.
        sleep(2)
        self.assertTrue(log.text.endswith('You hit a ship!'))

        # Florence clicks on yet another field and make one of opponent's ships sink.
        field2 = self.get_by_id('id_aifield_4_1')
        field2.click()
        sleep(2)

        self.assertTrue(log.text.endswith('You sunk a ship!'))
        self.assertEqual(field.value_of_css_property('background-color'), BLUE)
        self.assertEqual(field2.value_of_css_property('background-color'), BLUE)

        # Opponent's still not moving.
        sleep(2)
        self.assertTrue(log.text.endswith('You sunk a ship!'))

        # Florence clicks on a different box and misses.
        field = self.get_by_id('id_aifield_9_8')
        field.click()
        sleep(2)
        self.assertEqual(field.value_of_css_property('background-color'), WHITE)

        # Opponent finally performs his move(s).
        sleep(5)
        self.assertTrue(log.text.endswith('Opponent missed!'))


class TestGameOver(BaseTestCase):

    def setUp(self):
        super(TestGameOver, self).setUp()

        self.game = create_new_game(finished=True)
        self.game.update_ai_board(6, 0, State.FILLED)

    def test_can_lose(self):
        self.game.update_player_board(6, 0, State.FILLED)
        self.game.update_ai_board(9, 9, State.EMPTY)

        # Florence is logged in as an admin.
        self.login_as_admin()

        # She is nearly at the end of the game.
        self.get('/game/{}'.format(self.game.pk))

        # She performs a move and misses.
        field = self.get_by_id('id_aifield_9_9')
        field.click()
        sleep(1)
        self.assertEqual(field.value_of_css_property('background-color'), WHITE)

        # Her opponent makes her last ship sunk.
        log = self.get_by_id("log")
        sleep(5)
        self.assertTrue(log.text.endswith('Opponent sunk a ship!'))

        # Florence sees a big header "You lose!".
        self.assertEqual(self.get_by_id('id_game_over').text, "You lose!")

    def test_can_win(self):
        self.game.player_board = self.game.player_board.replace(str(State.SUNK), str(State.FILLED))
        self.game.save()

        # Florence is logged in as an admin.
        self.login_as_admin()

        # She is nearly at the end of the game.
        self.get('/game/{}'.format(self.game.pk))

        # She performs a move and makes opponent's last ship sunk.
        field = self.get_by_id('id_aifield_6_0')
        field.click()
        sleep(2)
        self.assertEqual(field.value_of_css_property('background-color'), BLUE)

        # Florence sees a big header "You win!".
        self.assertEqual(self.get_by_id('id_game_over').text, "You win!")
