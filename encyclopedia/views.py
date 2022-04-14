from django.shortcuts import render, redirect
from markdown2 import Markdown
import random
from . import util
from .forms import EntryCreateForm
from django.urls import reverse


def index(request):
    q = request.GET.get('q')
    entries = util.list_entries()

    if q:
        entries = [e for e in entries if q.lower() in e.lower()]

    if q in entries:
        return redirect('wiki:single-entry', q)

    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def single_entry(request, title: str):
    markdowny = Markdown()
    content = util.get_entry(title)
    if not content:
        return render(request, 'encyclopedia/error.html', {
            'title': 'Page not found! 404'
        })
    return render(request, 'encyclopedia/single_entry.html', {
        'title': title,
        'content': markdowny.convert(content),
    })


def create_entry(request):
    form = EntryCreateForm()

    if request.method == 'POST':
        form = EntryCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            if title in util.list_entries():
                return render(request, 'encyclopedia/error.html', {
                    'title': f'The entry {title} is exists.'
                })
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect('wiki:index')

    return render(request, 'encyclopedia/create_entry.html', {
        'form': form,
    })


def edit_entry(request, title):
    if request.method == 'GET':
        title = title
        content = util.get_entry(title)
        form = EntryCreateForm({
            'title': title,
            'content':content,
        })
        return render(request, 'encyclopedia/edit_entry.html', {
            'title': title,
            'form': form,
        })

    form = EntryCreateForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data.get('title')
        content = form.cleaned_data.get('content')

        util.save_entry(title=title, content=content)
        return redirect('wiki:single-entry', title)



def random_entry(request):
    entries = util.list_entries()
    random_choice = random.choice(entries)
    return redirect('wiki:single-entry', random_choice)
