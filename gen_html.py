import time
from util import gen_teamData,gen_playerData,gen_roundData
import pandas as pd
import warnings
from config import *
warnings.filterwarnings("ignore")


def index(html):
    update_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
    html=html.replace('!!update_time',"'"+update_time+"'")
    html=html.replace('!!genteamData',gen_teamData())
    html=html.replace('!!genplayerData',gen_playerData())
    html=html.replace('!!genroundData',gen_roundData())
    html=html.replace('!!eventName',event_name)
    f=open("./game_rule.txt",'r',encoding='utf-8')
    game_rule=f.read()
    game_rule=game_rule.replace('\n','<br/>')
    html=html.replace('!!gameRule',game_rule)
    return html

def player(html):
    df=pd.read_excel('./koala/output.xlsx',sheet_name='player')
    res=[]
    for req_id in range(player_number):
        data=[]
        times=int(df['出场次数'][req_id])
        data.append(times) # 0
        c1=int(round(times*int(float(df['一位率'][req_id][:-1]),)/100,0))
        c2=int(round(times*int(float(df['二位率'][req_id][:-1]),)/100,0))
        c3=int(round(times*int(float(df['三位率'][req_id][:-1]),)/100,0))
        c4=int(round(times*int(float(df['四位率'][req_id][:-1]),)/100,0))
        data.append(str(df['name'][req_id]))# 1
        data.append(str(df['team_name'][req_id]))# 2
        data.append(str(c1))# 3
        data.append(str(c2))# 4
        data.append(str(c3))# 5
        data.append(str(c4))# 6
        data.append(str(df['出场次数'][req_id]))# 7
        data.append(str(df['总局数'][req_id]))# 8
        data.append(str(round(df['总得分'][req_id],1)))# 9
        data.append(str(df['和牌率'][req_id]))# 10
        data.append(str(df['放铳率'][req_id]))# 11
        data.append(str(df['自摸率'][req_id]))# 12
        data.append(str(df['副露率'][req_id]))# 13
        data.append(str(df['立直率'][req_id]))# 14
        avg=0 if times==0 else round((c1+c2*2+c3*3+c4*4)/times,2)
        data.append(str(avg))# 15
        res.append(data)
    html=html.replace("!!playerdetailData",str(res))
    return html

def gen_html():
    f=open('DLindex.html','r',encoding='utf-8')
    html=f.read()
    f.close()
    html=index(html)
    html=player(html)
    f=open('index.html','w',encoding='utf-8')
    f.write(html)
    f.close()
