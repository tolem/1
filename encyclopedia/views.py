from django.shortcuts import render
from . import util
from django.http import HttpResponse
from .myform import NewWikiForm, EditWikiForm
from random import randint


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# renders a content from title of pass in args
def title(request, prefix):
    title = prefix.lower()
    content = util.get_entry(prefix)
    if content is not None:
        return render(request, "encyclopedia/entrypage.html", {
        "title": title,
        "content": util.converts_md_to_html(content)
        })

    else:
        return render(request, 'encyclopedia/err.html', {
        'msg': ' status:404, encyclopedia doesn\'t exist.' 
        })



def search(request):
    if request.method == "POST":
        query = request.POST["q"].lower()
        # If query is empty string
        if query == "":
            return render(request, "encyclopedia/search.html", {
            "query": query,
            "search_result": None
            })


        # If queried, check if query is substring of an existing wiki
        saved_entries = [x.lower() for x in util.list_entries()]
        matching_entries = [s.lower() for s in saved_entries if query in s]

        # checks if query perfectly matches a wiki
        if len(matching_entries) == 1 and query == matching_entries[0]:
            return render(request, "encyclopedia/entrypage.html", {
                "title": query,
                "content": util.converts_md_to_html(util.get_entry(query))
            })
        # validates If query is not part of an existing wiki
        else:
            print(f"testing {matching_entries}")
            return render(request, "encyclopedia/search.html", {
            "query": query,
            "search_results": matching_entries if len(matching_entries) >= 1 else None
            })
    return render(request, "encyclopedia/err.html", {
        "msg": "Sorry can't find your query try something else"
    })


# Handles wiki entry creation (with Django Forms)
def create_entry(request):
    if request.method == "POST":
        new_entry_form = NewWikiForm(request.POST)
        if new_entry_form.is_valid():
            saved_entries = saved_entries = [x.lower() for x in util.list_entries()]
            entry_title = new_entry_form.cleaned_data["entry_title"].lower()
            if entry_title in saved_entries:
                return render(request, "encyclopedia/err.html", {
                    "msg": "Failed to publish new entry (already exists in Wiki database)."
                })
            # Save entry to disk and redirect user to new entry's page
            entry_description = new_entry_form.cleaned_data["entry_description"]
            util.save_entry(entry_title, entry_description)
            return render(request, "encyclopedia/entrypage.html", {
                "title": entry_title,
                "content": util.converts_md_to_html(util.get_entry(entry_title))
            })


            # If form is not valid
        else:
            return render(request, "encyclopedia/newentry.html",{
            "new_entry_form": NewWikiForm()
            })
    
    return render(request, "encyclopedia/newentry.html", {
            "new_entry_form": NewWikiForm()
        })



# Handles returning of a random entry page
def random_entry(request):
    saved_entries = util.list_entries()
    random_int = randint(0, len(saved_entries) - 1)
    random_entry = saved_entries[random_int].lower()

    print(random_entry)
    return render(request, "encyclopedia/entrypage.html", {
        "title": random_entry,
        "content": util.converts_md_to_html(util.get_entry(random_entry))
    })





# Handles entry editing
def edit_entry(request, prefix):

    # If GET request is invoke
    if request.method == "GET":
        if prefix is not None:
            entry_description = util.get_entry(prefix)
            initial = {'entry_description': entry_description}
            return render(request, "encyclopedia/edit.html", {
                "title": prefix.lower(),
                "edit_form": EditWikiForm(initial=initial)
            })
        else:
            return render(request, "encyclopedia/err.html", {
            "msg": "Hmm, something went wrong."
        })
    # else it is POST request
    else:
        edit_form = EditWikiForm(request.POST)
        if edit_form.is_valid():
            new_description = edit_form.cleaned_data["entry_description"]
            util.save_entry(prefix.capitalize(), str(new_description))
            title = prefix.lower()
            content = util.get_entry(prefix)
            return render(request, "encyclopedia/entrypage.html", {
                "title": title,
                "content": util.converts_md_to_html(content)
            })
        # If form is not valid
        else:
            return render(request, "encyclopedia/err.html", {
                "msg": "Hmm, something went wrong."
            })

