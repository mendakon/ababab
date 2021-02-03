import json
import requests
import time
import paho.mqtt.client as mqtt
import random
import string


ipadder = "18.177.26.92"
placeId = 1
broker = "192.168.2.121"

def dataGet():
  response = requests.get("http://"+ipadder+"/place/"+str(placeId)+"/word_data")
  return response.text

def same(l1s, l2s):
  list1str = ""
  list2str = ""
  for l1 in l1s:
    list1str += l1["uniq_id"]
    for word in l1["words"]:
      list1str += word["word"]
  
  for l2 in l2s:
    list2str += l2["uniq_id"]
    for word in l2["words"]:
      list2str += word["word"]

  return list1str == list2str

if __name__ == '__main__':
  client = mqtt.Client()
  #client.connect(broker, port=1883, keepalive=60)
  #client.loop_start() 

  data_list_tmp = []
  pub_datas = []

  while True:
    res = dataGet()
    data_list = json.loads(res)
    if same(data_list, data_list_tmp):
      for pub in pub_datas:
        #client.publish("drone/001",pub) 
        print(pub_datas)
      time.sleep(1)
      continue
    data_list_tmp = list(data_list)
    pub_datas = []

    fixed_name_list = []
    for data in data_list:
      f = ""
      while f=="" or f in fixed_name_list:
        f = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
      data["fixed_name"] = f
      fixed_name_list.append(f)
    
    #送信文字列生成
    for data1 in data_list:
      pub_data = data1["fixed_name"]
      pub_id = data1["uniq_id"]
      
      for data2 in data_list:
        #自分をスキップ
        if data1["uniq_id"]==data2["uniq_id"]:
          continue
        
        #会うものを発見
        word_match_pack = 0
        for w1 in data1["words"]:
          for w2 in data2["words"]:
            if w1["word"] == w2["word"] and w1["word"]!="":
              print("ぱあああ:" + str(w1["order"]) + w1["word"])
              word_match_pack = word_match_pack | (1<<w1["order"])
        pub_data = pub_data + data2["fixed_name"] + str(word_match_pack)
              
      #client.publish("drone/001",pub_data) 
      print(pub_data)
      pub_datas.append(pub_data)

    time.sleep(1)