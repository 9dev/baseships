from django.conf.urls import url

from main import views


urlpatterns = [
    url(
        r'^$',
        views.HomepageView.as_view(),
        name='homepage',
    ),

    url(
        r'^new$',
        views.NewGameView.as_view(),
        name='new_game',
    ),
]
