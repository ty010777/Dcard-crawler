from logging import error
import requests
import cloudscraper


headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
# Dcard網站
class Dcard:
    @staticmethod
    def fetch_forums():
        url = 'https://www.dcard.tw/service/api/v2/forums'#爬看板API

        forums = cloudscraper.create_scraper().get(url, headers=headers).json()

        # forums.toName = {forum['alias'] : forum['name'] for forum in forums}
        # forums.toAlias = {forum['name'] : forum['alias'] for forum in forums}

        #KEYS : VALUE  => alias : name

        return forums
    @staticmethod
    def fetch_posts(forum):
        if not forum:  # 如果名稱非空值
            raise TypeError("forum is required")

        url = f'https://www.dcard.tw/service/api/v2/forums/{forum}/posts?popular=true&limit=5'
        #https://www.dcard.tw/service/api/v2/forums/trending/posts?popular=true&limit=20


        posts = cloudscraper.create_scraper().get(url, headers=headers).json()
        # return posts
        for post in posts:
            post['img'] = (post['mediaMeta'][0]['url'] if len(post['mediaMeta']) else 'https://i.imgur.com/Ewmac29.jpg')
            post['link'] = f'https://www.dcard.tw/f/{post["forumAlias"]}/p/{post["id"]}'


        return posts

    @staticmethod
    def fetch_post(postId): # 單一文章
        if not postId :
            raise TypeError("post is required")

        # https://www.dcard.tw/service/api/v2/posts/236038749
        url = f'https://www.dcard.tw/service/api/v2/posts/{postId}'
        # print(url)
        post = requests.get(url).json()    # 回傳結果
        # print(type(post))
        post['img'] = (post['mediaMeta'][0]['url'] if len(post['mediaMeta']) else 'https://i.imgur.com/Ewmac29.jpg')

        post['link'] = f'https://www.dcard.tw/f/{post["forumAlias"]}/p/{postId}'

        return {i : post[i] for i in ['title','forumAlias', 'commentCount', 'topics', 'link', 'likeCount', 'img','excerpt','content']}

# print(Dcard.fetch_posts('trending'))
