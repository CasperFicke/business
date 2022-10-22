# core/views.py

from django.shortcuts import render
from django.views import generic

# home view
# classbased view 
class HomeView(generic.TemplateView):
	"""
    Website home page.

    **Template:**

    :template:`core/index.html`
    """
	template_name = "core/index.html"


