import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404
from django.views.generic import DetailView, FormView, TemplateView

from main.ai import ai_moves
from main.forms import NewGameForm
from main.models import BOARD_SIZE, Game, SHIPS, State


class HomepageView(TemplateView):
    template_name = 'main/homepage.html'


class NewGameView(FormView):
    template_name = 'main/new_game.html'
    form_class = NewGameForm

    def get_context_data(self, **kwargs):
        context = super(NewGameView, self).get_context_data(**kwargs)
        context['board_size'] = BOARD_SIZE
        context['ship_list'] = SHIPS
        return context

    def form_valid(self, form):
        player_board = json.dumps(form.cleaned_data['fields'])

        x = ['0' * BOARD_SIZE] * BOARD_SIZE
        x[1] = '1111111111'
        ai_board = json.dumps(x)

        player_ships = json.dumps(form.cleaned_data['ships'])
        ai_ships = json.dumps('')

        game = Game.objects.create(
            player=self.request.user,
            player_board=player_board,
            ai_board=ai_board,
            player_ships=player_ships,
            ai_ships=ai_ships,
        )

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
    countermoves = []

    if state == State.EMPTY:
        state = State.MISSED
        countermoves = ai_moves(game)
    elif state == State.FILLED:
        state = State.HIT

    game.update_ai_board(x, y, state)

    response = {
        'state': state,
        'countermoves': countermoves,
    }

    return HttpResponse(json.dumps(response))
