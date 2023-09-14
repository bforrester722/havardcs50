from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from . import util
from random import choice
from markdown2 import Markdown
import logging
logger = logging.getLogger('django')


# class EntryForm(forms.Form):
#     title = forms.CharField(label="New Task")
#     content = forms.CharField(label="content")
class EntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Title',  'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Content',  'class': 'form-control'}))


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    page = util.get_entry(title)
    return render(request, "encyclopedia/error.html", {"error": "404"}) if page is None else render(request, "encyclopedia/entry.html", {"title": title, "content": Markdown().convert(page)})


def create(request):

    if request.method == "POST":
        form = EntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None:
                util.save_entry(title, content)
                messages.success(
                    request, f'{title} created')
                return HttpResponseRedirect(reverse("encyclopedia:index"))
            else:
                messages.error(
                    request, f'{title} already exists', extra_tags=f'{title}')
                return render(request, "encyclopedia/create.html", {"form": form})

        else:
            return render(request, "encyclopedia/create.html", {"form": form})

    return render(request, "encyclopedia/create.html", {"form": EntryForm()})


def edit(request, title):

    if request.method == "POST":
        form = EntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"].encode()

            util.save_entry(title, content)
            messages.success(request, f'{title} created')
            return HttpResponseRedirect("/wiki/%s" % title)
    else:
        page = util.get_entry(title)
        form = EntryForm({'title': title, 'content': page})
        form.fields['title'].widget.attrs['readonly'] = True
        return render(request, "encyclopedia/create.html", {"form": form, "title": title})


def random(request):
    return entry(request, choice(util.list_entries()))
