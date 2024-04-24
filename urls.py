from django.urls import path
from counter import views


urlpatterns = [
    path("", views.home_list_view, name="home"),
    path("count/", views.count_list_view, name="count"),
    path("start/", views.start_list_view, name="start"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("add_log/<int:starter_id>", views.add_log, name='add_log'),
    path("logdetailview/<int:starter_id>", views.StarterLogListView.as_view(), name='logdetailview'),
    path("async/", views.asyncview, name='asyncview'),
]
