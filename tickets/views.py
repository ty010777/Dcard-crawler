from django.shortcuts import render
from .scrapers import Dcard
from tickets.models import CrawledData
from .filter import DataFilter
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

def index(request):

    # datas = CrawledData.objects.all()
    # datas=getPage(request,datas)

    # dataFilter = DataFilter(queryset=datas)
    context = {}
    dataFilter_list = DataFilter(
                        request.POST,
                        queryset=CrawledData.objects.all()
                )

    context['dataFilter'] = dataFilter_list

    paginator = Paginator(dataFilter_list.qs,5)
    try:
        page_number = request.GET.get('p') #這裡設定頁數 ('page',n)= 第n頁
        DataPage = paginator.get_page(page_number)
    except EmptyPage as e:
        DataPage = paginator.page(1)
    except PageNotAnInteger:
        DataPage = paginator.page(1)

    context['DataPage'] = DataPage
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


