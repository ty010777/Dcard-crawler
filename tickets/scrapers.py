from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
from datetime import datetime
#依樣畫葫蘆版


# 票券網站抽象類別
class Website(ABC):
    def __init__(self, kanban_name):
        self.kanban_name = kanban_name  # 看版名稱屬性

    @abstractmethod
    def scrape(self):  # 爬取文章抽象方法
        pass

    def catch_kanban(self,kanban):
        self.kanban = kanban
        pass
    def catch_article(self):
        pass

# Dcard網站
class Dcard(Website):
    kanban = {} #所有看板(k:看板名，v:別名)
    article = {} #所有文章(k:自訂編號，v:[0]:文章ID、[1]:標題)
    url = 'https://www.dcard.tw/service/api/v2/forums'#爬看板API
    requ = requests.get(url)
    rejs = requ.json()
    def catch_kanban(self):
        # self.User_input_kanban = User_input_kanban
        for i in self.rejs:
            self.kanban[i.get('name')] = i.get('alias')
        return self.kanban


    def scrape(self,kanban):
        result = []  # 回傳結果
        if self.kanban_name:  # 如果城市名稱非空值
            # return self.kanban[self.kanban_name]

            rejs = requests.get(
                f'https://www.dcard.tw/service/api/v2/forums/{self.kanban[self.kanban_name]}/posts').json()
            # https://www.dcard.tw/service/api/v2/forums/pet/posts
            # return rejs
            # soup = BeautifulSoup(response.text, "lxml")
            # return soup.prettify()
            # 取得十個票券卡片(Card)元素
            # activities = soup.find_all(
                # "div", {"class", "j_activity_item_link j_activity_item_click_action"}, limit=10)

            for activity in rejs:

                # 標題名稱
                title = activity['title']

                link = f'https://www.dcard.tw/f/{self.kanban[self.kanban_name]}/p/' + str(activity['id'])

                #https://www.dcard.tw/f/pet/p/235864182

                commentCount = activity['commentCount']

                topics = activity['topics']

                likecount = activity['likeCount']

                if len(activity['mediaMeta']):
                    media = activity['mediaMeta'][0]["url"]
                else:
                    media = '/static/images/noPicture.jpg'
                # 儲存串列 去中括號
                # Current_Kanban = activity['forumName']

                result.append(
                    dict(
                        title=title,#標題
                        commentCount = commentCount,#留言
                        topic = topics,#標籤
                        link = link,#超連結
                        likecount = likecount ,#按讚數
                        media = media #縮圖
                    )
                )


            return result



    def catch_article(self):

        rejs = requests.get(
                f'https://www.dcard.tw/service/api/v2/forums/{self.kanban[self.kanban_name]}/posts').json()

        for activity in rejs:
            excerpt = activity['excerpt']


        return excerpt

