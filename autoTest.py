#coding:utf-8
import requests   #接口
import json       #解析返回的json数据
import re         #正则表达式
import xlrd       #读excel
import xlwt       #写excel
import os         #对文件的导入导出操作
import socket
from xlutils.copy import copy    #复制excel的sheet

excel = 'C:/Users/legion_i7_10th/Desktop/autoTest.xls'    #定义存放用例的excel路径
all_data = xlrd.open_workbook(excel,formatting_info=True)
headers = {'Content-type': 'application/json; charset=utf-8',
           'Connection':'keep-alive','access_token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDY0NjI5OTMsInVzZXJuYW1lIjoiMzA2MDAwMDY2NzMzIn0.zAusk-ZA4iLQy5AGtL-ngoTgT8_c_WeTrIj_g5Wqjgg'}   #定义headers
I = []       #用来存放测试结果
J = []      #用来存放flag,返回标志
K = []      #用例存放实际Status Code
L = []      #用来存放实际Response
M = []      #表示查询结果为空
table = all_data.sheet_by_index(0)  #第一个sheet
nrow = table.nrows      #获取行数
m = 0   # 表示查询结果为空
#print(nrow)

for i in range(1,nrow):     #循环获取每行中的数据
    api_host = table.cell(i,2).value    #获取excel中API Host
    request_url = table.cell(i,3).value     #获取excel中Request URL
    request_method = table.cell(i,4).value      #获取excel中的方法，GET/POST/DELETE
    url = api_host + request_url        #拼接url
    request_data = table.cell(i,5).value.encode("utf-8")    #获取excel中要传的参数Request Data
    status_code = table.cell(i,6).value      #获取期望的状态码Status Code
    flag = table.cell(i,7).value     #获取期望的Response
    flagint = int(flag)     #转为int

    if request_method == 'GET':     #不同的方法发不同的请求
        r = requests.get(url,headers = headers)
    elif request_method == 'POST':
        r = requests.post(url,data = request_data,headers = headers)
    elif request_method == 'DELETE':
        r = requests.delete(url,data = request_data,headers = headers)

    #print(r.text)
    #print(r.json())

    if r.status_code == status_code:  #返回status与预计status相同，比如200 = 200
        #if r.json()['resultCode'] == flagint:  # 返回flag与预计flag相同，比如0 = 0
            J.append(r.json()['resultCode'])
            K.append(r.status_code)
            L.append(json.dumps(r.json(),ensure_ascii=False))
            if r.json()['resultCode'] == flagint:  # 返回flag与预计flag相同，比如0 = 0
                I.append('Pass')
            else:
                I.append('status pass  And result fail')
            if len(r.json().get("content")) == m:  # 查询结果
                M.append('查询结果为空')
            else:
                M.append('')

    else:
        #print(json.dumps(r.json(),ensure_ascii=False))
        I.append('Fail')
        J.append('')
        K.append(r.status_code)
        M.append('')
        try:
            L.append(json.dumps(r.json(),ensure_ascii=False))
        except:
            L.append(re.search("<title>.*</title>", r.text).group().strip("</title>"))
    r.close()
    print('共有%d个url，第%d个执行完毕'%(nrow-1,i))

book = copy(all_data)
sheet1 = book.get_sheet(0)
for j in range(1,nrow):     #将各结果写入到对应的表格中
    sheet1.write(j,8,I[j-1])
    sheet1.write(j,9,J[j-1])
    sheet1.write(j,10,K[j-1])
    sheet1.write(j,11,L[j-1])
    sheet1.write(j,12,M[j-1])
book.save(excel)