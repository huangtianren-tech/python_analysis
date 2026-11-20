from django.http import JsonResponse    #将后端数据以Json格式返回给前端
from django.template.backends import django
from typing import Any  #导入任意数据类型
from django.shortcuts import render
def hello(request: Any): #request变量，为接收前端方法、参数、请求头
    i=122408
    data = {"role":"user","info":"how are you?","content":i}
    # i+=1
    return JsonResponse(data)

# 访问前端代码时，使用render试图解析
def index(request:Any):
    return render(request = request,template_name="index.html")

from django.conf import settings #settings.py
import os #组合文件地址
import numpy as np
import pandas as pd

"""
第一个案例，红球中奖率最高的十个点数
"""
def red_balls_top10(request:Any):
    BASE = settings.BASE_DIR
    csv_path = os.path.join(BASE,"DjangoProject","web","TwoColorBall.csv")
    df = pd.read_csv(csv_path)
    # print(df)
    #构建需要获取数据的列名
    colums =["红1","红2","红3","红4","红5","红6"]
    df[colums]=df[colums].astype(int)
    # print(df[colums])
    reds = df[colums].values
    # print(res)
    all_red = reds.flatten()    #二维转为一维
    # print(all_red)
    # 将一维数组转为Serise序列,统计每个号码出现的次数（比列表多统计功能）
    red_freq = pd.Series(all_red).value_counts().sort_values(ascending=False).head(10)
    # print(red_freq)
    list1 = []
    for k,v in red_freq.items():
        list1.extend([{"number":k,"count":v}])
    # print(list1)
    # print([{"number":k,"count":v}for k,v in red_freq.items()])
    json_1={
        "msg":"ok",
        "title":"中奖率最高的十个红球",
        "data":list1,
    }
    return JsonResponse(json_1)

"""
蓝球中奖率最高的8个球-11.18
"""
def blue_ball_top8(req:Any):
    BASE = settings.BASE_DIR
    csv_path = os.path.join(BASE,"DjangoProject","web","TwoColorBall.csv")
    df = pd.read_csv(csv_path)
    colums = ["蓝球"]
    df["blue_ball"] = df[colums].astype(int)
    blue = df["blue_ball"].values
    blue_freq = pd.Series(blue).value_counts().sort_values(ascending=False).head(8)
    blue_list = []
    for k,v in blue_freq.items():
        blue_list.extend([{"number":k,"count":v}])
    # print(blue_list)
    json_2 = {
        "msg":"ok",
        "title":"中奖率最高的8个蓝球",
        "data":blue_list,
    }
    return JsonResponse(json_2)


"""
分别取出红球1号到红球6号中，中奖率最高的点数-11.18
"""
def every_red_ball_top1(req:Any):
    BASE = settings.BASE_DIR    #获取项目根目录
    csv_path = os.path.join(BASE,"DjangoProject","web","TwoColorBall.csv")
    df = pd.read_csv(csv_path)
    df["红球1号"] = df["红1"].astype(int)   #ctrl+D,将该行复制到下一行
    df["红球2号"] = df["红2"].astype(int)
    df["红球3号"] = df["红3"].astype(int)
    df["红球4号"] = df["红4"].astype(int)
    df["红球5号"] = df["红5"].astype(int)
    df["红球6号"] = df["红6"].astype(int)
    # for i in range(1,7):
    #       df["红球",i,"号"] = df["红",i].astype(int)
    red1 = df["红球1号"].values
    red2 = df["红球2号"].values
    red3 = df["红球3号"].values
    red4 = df["红球4号"].values
    red5 = df["红球5号"].values
    red6 = df["红球6号"].values
    # print(red1)
    red1 = pd.Series(red1).value_counts().sort_values(ascending = False).head(1)
    red2 =pd.Series(red2).value_counts().sort_values(ascending = False).head(1)
    red3 =pd.Series(red3).value_counts().sort_values(ascending = False).head(1)
    red4 =pd.Series(red4).value_counts().sort_values(ascending = False).head(1)
    red5 =pd.Series(red5).value_counts().sort_values(ascending = False).head(1)
    red6 =pd.Series(red6).value_counts().sort_values(ascending = False).head(1)
    lists = [red1,red2,red3,red4,red5,red6]
    # data_list = []
    # for j in lists:
    #     for i, k in j.items():
    #         # print("name:", "红球", str(i), "号", "value:" + str(k))
    #         data_list.append([{"name:""红球"+str(i)+ "号"+","+"value:" + str(k)}])
    # return JsonResponse(data_list)
    """
    for k,v in enumerate(lists):    #最前面第一个数字k是lists的列表序列
        print(k)
        print("---")
        print(v)    #这个 v 就是lists中red1到red6的键和值
        print("----")
        print(f"name:红球{k + 1}:{v.index[0]}")
        print(f"value:{v.iloc[0]}")
    # reds = [{("红球",1,"号"):k,"value":v} for k,v in lists]
    """
    data=[{"value":int(v.iloc[0]),"name":f"红球{k+1}号:{v.index[0]}"}for k,v in enumerate(lists)]
    json_3 = {
        "msg":"ok",
        "title":"中奖率最高的每个红球最高的点数",
        "data":data,
    }
    return JsonResponse(json_3)

"""
冷热号分析-11.19
"""
def cold_hot_ball(req:Any):
    BASE = settings.BASE_DIR
    csv_path = os.path.join(BASE,"DjangoProject","web","TwoColorBall.csv")
    df = pd.read_csv(csv_path)
    red_col = ["红1","红2","红3","红4","红5","红6"]
    df[red_col] = df[red_col].astype(int)
    # print(df[red_col])
    # 声明一个字典，来存储每个球号上一次出现的位置
    last_ass = {}
    for idx,row in df.iterrows():  #idx为序号，row为出现的球
        for ball in row[red_col]:
            #记录每个球出现的位置
            last_ass[ball] = idx
    # print(df)
    late_idx = df.index[-1]
    #定义冷号,近5期未出现则为冷号
    cold_ball = [ball for ball,l_idx in last_ass.items() if late_idx - l_idx >5]
    hot_ball = [ball for ball,l_idx in last_ass.items() if late_idx - l_idx <=5]
    # print(hot_ball)
    json_4 ={
        "msg":"ok",
        "title":"冷热号分析",
        "data":{
            "cold_ball":cold_ball,
            "hot_ball":hot_ball,
            "cold_name":"冷号",
            "hot_name":"热号",
        }
    }
    return JsonResponse(json_4)

def first_and_second_prizes(req:Any):
    BASE = settings.BASE_DIR
    csv_path = os.path.join(BASE,"DjangoProject","web","TwoColorBall.csv")
    df = pd.read_csv(csv_path)
    df["一等奖"] = df["一等奖"].astype(int)
    df["二等奖"] = df["二等奖"].astype(int)
    # 得到中奖注数排名前五的一等奖和二等奖
    first_prize_top5 = df["一等奖"].sort_values(ascending = False).head(5)
    second_prize_top5 = df["二等奖"].sort_values(ascending = False).head(5)
    first_prize_issue = []
    second_prize_issue = []
    first_prize_bets = []
    second_prize_bets = []
    #把期号取出来
    df["期号"] = df["期号"].astype(int)
    for k,v in first_prize_top5.items():
        first_prize_issue.append("期号"+str(df["期号"][k]))
        first_prize_bets.append(v)

    for k,v in second_prize_top5.items():
        second_prize_issue.append("期号"+str(df["期号"][k]))
        second_prize_bets.append(v)
    # print(first_prize_issue)
    # print(first_prize_bets)
    json_5 = {
        "msg":"ok",
        "title":"一、二等奖注数前5的期数",
        "data":{
            "first":{
                "issue": first_prize_issue,
                "bets": first_prize_bets,
            },
            "second":{
                "issue": second_prize_issue,
                "bets": second_prize_bets,
            }
        },
    }
    return JsonResponse(json_5)
def sales_trend(request):
    BASE = settings.BASE_DIR
    csv_path = os.path.join(BASE, "DjangoProject", "web", "TwoColorBall.csv")
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    df = df.sort_values(by="期号", ascending=True)##升序

    recent_df = df.tail(10)##截取最后十行

    x_data = recent_df["期号"].astype(str).tolist()##提取期号列表

    sales_data = []
    for val in recent_df["销售额"]:##遍历销售额的值
        sales_data.append(int(float(val)))##int化然后追加
    data_list = []
    for x, y in zip(x_data, sales_data):
        data_list.append({"issue": x, "sales": y})##合并成字典

    json_6=({
        "msg": "ok",
        "title": "最近10期销售额走势",
        "data": data_list
    })
    return JsonResponse(json_6)##打包并发送给前端

