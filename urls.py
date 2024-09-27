from django.urls import path
from counter import views


urlpatterns = [
    path("", views.home_list_view, name="home"),
    path("count/", views.count_list_view, name="count"),
    path("start/", views.start_list_view, name="start"),
    path("result/", views.result_list_view, name="result"),
    path("contact/", views.contact, name="contact"),
    path("add_log/<int:starter_id>", views.add_log, name='add_log'),
    path("take_a_break/<int:starter_id>", views.take_a_break, name='take_a_break'),
    path("back_to_swim/<int:starter_id>/<int:lane>", views.back_to_swim, name='back_to_swim'),
    path("logdetailview/<int:starter_id>", views.StarterLogListView.as_view(), name='logdetailview'),
    path("loglistlanes/<str:lanes>", views.loglistlanes, name='loglistlanes'),
    path("startlist/", views.startlist, name='startlist'),
     path("resultlist/", views.resultlist, name="resultlist"),
]
