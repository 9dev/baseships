from ._Base import BaseTestCase


class TestStartGame(BaseTestCase):

    def test_cannot_start_with_too_few_ships(self):
        # Florence hits the homepage.
        self.get('/')

        # She clicks on a link to start a new game.
        self.browser.find_element_by_link_text('New game').click()

        # She is taken to a game creator.
        self.assertEqual(self.browser.current_url, '/new')

        # She sees a board.
        self.browser.find_element_by_id('id_board')

        # She clicks on one of the fields on the board and it changes its color to green.
        field = self.browser.find_element_by_id('id_field_2_2')
        self.assertEqual(field.value_of_css_property('background-color'), 'silver')
        field.click()
        self.assertEqual(field.value_of_css_property('background-color'), 'green')

        # Florence submits the board.
        self.browser.find_element_by_tag_name('form').submit()

        # She is redirected to the same page.
        self.assertEqual(self.browser.current_url, '/new')

        # She sees an error.
        self.assertIn(self.browser.page_source, 'Too few ships!')
