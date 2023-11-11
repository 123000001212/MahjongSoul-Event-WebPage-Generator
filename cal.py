import pandas as pd
import os
import warnings
from tqdm import tqdm
from config import *
from gen_html import gen_html
warnings.filterwarnings("ignore")

def deal_name_changes(name):
    if name=='天才呆黑魔魔':
        return '胡乱思维的猫'
    return name


def cal():
    # 出场次数	总得分	一位率	二位率	三位率	四位率  总局数  和牌率  放铳率  立直率  副露率  自摸率
    data=[[0,0,0,0,0,0,0,0,0,0,0,0] for i in range(player_number)]

    file_name = 'player.xlsx'
    frame=pd.read_excel(file_name)
    dic={}
    team_has_player=[[] for _ in range(10)]
    for i in range(len(frame['id'])):
        dic[str(frame['name'][i])]=frame['id'][i]
        team_has_player[int(frame['team_id'][i])].append(int(frame['id'][i]))

    data_filenames=None
    for root, dirs, files in os.walk('./data'):
        data_filenames=[root+'/'+f for f in files]
    #print(data_filenames)

    # 顺位马见config.add_score
    for path in tqdm(data_filenames):
        frame1=pd.read_excel(path)
        scores=[0,0,0,0]

        for i in range(4):
            playerid=dic[deal_name_changes(str(frame1['帐户名'][i]))]
            place=int(frame1['名次'][i])
            scores[i]=add_score[place-1]+(int(frame1['标准分之和'][i])-init_score)/1000
            data[playerid][0]+=1
            data[playerid][place+1]+=1
            data[playerid][6]+=frame1['局数'][i]
            data[playerid][7]+=frame1['和了数'][i]
            data[playerid][8]+=frame1['放銃数'][i]
            data[playerid][9]+=frame1['立直数'][i]
            data[playerid][10]+=frame1['副露数'][i]
            data[playerid][11]+=frame1['自摸数'][i]
            
        if has_tie:
            # 同分则平分点数
            for m in range(4):
                for n in range(m+1,4):
                    if int(frame1['标准分之和'][m])==int(frame1['标准分之和'][n]):
                        scores[m]=scores[n]=(scores[m]+scores[n])/2
        for i in range(4):
            playerid=dic[deal_name_changes(str(frame1['帐户名'][i]))]
            data[playerid][1]+=scores[i]


    for i in range(player_number):
        frame['出场次数'][i]=data[i][0]
        frame['总得分'][i]=data[i][1]
        frame['一位率'][i]=str(round(data[i][2]/data[i][0]*100,2))+'%' if data[i][0]!=0 else "0.0%"
        frame['二位率'][i]=str(round(data[i][3]/data[i][0]*100,2))+'%' if data[i][0]!=0 else "0.0%"
        frame['三位率'][i]=str(round(data[i][4]/data[i][0]*100,2))+'%' if data[i][0]!=0 else "0.0%"
        frame['四位率'][i]=str(round(data[i][5]/data[i][0]*100,2))+'%' if data[i][0]!=0 else "0.0%"
        frame['总局数'][i]=data[i][6]
        frame['自摸率'][i]=str(round(data[i][11]/data[i][7]*100,2))+'%' if data[i][7]!=0 else "0.0%"
        frame['和牌率'][i]=str(round(data[i][7]/data[i][6]*100,2))+'%' if data[i][6]!=0 else "0.0%"
        frame['放铳率'][i]=str(round(data[i][8]/data[i][6]*100,2))+'%' if data[i][6]!=0 else "0.0%"
        frame['立直率'][i]=str(round(data[i][9]/data[i][6]*100,2))+'%' if data[i][6]!=0 else "0.0%"
        frame['副露率'][i]=str(round(data[i][10]/data[i][6]*100,2))+'%' if data[i][6]!=0 else "0.0%"
        


    scores=team_init_score
    for i in range(player_number):
        for j in range(len(team_name)):
            if i in team_has_player[j]:
                scores[j]+=data[i][1]


    names=team_name
    df = pd.DataFrame([[names[i],scores[i]]for i in range(len(team_name))],index=[i for i in range(len(team_name))],columns=['team_name', 'score'])

    with pd.ExcelWriter('output.xlsx') as writer: 
        frame.to_excel(writer,sheet_name='player')
        df.to_excel(writer , sheet_name='team')

    with pd.ExcelWriter('./koala/output.xlsx') as writer: 
        frame.to_excel(writer,sheet_name='player')
        df.to_excel(writer , sheet_name='team')

if __name__=='__main__':
    cal()
    gen_html()
