from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from . import util
from random import choice
from markdown2 import Markdown
import logging

logger = logging.getLogger("django")


class EntryForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Title", "class": "form-control"})
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Content", "class": "form-control"})
    )


# Render the index page with a list of all entries
def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


# Render an individual entry page or display an error page if the entry does not exist
def entry(request, title):
    page = util.get_entry(title)
    if page is None:
        return render(request, "encyclopedia/error.html", {"error": "404"})
    else:
        return render(
            request,
            "encyclopedia/entry.html",
            {"title": title, "content": Markdown().convert(page)},
        )


# Handle the creation of new entries
def create(request):
    if request.method == "POST":
        form = EntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # New Entry
            if util.get_entry(title) is None:
                util.save_entry(title, content)
                messages.success(request, f"{title} created")
                return HttpResponseRedirect(reverse("encyclopedia:index"))
            # Already exists
            else:
                messages.error(
                    request, f"{title} already exists", extra_tags=f"{title}"
                )
                return render(request, "encyclopedia/create.html", {"form": form})

        else:
            return render(request, "encyclopedia/create.html", {"form": form})
    # Empty Form
    return render(request, "encyclopedia/create.html", {"form": EntryForm()})


# Handle the editing of existing entries
def edit(request, title):
    # form submit
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"].encode()

            util.save_entry(title, content)
            messages.success(request, f"{title} edited successfully")
            return HttpResponseRedirect("/wiki/%s" % title)
    # Prepopulated form
    else:
        page = util.get_entry(title)
        form = EntryForm({"title": title, "content": page})
        form.fields["title"].widget.attrs["readonly"] = True
        return render(
            request, "encyclopedia/create.html", {"form": form, "title": title}
        )


# Handle search functionality
def search(request):
    searchVal = request.GET.get("q", "")
    # route to entry if exists
    if util.get_entry(searchVal):
        return entry(request, searchVal)
    # displays matches
    else:
        foundEntries = [
            i for i in util.list_entries() if searchVal.lower() in i.lower()
        ]
        return render(
            request,
            "encyclopedia/index.html",
            {
                "entries": foundEntries,
                "searchVal": searchVal,
            },
        )


# Display a random entry
def random(request):
    return entry(request, choice(util.list_entries()))
