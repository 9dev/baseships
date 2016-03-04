from ._Base import BaseTestCase


class TestStartGame(BaseTestCase):

    def test_cannot_start_with_too_few_ships(self):
        # Florence hits the homepage.
        self.get('/')

        # She clicks on a link to start a new game.
        # She sees a board.
        # She clicks on one of the fields on the board.
        # The field changes its color to green.
        # Florence submits the board.
        # She is redirected to the same page.
        # She sees an error.
        self.fail()
