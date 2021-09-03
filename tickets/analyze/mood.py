#Sentimentdict.csv也要放在同個資料夾中呦
# coding=utf-8
import pandas
import jieba
'''
三函數流程:
analyze(正向+1/負向-1)
->hasOpposite(看有沒有反義字,有:分數正負相反/沒有:不變)
->getDegree(權重詞判斷)
->return 分數
'''
class mood:


    #讀Sentimentdict.csv的內容並建立相對應的集合
    def get_mood(text):
        def analyze(positives_set,negatives_set,not_set,degree_dict,token):
            def hasOpposite(wordlist):
                for word in wordlist:
                    if word in not_set:
                        return True
                return False
            def getDegree(wordlist):
                degree =1.0
                for word in wordlist:
                    if word in degree_dict:
                        degree = degree_dict[word]
                return degree

            sum  = 0
            for word in token:
                if word.lower() in positives_set:
                    sum += 1
                elif word.lower() in negatives_set:
                    sum -= 1

            if hasOpposite(token):
                sum = - sum

            sum = sum * getDegree(token)
            return sum
        mydata = pandas.read_csv("C:/Users/陳錫彬/Desktop/新增資料夾/SentimentDict.csv")
        positives_set=set(mydata['positive'])
        negatives_set = set(mydata['negative'])
        not_set = set(mydata['not'])

        degree_dict = {}
        for word in mydata['degree-1']:
            degree_dict[word] = 1.8
        for word in mydata['degree-2']:
            degree_dict[word] = 1.6
        for word in mydata['degree-3']:
            degree_dict[word] = 1.4
        for word in mydata['degree-4']:
            degree_dict[word] = 1.2
        for word in mydata['degree-5']:
            degree_dict[word] = 1.1
        for word in mydata['degree-6']:
            degree_dict[word] = 0.9

        #這裡應該放jieba自訂詞庫的，只是我這裡不曉得怎麼放W，靠你惹

        # text = "大大大優惠" 內容會從scraper傳入
        token = list(jieba.cut(text)) #分詞
        score = analyze(positives_set,negatives_set,not_set,degree_dict,token) #return的值
        #print("情感分數：",score)

        #這裡print看要不要改成emoji符號
        if score > 20:
            return '非常正向 分數:{}'.format(round(score ,1))
        elif score > 0:
            return '輕微正向 分數:{}'.format(round(score ,1))
        elif score > -20:
            return '輕微負向 分數:{}'.format(round(score ,1))
        elif score < -20:
            return '非常負向 分數:{}'.format(round(score ,1))
        else :
            return '普普通通 分數:{}'.format(round(score ,1))
