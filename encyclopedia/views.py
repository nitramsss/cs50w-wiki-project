from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from markdown2 import markdown
from django import forms
import random

from . import util


class Form(forms.Form):
    title = forms.CharField(
        label="Title",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a title',
        }),
    )
    content = forms.CharField(
        label="Description",
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Write your description here...',
            'rows': 5,
        }),
    )


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, entry):
    if util.get_entry(entry):
        return render(request, "encyclopedia/entry.html", {
            "content": markdown(util.get_entry(entry)),
            "title": entry.title(),
            "entry": entry
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Page does not exist."
        })
    

def create_page(request):
    _form = Form()

    if request.method == "POST":
        form = Form(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "message": "Page already exist."
                })
            else:
                util.save_entry(title, markdown(content))
                return HttpResponseRedirect(reverse('entrypage', kwargs={
                    "entry": title
                    }))
        else:
            _form = form

    return render(request, "encyclopedia/create.html", {
        "form": _form
    })


def edit_page(request, page):
    title = page.title()
    content = util.get_entry(title)
    _form = Form(initial={
        "title": title,
        "content": content
    })
   
    if request.method == "POST":
        form = Form(request.POST)

        if form.is_valid():
            new_content = form.cleaned_data["content"]
            util.save_entry(title, new_content)
            return HttpResponseRedirect(reverse('entrypage', kwargs={
                "entry": page
            }))
        else:
            _form = form()

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content,
        "form": _form,
        "entry": page
    })
        


def random_page(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return HttpResponseRedirect(reverse('entrypage', kwargs={
        "entry": entry
    }))


