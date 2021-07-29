from django.shortcuts import render
from .scrapers import Dcard
from tickets.models import CrawledData
from .filter import DataFilter
def index(request):

    datas = CrawledData.objects.all()

    dataFilter = DataFilter(queryset=datas)

    if request.method == "POST":
        dataFilter = DataFilter(request.POST, queryset=datas)

    context = {
        'dataFilter': dataFilter
    }

    return render(request, 'tickets/index.html', context)

def insert(request):
    forums = Dcard.fetch_forums()
    toalias = {forum['name'] : forum['alias'] for forum in forums}
    alias = toalias.get(request.POST.get("kanban_name"))

    context = {}
    if alias:
        context['tickets'] = Dcard.fetch_posts(alias)
        # print(context['tickets'])
        for ticket in context['tickets']:
            try:
                if(CrawledData.objects.get(num = ticket['id'])):
                    continue
            except:
                pass
            unit = CrawledData.objects.create(
                num = ticket['id'],
                cTitle=ticket['title'],
                cForumAlias=ticket['forumAlias'],
                cForumName = ticket['forumName'],
                cCommentCount=ticket['commentCount'],
                cLikeCount=ticket['likeCount'],
                cExcerpt = ticket['excerpt'],
                cTag = ticket['topics'],
                link=ticket['link'],
                img=ticket['img']

                )

            unit.save()

        return render(request, 'tickets/insert.html')

# def listall(request):
#     tickets = CrawledData.objects.all().order_by('cLikeCount')
#     #讀取資料表, 依 id 遞增排序(欄位前加入負號-id代表遞減排序)
#     return render(request, "listall.html", locals())