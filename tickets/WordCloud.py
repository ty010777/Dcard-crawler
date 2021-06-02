#encoding=utf-8
from scrapers import Dcard
from wordcloud import WordCloud  #用於製作文字雲，要去安裝套件
import jieba # 用於句子切割，要去安裝套件
import multidict
import os
import re
import time

d = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
font = os.path.join(d, 'NotoSansCJKtc-Regular.otf')
dict_file = os.path.join(d,'jieba-dict.txt')
jieba.load_userdict(dict_file)

stopwords = {"，", "一直", "了", "也", "大家", "小姐", "已", "之", "什麼", "巴", "比", "他", "他們", "以", "以", "只是", "可", "可以", "可是", "用", "由於", "先生", "向", "因為", "在", "在內", "地", "好", "有", "有些", "而且", "自", "似的", "但是", "你", "你們", "吧", "我", "我們", "把", "更", "那", "那麼", "那邊", "來說", "依", "到", "呢", "和", "所以", "於", "於", "的", "的話", "阿", "很", "怎麼", "是", "為了", "們", "哦", "恩", "拿", "般", "除", "啊", "啦", "得", "從", "從", "這", "這邊", "都", "最", "喔", "就", "等", "等等", "給", "著", "嗎", "嗯", "當", "跟", "過", "對於", "與", "靠", "還有", "關於", "囉", "讓", "蠻", "呀"}

def getFrequencyDictForText(post):
    freq = multidict.MultiDict()
    tmpDict = {}

    r1 = '[-a-zA-Z0-9\s./:：︰﹕;<=>?@，。?★、…⋯【】（）﹙﹚《》「」？“”‘’！[\\]^_`{|}~～﹋, ’!"#$%&\'()*+]+'
    post = re.sub(r1,'，',post)

    for text in jieba.cut(post):
        text = text.lower()
        print("text = " + text )
        print("len(text) = "+ str(len(text)))
        if (text in stopwords) or (len(text) == 1):

            continue
        freq[text] = freq.get(text, 0) + 1
    print({i : k for i , k in freq.items() })
    return freq

def makeImage(filename,text):
    # https://amueller.github.io/word_cloud/auto_examples/frequency.html
    if not text:
        return
    wc = WordCloud(
        background_color='white', #背景顏色
        max_words=200,      #文字雲顯示最多幾個字詞
        max_font_size=50,     #最多字詞大小
        min_font_size=3,     #最少字詞大小
        font_path=font,      #字形，是中文一定要+
        # mask=mask_image,     #想放特定圖片才要+
        scale=3,          #文字雲解析度，3左右就夠高了
        collocations=False,    #避免重複字詞
        colormap="Dark2"      #字體顏色
    )
    wc.generate_from_frequencies(text)
    wc.to_file(os.path.join(d,f"./static/images/wordcloud/{filename}.png"))

if __name__ == "__main__":
    forums = [{'alias':'relationship'}]
    # forums = Dcard.fetch_forums()
    for forum in forums:
        try:
            posts = Dcard.fetch_posts(forum["alias"])
            tmp = []
            for post in posts:
                try:
                    post = Dcard.fetch_post(post["id"])
                    tmp += post["content"]
                except Exception as e:
                    print(e)
                time.sleep(0.5)
            # print('。'.join(tmp).encode("utf8").decode("cp950", "ignore"))
            # break
            makeImage(forum["alias"],getFrequencyDictForText('。'.join(tmp)))
        except Exception as e:
            print(e)
        break

