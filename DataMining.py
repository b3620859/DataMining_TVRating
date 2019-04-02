import numpy as np
import datetime
import re
import os
import urllib.error
import pandas as pd
import requests

def create_date(datestart = None,dateend = None):
    global date_list

    if datestart is None:
        datestart = '20190402'
    if dateend is None:
        dateend = datetime.datetime.now().strftime('%Y%m%d')


    datestart=datetime.datetime.strptime(datestart,'%Y%m%d')
    dateend=datetime.datetime.strptime(dateend,'%Y%m%d')
    date_list = []
    date_list.append(datestart.strftime('%Y%m%d'))
    while datestart<dateend:

        datestart+=datetime.timedelta(days=+1)

        date_list.append(datestart.strftime('%Y%m%d'))
#     return date_list
    print(date_list)

    
def get_data(date_list = None):
           
    for date in date_list:
        
        date = int(date) - 20000000
    #         print(date, type(date))
        src = 'http://www1.xkm.com.tw/hr/DATA/HR'+str(date)+'.htm'
    #         print(src)
        src = requests.get('http://www1.xkm.com.tw/hr/DATA/HR' +str(date)+'.htm')
        src_text = src.text
    #   print(src_text)
        try: 
            dfs = pd.read_html('http://www1.xkm.com.tw/hr/DATA/HR' +str(date)+'.htm')
        except urllib.error.HTTPError:
            continue
    
        
        
        rating = dfs[0]
        rating.drop(columns=[0,7],axis=1,inplace = True)
        rating.columns = rating.loc[3]
        rating.drop([0,1,2,3],inplace = True)
        rating.dropna(how='any',inplace = True)     
        rating.reset_index(drop = True, inplace=True)
        rating.to_csv(str(date)+".csv" ,index=False,encoding = 'utf-8-sig')
            
        

        


if __name__ == '__main__':
    datestart = '20160331'
    dateend = '20190331'
    create_date(datestart,dateend)
    get_data(date_list)