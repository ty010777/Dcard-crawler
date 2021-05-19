from django.shortcuts import render
from .scrapers import Dcard


def index(request):

    dcard = Dcard(request.POST.get("kanban_name"))

    context = {
        "tickets": dcard.scrape(dcard.catch_kanban())
    }

    return render(request, "tickets/index.html", context)



def catch(request):

    dcard = Dcard(request.POST.get("kanban_name"))


    A = WordCloud(dcard.scrape(dcard.catch_article()))

    context = {

        "articles":A

    }


    return render(request, "tickets/WordCloud.html", context)

