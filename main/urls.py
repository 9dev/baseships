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
        views.new_game,
        name='new_game',
    ),
]
