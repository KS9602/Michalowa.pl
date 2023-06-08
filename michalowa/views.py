from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User

import requests
from random import randint, choice
from decouple import config

from .models import ForumUser, Section, Subject, Post
from .forms import NewUserForm, LoginForm
from .decorators import login_required
from .constants import SECTIONS


def init_app(request):
    """Generate random users and topics"""

    if len(User.objects.all()) != 1:
        return redirect("forum")

    admin = User.objects.get(id=1)
    admin_form_user = ForumUser(user=admin, nick=request.user.username)
    admin_form_user.save()

    names = requests.get("https://names.drycodes.com/10").json()
    emails = [i + "@gmail.com" for i in names]
    passwrod = config("USER_PASSWORD")

    for i, j, k in zip(names, emails, passwrod):
        user = User.objects.create_user(username=i, email=j, password=k)
        user.save()
        forum_user = ForumUser(user=user, nick=i)
        forum_user.save()

    for i in SECTIONS.values():
        section = Section(name=i, section_description=i)
        section.save()

    for i in range(25):
        subject_description = requests.get(
            f"https://baconipsum.com/api/?type=all-meat&sentences={randint(1,15)}&start-with-lorem=1"
        ).json()
        title = subject_description[0].split()[5].capitalize()
        subject_creator = ForumUser.objects.get(id=randint(1, 11))
        s = randint(1, 6)
        subject_section = Section.objects.get(name=SECTIONS[s])
        subject = Subject(
            title=title,
            subject_description=subject_description[0],
            subject_creator=subject_creator,
            subject_section=subject_section,
        )
        subject.save()

    for i in range(40):
        content = requests.get(
            f"https://baconipsum.com/api/?type=all-meat&sentences={randint(1,15)}&start-with-lorem=1"
        ).json()

        topic = Subject.objects.get(id=randint(1, 25))
        post_creator = ForumUser.objects.get(id=randint(1, 11))

        post = Post(content=content[0], topic=topic, post_creator=post_creator)

        post.save()

    return redirect("forum")


@transaction.atomic()
def new_user(request):
    form = NewUserForm()

    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            forum_user = ForumUser(user=user, nick=user.username)
            forum_user.save()
            login(request, user)

            messages.success(request, "Zarejestrowano")
            return redirect("forum")

    context = {"form": form}
    return render(request, "new_user.html", context=context)


def login_user(request):
    form = LoginForm()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Zalogowano")
            return redirect("forum")

        else:
            messages.error(request, "Błędne dane")
            return redirect("login")

    context = {"form": form}
    return render(request, "login_user.html", context=context)


@login_required
def logout_user(request):
    logout(request)
    return redirect("forum")


def index(request):
    subjects = Subject.objects.all()
    subject = choice(subjects)

    context = {"subject": subject}
    return render(request, "michalowa.html", context=context)


def forum(request):
    sections = Section.objects.all()

    context = {"sections": sections}
    return render(request, "main.html", context=context)


def section(request, section):
    subjects = Subject.objects.filter(subject_section__name=section)

    context = {"subjects": subjects}
    return render(request, "subjects.html", context=context)


def subject(requst, section, title):
    topic = Subject.objects.get(title=title)
    posts = Post.objects.filter(topic__title=title).order_by("date_created")

    context = {"topic": topic, "posts": posts}
    return render(requst, "topic.html", context=context)


@login_required
def new_post(requst, section, title):
    topic = Subject.objects.get(title=title)

    if requst.method == "POST":
        if "cancel" in requst.POST:
            return redirect("subject", topic.subject_section.name, topic.title)

        elif "enter" in requst.POST:
            text = requst.POST.get("textbox")
            user = ForumUser.objects.get(user=requst.user)
            post = Post.objects.create(content=text, topic=topic, post_creator=user)
            post.save()

            return redirect("subject", topic.subject_section.name, topic.title)

    context = {"topic": topic}
    return render(requst, "new_post.html", context=context)


@login_required
def new_topic(requst, section):
    if requst.method == "POST":
        if "cancel" in requst.POST:
            return redirect("section", section)

        elif "enter" in requst.POST:
            title = requst.POST.get("title")
            text = requst.POST.get("textbox")
            user = ForumUser.objects.get(user=requst.user)
            category = Section.objects.get(name=section)
            subject = Subject.objects.create(
                title=title,
                subject_description=text,
                subject_creator=user,
                subject_section=category,
            )
            subject.save()

            return redirect("section", section)

    context = {"section": section}
    return render(requst, "new_topic.html", context=context)


@login_required
def like(request, pk):
    subject = Subject.objects.get(id=pk)
    likes = subject.likes.values("id")
    likes = likes.values_list("id", flat=True)
    user = ForumUser.objects.get(id=request.user.id)

    if request.user.id in likes:
        subject.likes.remove(user)
    else:
        subject.likes.add(user)

    subject.save()

    return redirect("section", subject.subject_section)


def michalowaApi(request, type, pk):
    if type == "subject":
        subject = get_object_or_404(Subject, id=pk)
        post_dict = {
            "author": subject.subject_creator.nick,
            "content": subject.subject_description,
        }

    elif type == "post":
        post = get_object_or_404(Post, id=pk)
        post_dict = {"author": post.post_creator.nick, "content": post.content}

    return JsonResponse(post_dict)
