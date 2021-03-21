import markdown2 # needed for markdown.convert function. There is a markdown3 but using 2. 
import secrets # Needed for the random function to work correctly.

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# import from same dir (.) util for reference in this page: great for repetition and keeping code neat.
from . import util
from markdown2 import Markdown # being explicit.

# New Entry form using Django forms functions hence 'forms.CharField' etc.
class NewEntryForm(forms.Form):
	title = forms.CharField(label="Entry Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}))
	content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))
	edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

# renders index page on call.
def index(request):
	return render(request, "encyclopedia/index.html", {
		"entries": util.list_entries()
	})

# takes entry and uses markdown.convert function if entry page is not none otherwise - shows a corgi error page.
def entry(request, entry):
	markD = Markdown()
	entryPage = util.get_entry(entry)
	if entryPage is None:
		return render(request, "encyclopedia/nonExistingEntry.html",{
			"entryTitle": entry
		})
	else:
		return render(request, "encyclopedia/entry.html", {
			"entry": markD.convert(entryPage),
			"entryTitle": entry
		})
# new Entry takes Post request with kickout logic based on status. Bools used as flags.
def newEntry(request):
	if request.method == "POST":
		form = NewEntryForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			content = form.cleaned_data["content"]
			if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
				util.save_entry(title, content)
				return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
			else:
				return render(request, "encyclopedia/newEntry.html", {
				"form": form,
				"existing": True,
				"entry": title
				})
		else:
			return render(request, "encyclopedia/newEntry.html",{
			"form": form,
			"existing": False
			})
	else:
		return render(request, "encyclopedia/newEntry.html",{
		"form": NewEntryForm(),
		"existing": False
		})

# edit request takes in 'entry' and allows users to edit form.fields if it exists otherwise error corgi picture.
def edit(request, entry):
	entryPage = util.get_entry(entry)
	if entryPage is None:	
		return render(request, "encyclopedia/nonExistingEntry.html", {
			"entryTitle": entry
		})
	else:
		form = NewEntryForm()
		form.fields["title"].initial = entry
		form.fields["title"].widget = forms.HiddenInput()
		form.fields["content"].initial = entryPage
		form.fields["edit"].initial = True
		return render(request, "encyclopedia/newEntry.html", {
			"form": form,
			"edit": form.fields["edit"].initial,
			"entryTitle": form.fields["title"].initial
		})

# random page request called using the 'secrets' library. 
def random(request):
	entries = util.list_entries()
	randomEntry = secrets.choice(entries)
	return HttpResponseRedirect(reverse("entry", kwargs={'entry': randomEntry}))

# search function takes user input and checks against eisting list. 
# Note how it calls list_entries() for example from the util.py reusable code for convenience. 
# first part handles the logic for complete entry, second partial matches using for loop and 3rd returns values and renders them from the logic.
def search(request):
	value = request.GET.get('q', '')
	if(util.get_entry(value) is not None):
		return HttpResponseRedirect(reverse("entry", kwargs={'entry': value}))
	else:
		subStringEntries=[]
		for entry in util.list_entries():
			if value.upper() in entry.upper():
				subStringEntries.append(entry)
		
		return render(request,"encyclopedia/index.html", {
		"entries": subStringEntries,
		"search": True,
		"value": value
	})

