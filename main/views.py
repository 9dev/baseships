from django.views.generic import DetailView, FormView, TemplateView
from django.http import HttpResponseRedirect

from main.forms import NewGameForm
from main.models import Board, BOARD_SIZE, Game


class HomepageView(TemplateView):
    template_name = 'main/homepage.html'


class NewGameView(FormView):
    template_name = 'main/new_game.html'
    form_class = NewGameForm

    def get_context_data(self, **kwargs):
        context = super(NewGameView, self).get_context_data(**kwargs)
        context['board_size'] = BOARD_SIZE
        return context

    def form_valid(self, form):
        player_board = Board.objects.create(owner=self.request.user, fields=form.cleaned_data['fields'])
        ai_board = Board.objects.create()
        game = Game.objects.create(player=self.request.user, player_board=player_board, ai_board=ai_board)
        return HttpResponseRedirect(game.get_absolute_url())


class GameDetailView(DetailView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        context['board_size'] = BOARD_SIZE
        context['player_board'] = self.object.player_board.fields
        return context
