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
        ai_board = json.dumps(form.cleaned_data['fields'])

        player_ships = json.dumps(form.cleaned_data['ships'])
        ai_ships = json.dumps(form.cleaned_data['ships'])

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
        context['ai_board'] = self.object.ai_board.replace(str(State.FILLED), str(State.EMPTY))
        return context


def move(request):
    x, y = request.POST.get('x', '0'), request.POST.get('y', '0')

    try:
        x, y = int(x), int(y)
    except (ValueError, IndexError):
        return HttpResponse('')

    game = get_list_or_404(Game, player=request.user.pk)[0]
    state = int(json.loads(game.ai_board)[x][y])
    countermoves, ai_sunk, player_sunk = [], [], []

    if state == State.EMPTY:
        state = State.MISSED
        countermoves, player_sunk = ai_moves(game)
    elif state == State.FILLED:
        state, ai_sunk = game.hit_ai_ship(x, y)

    game.update_ai_board(x, y, state)

    response = {
        'state': state,
        'countermoves': countermoves,
        'ai_sunk': ai_sunk,
        'player_sunk': player_sunk,
        'game_over': game.game_over(),
    }

    return HttpResponse(json.dumps(response))
