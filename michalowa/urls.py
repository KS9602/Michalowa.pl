from django.urls import path
from .views import (
    forum,
    new_user,
    login_user,
    logout_user,
    init_app,
    section,
    subject,
    new_post,
    new_topic,
    index,
    like,
    michalowaApi,
)

urlpatterns = [
    path("registration/", new_user, name="registration"),
    path("login/", login_user, name="login_user"),
    path("logout/", logout_user, name="logout"),
    path("init_app/", init_app),
    path("", index, name="index"),
    path("forum/", forum, name="forum"),
    path("forum/<str:section>", section, name="section"),
    path("forum/<str:section>/new_topic", new_topic, name="new_topic"),
    path("forum/<str:section>/<str:title>", subject, name="subject"),
    path("forum/<str:section>/<str:title>/new_post", new_post, name="new_post"),
    path("forum_like/<str:pk>", like, name="like"),
    path("michalowa_api/<str:type>/<str:pk>", michalowaApi, name="michalowaApi"),
]
