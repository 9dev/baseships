from django.views.generic import TemplateView


class HomepageView(TemplateView):
    template_name = 'main/homepage.html'


def new_game(request):
    from django.http import HttpResponse
    return HttpResponse('new game')
