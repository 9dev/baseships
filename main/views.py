import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404
from django.views.generic import DetailView, FormView, TemplateView

from main.ai import ai_moves
from main.forms import NewGameForm
from main.models import BOARD_SIZE, Game, State


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
        player_board = json.dumps(form.cleaned_data['fields'])
        ai_board = json.dumps(['0' * BOARD_SIZE] * BOARD_SIZE)
        game = Game.objects.create(player=self.request.user, player_board=player_board, ai_board=ai_board)
        return HttpResponseRedirect(game.get_absolute_url())


class GameDetailView(DetailView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        context['board_size'] = BOARD_SIZE
        context['player_board'] = self.object.player_board
        return context


def move(request):
    x, y = request.POST.get('x', '0'), request.POST.get('y', '0')

    try:
        x, y = int(x), int(y)
    except (ValueError, IndexError):
        return HttpResponse('')

    game = get_list_or_404(Game, player=request.user)[0]
    state = int(json.loads(game.ai_board)[x][y])

    if state == State.EMPTY:
        state = State.MISSED

    response = {
        'state': state,
        'countermoves': ai_moves(game),
    }

    return HttpResponse(json.dumps(response))
