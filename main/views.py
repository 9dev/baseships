from django.views.generic import FormView, TemplateView

from main.forms import NewGameForm
from main.models import Board, BOARD_SIZE


class HomepageView(TemplateView):
    template_name = 'main/homepage.html'


class NewGameView(FormView):
    template_name = 'main/new_game.html'
    form_class = NewGameForm
    success_url = '/xyz'

    def get_context_data(self, **kwargs):
        context = super(NewGameView, self).get_context_data(**kwargs)
        context['board_size'] = BOARD_SIZE
        return context

    def form_valid(self, form):
        board = Board(owner=self.request.user, fields=form.cleaned_data['fields'])
        board.save()
        return super(NewGameView, self).form_valid(form)
