from django.db.models import query
from django.shortcuts import render
import requests
from .scrapers import Dcard
from tickets.models import CrawledData
from .filter import DataFilter
from .serializers import TicketsSerializer
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from rest_framework import views, viewsets,filters,pagination
from rest_framework.pagination import PageNumberPagination
from tickets.WordCloud import getFrequencyDictForText,makeImage

def index(request):
    context = {}
    dataFilter_list = DataFilter(
                        request.GET,
                        queryset=CrawledData.objects.all()
                )

    context['dataFilter'] = dataFilter_list

    paginator = Paginator(dataFilter_list.qs,5)

    try:
        page_number = request.GET.get('page') #這裡設定頁數 ('page',n)= 第n頁
        DataPage = paginator.get_page(page_number)

    except EmptyPage as e:
        DataPage = paginator.page(1)
    except PageNotAnInteger:
        DataPage = paginator.page(1)

    context['DataPage'] = DataPage

    return render(request, 'tickets/index.html', context)

def Make_one_cloud(request):
    # 下次想嘗試用以前objects.filter的方式來擷取資料庫篩選
    #在製作成文字雲 阿 記得做跳出視窗的功能。
    temp =""
    dataFilter_list = DataFilter(
                        request.GET,
                        queryset=CrawledData.objects.all()
                )
    paginator = Paginator(dataFilter_list.qs,10000)
    DataPage = paginator.get_page(1)
    for ticket in DataPage:
        temp += ticket.cContent


    makeImage("Search",getFrequencyDictForText('。'.join(temp)))
    return render(request, 'tickets/insert.html')


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
                cContent = ticket['content'],
                cTag = ticket['topics'],
                link=ticket['link'],
                img=ticket['img'],
                mood=ticket['mood']
                )

            unit.save()

        return render(request, 'tickets/insert.html')


class TicketsViewSet(viewsets.ModelViewSet):
    queryset = CrawledData.objects.all()
    serializer_class = TicketsSerializer

class  MyPagination(PageNumberPagination):
    # 指定每一页的个数，默认为配置文件里面的PAGE_SIZE
    page_size =  10

    # 可以让前端指定每页个数，默认为空，这里指定page_size去指定显示个数
    page_size_query_param =  'page_size'

    # 可以让前端指定页码数，默认就是page参数去接收
    page_query_param =  'page'

    # 指定返回格式，根据需求返回一个总页数，数据存在results字典里返回
    def get_paginated_response(self, data):
        from collections import OrderedDict
        return render(OrderedDict([('count', self.page.paginator.count), ('results',data)]))
