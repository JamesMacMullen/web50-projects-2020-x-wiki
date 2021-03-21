import django
from . import views
from django.urls import path

# url paths used by the application encyclopedia.
# Please remember when making new pages to add the path reference here.
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
	path("newEntry", views.newEntry, name="newEntry"),
	path("wiki/<str:entry>/edit", views.edit, name="edit"),
	path("random", views.random, name="random"),
	path("search", views.search, name="search")
	# Testing something below that is not needed
	#path("<str:title>", views.entry, name="entry")
]
