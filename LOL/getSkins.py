#-*- coding: utf-8 -*-
import json
import logging
import os.path
import shutil
import time
import requests

# 图片存放位置,桌面/hero
file_name = r"C:\Users\admin\Desktop\hero"
# 删除原有存放图片的文件夹，然后创建新的文件夹
if os.path.exists(file_name):
    shutil.rmtree(file_name,ignore_errors=True)
os.mkdir(file_name)

# 获取英雄id
hero_id_url = r'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js?ts=2770133'
r = requests.get(url=hero_id_url)
# 解决Unicode编码问题
hero_info = r.text.encode('utf-8').decode('unicode_escape')
hero_json = json.loads(hero_info)["hero"]

# 英雄数量
hero_num = len(hero_json)
# 英雄字典{英雄名称：英雄ID}
hero_list = {}
for i in range(hero_num):
    hero_list[hero_json[i]['name']] = hero_json[i]['heroId']
# 按英雄名称创建文件夹
for name,hero_id in hero_list.items():

    hero_file = file_name+'\\'+name
    os.mkdir(hero_file)
    # 根据英雄ID获取英雄皮肤id列表
    skin_id_url = 'https://game.gtimg.cn/images/lol/act/img/js/hero/' + hero_id +'.js?ts=2770132'
    skin_id_info1 = requests.get(skin_id_url).text
    # 解决类似内容  "凯尔乘坐“X40”战机..."问题
    if '\\"'in skin_id_info1:
        skin_id_info1 = skin_id_info1.replace('\\"','____')

    skin_id_info = skin_id_info1.encode('utf-8').decode('unicode_escape')
    skin_id_json = json.loads(skin_id_info, strict=False)['skins']


    # 一个英雄的皮肤
    skin_num = len(skin_id_json)
    print("开始下载英雄： "+name)
    for i in range(skin_num):
        # 皮肤ID
        skin_id = skin_id_json[i]["skinId"]

        # 皮肤url
        img_url=''
        if skin_id_json[i]["chromas"]=='0':
            img_url = 'https://game.gtimg.cn/images/lol/act/img/skin/big'+skin_id+'.jpg'
        elif skin_id_json[i]["chromas"]=='1':
            img_url = 'https://game.gtimg.cn/images/lol/act/img/chromas/'+hero_id+'/'+skin_id+ '.png'

        # 下载图片,e
        print(img_url)
        # 以皮肤名称命名‘哥特萝莉安妮.jpg’
        img_name = skin_id_json[i]['name']
        # 防止类似文件名  "K/DA"
        if '/' in img_name:
            img_name = img_name.replace('/','')
        store_img_name = hero_file + '\\' + img_name + '.jpg'
        img = requests.get(img_url,stream=True)

        # 保存图片到文件
        time.sleep(0.51)
        chunk_size = 100
        size = 0
        with open(store_img_name,'wb') as f:
            f.write(img.content)
            print('正在下载===',skin_id_json[i]['name'])
