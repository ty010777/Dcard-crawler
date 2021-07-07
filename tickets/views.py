from django.shortcuts import render
from .scrapers import Dcard


def index(request):

    forums = Dcard.fetch_forums()
    toalias = {forum['name'] : forum['alias'] for forum in forums}
    alias = toalias.get(request.POST.get("kanban_name"))

    context = {}
    if alias:
        # posts = Dcard.fetch_posts(alias)

        context['tickets'] = Dcard.fetch_posts(alias)
        # print(context['tickets'])

    return render(request, "tickets/index.html", context)



