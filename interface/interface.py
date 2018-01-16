#!/usr/bin/env python
#coding:utf-8
import json
import requests
import operator
import os
from xml.dom import minidom

def sendData(par):
        payload = {}
        payload[0] = par[6]
        params = par[5]
        mystr=par[4]
        #发送请求
        with open('rightside.txt','a+') as rs: 
                try:
                        data = requests.get(mystr,params=payload)
                except Exception as e:
                        if operator.eq("404",par[6]):
                                rs.write('通过\n')
                        else:
                                rs.write('失败\n')
                else:
                        print(data.text)
                        r=str(data.status_code)
                        print (r)
                        try:
                                if ((operator.eq(r,par[6])) and (par[7]) in data.text):
                                        rs.write('通过\n')
                                else:
                                        rs.write('失败\n')
                        except Exception as e:
                                rs.write('没有执行结果\n')
        rs.close()
                
def report(par,line):
        mystr="<tr>"
        mystr=mystr+"<td>"+par[0]+"</td>\n"
        mystr=mystr+"<td>"+par[1]+"</td>\n"
        mystr=mystr+"<td>"+par[2]+"</td>\n"
        mystr=mystr+"<td>"+par[3]+"</td>\n"
        mystr=mystr+"<td>"+par[4]+"</td>\n"
        mystr=mystr+"<td>"+par[5]+"</td>\n"
        mystr=mystr+"<td>"+par[6]+"</td>\n"
        mystr=mystr+"<td>"+par[7]+"</td>\n"
        mystr=mystr+"<td>"+line+"</td>\n"
        mystr=mystr+"</tr>\n"
        return mystr

def getpar():
        par = []
        par.append(TestIds[i].firstChild.data)
        par.append(Titles[i].firstChild.data)
        par.append(Methods[i].firstChild.data)
        par.append(Descs[i].firstChild.data)
        par.append(Urls[i].firstChild.data)
        par.append(InptArgs[i].firstChild.data)
        par.append(Results[i].firstChild.data)
        par.append(CheckWords[i].firstChild.data)
        return par
        

if __name__=="__main__":
        dom =  minidom.parse('config.xml')
        root = dom.documentElement
        TestIds = root.getElementsByTagName('TestId')
        Titles = root.getElementsByTagName('Title')
        Methods = root.getElementsByTagName('Method')
        Descs = root.getElementsByTagName('Desc')
        Urls = root.getElementsByTagName('Url')
        InptArgs = root.getElementsByTagName('InptArg')
        Results = root.getElementsByTagName('Result')
        CheckWords =root.getElementsByTagName('CheckWord')
        i=0
        with  open('rightside.txt','w') as rs:
                for TestId in TestIds:
                        par = getpar()
                        sendData(par)
                        i=i+1
        rs.close()        
        frs = open("rightside.txt","r")
        lines=""
        i=0
        for TestId in TestIds:
                line=frs.readline()
                par = getpar()
                lines=lines+report(par,line)
                i=i+1
        frs.close()
        fhtml = open("index.htm","r")
        myline=fhtml.read()
        myline=myline.replace('###1',lines)
        fhtml.close()
        with  open('report.html','w') as fhtml1:
                fhtml1.write(myline)
        fhtml1.close()

