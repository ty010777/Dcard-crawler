#encoding=utf-8
import multidict as multidict
import jieba  #用於句子切割，要去安裝套件
import os
from os import path
from wordcloud import WordCloud  #用於製作文字雲，要去安裝套件
import matplotlib.pyplot as plt  #輸出文字雲圖片
import numpy as np  #文字雲如果要有特定圖片才需import這行，有沒有內建就不知了W
from PIL import Image
from wordcloud import ImageColorGenerator
from scrapers import Dcard
import re
import time



#快取 資料庫
#從資料庫抓資料產生標籤雲
#更新頻率不可超高
#每分鐘跑一次,每分鐘重抓一次
#存入images
#每天更新一次的文字雲:>



# text = "articles"  #將爬取該看板的所有標題組成一串句子丟進去
# s = ' '.join(jieba.cut(text)) #句子切割

# font = 'C:\\Users\\陳錫彬\Desktop\\依樣畫葫蘆版part2文字雲\\tickets\\NotoSansCJKtc-Regular.otf' #由於是中文，所以要載字型，我有包給你

# # Mask image 有特定圖片才需以下註解的這幾行
# # '''

# mask_color = np.array(Image.open('C:\\Users\\陳錫彬\\Desktop\\依樣畫葫蘆版part2文字雲\\tickets\\static\\images\\cat.jpg')) #('')中要放圖片
# mask_color = mask_color[::3, ::3]
# mask_image = mask_color.copy()
# mask_image[mask_image.sum(axis=2) == 0] = 255
# # '''

#特定字詞  要過濾特定字才需要用到
#stopwords = set(STOPWORDS)
#stopwords.add("")

#文字雲



# cloud = WordCloud(

#           background_color='white', #背景顏色
#           #max_words=2000,      #文字雲顯示最多幾個字詞
#           max_font_size=50,     #最多字詞大小
#           min_font_size=3,     #最少字詞大小
#           font_path=font,      #字形，是中文一定要+
#           mask=mask_image,     #想放特定圖片才要+
#           scale=3,          #文字雲解析度，3左右就夠高了
#           collocations=False,    #避免重複字詞
#           #stopwords=stopwords    #停用詞
#           colormap="Dark2"      #字體顏色
#           ).generate(s)

# # Create coloring from image 有特定圖片才需以下註解的這幾行

# image_colors = ImageColorGenerator(mask_color)#根據特定圖片設定其文字顏色
# cloud.recolor(color_func=image_colors)

# plt.figure(dpi=200) #圖片放大
# plt.axis('off')   #關座標
# plt.imshow(cloud)
# plt.show()
# cloud.to_file('C:\\Users\\陳錫彬\\Desktop\\依樣畫葫蘆版part2文字雲\\tickets\\static\\images\\寵物效果圖.png')


d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
stopwords = {"之","的","從","自","當","於","在","於","從","向","把","給","讓","用","以","拿","靠","依","由於","為了","對於","關於","與","和","比","除","了","似的","在內","地","得","來說","的話","著","等","等等","般","過","你","我","他","你們","他們","我們","大家","先生","小姐","也","囉","已","更","以","因為","所以","可以","這邊","那邊","一直","有","都","們","到","就","只是","但是","可是","而且","怎麼","那麼","什麼","還有","啊","阿","最","呢","嗎","是","蠻","吧","巴","很","跟","可","那","這","哦","喔","恩","嗯","好","有些","，"}
font = path.join(d, 'NotoSansCJKtc-Regular.otf')

def getFrequencyDictForText(post):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}

    r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-./:：︰﹕;<=>?@，。?★、…【】（）﹙﹚《》？“”‘’！[\\]^_`{|}~～﹋]+'
    post = re.sub(r1,'，',post)

    for text in jieba.cut(post):
        if text in stopwords:
            continue

        fullTermsDict.add(text.lower(), 1)

    return fullTermsDict


def makeImage(filename,text):
    # https://amueller.github.io/word_cloud/auto_examples/frequency.html
    if not text :
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
    wc.to_file(path.join(d,f"./static/images/wordcloud/{filename}.png"))




if __name__ == "__main__":

    forums = Dcard.fetch_forums()
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

