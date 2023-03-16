import pandas as pd
import os
from config import *

def gen_teamData():
    res='['
    df=pd.read_excel('./koala/output.xlsx',sheet_name='team')
    for i in range(len(df['team_name'])):
        part="{name: '"+str(df['team_name'][i])+"',score: "+str(round(df['score'][i],1))+'},'
        res+=part
    res+=']'
    return res

def gen_playerData():
    res='['
    df=pd.read_excel('./koala/output.xlsx',sheet_name='player')
    for i in range(len(df['id'])):
        part="{name: '"+str(df['name'][i])+"',score: "+str(round(df['总得分'][i],1))+",team: '"+str(df['team_name'][i])+"',id:'"+str(df['id'][i])+"'},"
        res+=part
    res+=']'
    return res
def indexof(l,a):
    for i in range(len(l)):
        if a==l[i]:
            return i
    return -1
def handle_same_score(df,i):
    # 处理同分情况
    if has_tie==False: # 无同分规则直接返回0
        return 0
    spec=0
    if df['1位得分'][i]-df['2位得分'][i]<=40.01:
        df['1位得分'][i]=df['2位得分'][i]=(df['1位得分'][i]+df['2位得分'][i])/2
        spec=2
    if df['2位得分'][i]-df['3位得分'][i]<=20.01:
        df['2位得分'][i]=df['3位得分'][i]=(df['2位得分'][i]+df['3位得分'][i])/2
        spec=3
    if df['3位得分'][i]-df['4位得分'][i]<=20.01:
        spec=4
        df['3位得分'][i]=df['4位得分'][i]=(df['3位得分'][i]+df['4位得分'][i])/2
    return spec
def gen_roundData(player=None):
    gen_roundxlsx()
    res='['
    df=pd.read_csv('./temp_data/雀魂牌譜記錄.csv',header=0,encoding='utf-8')

    if player is None:
        for i in range(len(df['開始時間'])):
            handle_same_score(df,i)
            result=str(df['1位昵稱'][i])+'('+str(round(float(df['1位得分'][i]),1))+')， '+str(df['2位昵稱'][i])+'('+str(round(float(df['2位得分'][i]),1))+')， '+str(df['3位昵稱'][i])+'('+str(round(float(df['3位得分'][i]),1))+')， '+str(df['4位昵稱'][i])+'('+str(round(float(df['4位得分'][i]),1))+')'
            link="https://game.maj-soul.net/1/?paipu="+str(df['牌譜鏈接'][i])
            part="{date: '"+str(df['結束時間'][i])+"',result:'"+result+"',link:'"+link+"'},"
            res+=part
        res+=']'
        return res
    # no use
    else:
        for i in range(len(df['開始時間'])):
            spec=handle_same_score(df,i)
            print(spec)
            names=[df['1位昵稱'][i],df['2位昵稱'][i],df['3位昵稱'][i],df['4位昵稱'][i]]
            if player in names:
                result=str(df['1位昵稱'][i])+'('+str(round(float(df['1位得分'][i]),1))+')， '+str(df['2位昵稱'][i])+'('+str(round(float(df['2位得分'][i]),1))+')， '+str(df['3位昵稱'][i])+'('+str(round(float(df['3位得分'][i]),1))+')， '+str(df['4位昵稱'][i])+'('+str(round(float(df['4位得分'][i]),1))+')'
                link="https://game.maj-soul.net/1/?paipu="+str(df['牌譜鏈接'][i])
                place=['一','二','三','四'][indexof(names,player)]
                if spec==2 and indexof(names,player)==1:
                    place='一'
                if spec==3 and indexof(names,player)==2:
                    place='二'
                if spec==4 and indexof(names,player)==3:
                    place='三'
                part="{date: '"+str(df['結束時間'][i])+"',result:'"+result+"',link:'"+link+"',place:'"+place+"'},"
                res+=part
        res+=']'
        return res

def gen_roundxlsx():
    res={}
    res['開始時間']=[]
    res['結束時間']=[]
    res['1位昵稱']=[]
    res['2位昵稱']=[]
    res['3位昵稱']=[]
    res['4位昵稱']=[]
    res['1位得分']=[]
    res['2位得分']=[]
    res['3位得分']=[]
    res['4位得分']=[]
    res['牌譜鏈接']=[]
    data_filenames=None
    for root, dirs, files in os.walk('./data'):
        data_filenames=[root+'/'+f for f in files]

    # 顺位马见config.add_score
    for path in data_filenames:
        frame1=pd.read_excel(path)
        names=[]
        scores=[0,0,0,0]
        place=[]
        for i in range(4):
            names.append(str(frame1['帐户名'][i]))
            p=int(frame1['名次'][i])
            place.append(p)
            scores[i]=round(add_score[p-1]+(int(frame1['标准分之和'][i])-init_score)/1000,1)
        #print(names,scores,place)
        res['開始時間'].append(path.split('/')[-1].split('-')[0])
        res['結束時間'].append(path.split('/')[-1].split('-')[0])
        res['1位昵稱'].append(names[indexof(place,1)])
        res['2位昵稱'].append(names[indexof(place,2)])
        res['3位昵稱'].append(names[indexof(place,3)])
        res['4位昵稱'].append(names[indexof(place,4)])
        res['1位得分'].append(scores[indexof(place,1)])
        res['2位得分'].append(scores[indexof(place,2)])
        res['3位得分'].append(scores[indexof(place,3)])
        res['4位得分'].append(scores[indexof(place,4)])
        res['牌譜鏈接'].append(str(frame1['gameID'][0]))
    df=pd.DataFrame(data=res)
    df.to_csv('./temp_data/雀魂牌譜記錄.csv',encoding='utf-8',index=0)
if __name__=='__main__':
    gen_roundxlsx()
