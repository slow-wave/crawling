#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
import pandas as pd
import re
import os
#from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager

def item_info(p_count,sub_category):
    for i in range(int(p_count)):
        sort = 'pop&sub_sort'

        url = 'https://search.musinsa.com/category/'+ sub_category + \
        '?device=&d_cat_cd=020006&brand=&rate=&page_kind=search&list_kind=small&sort=' + \
        sort+'=&page='+str(i)+'&display_cnt=90&sale_goods=&ex_soldout=&color=&price1=&price2=&exclusive_yn=&size=&tags=&sale_campaign_yn=&timesale_yn=&q='

        req = requests.get(url)
        raw = req.text

        html = BeautifulSoup(raw, 'html.parser')
        items = html.select('ul#searchList > li ')

        for item in items:
            item_id_c.append(item['data-no']) #item별 아이디를 가져옴
            img_url_c.append(item.img['data-original']) #item별 img url을 가져옴.
            page_num_c.append(i) #몇 페이지에서 가져온건지 기록
        
        #동적 데이터라 selenium으로 가져옴.
        #driver.get(url)

        #like = driver.find_elements_by_class_name('txt_cnt_like')
        
        #for i in like:
        #    like_c.append(re.sub('\,','',i.text))
def to_csv(sub_category):
    df = pd.DataFrame()
    df['item_id'] = item_id_c
    df['img_url'] = img_url_c
    df['page_num']=page_num_c
    df['like'] = like_c
    df['date'] = date.today().isoformat() #'yyyy-mm-dd'
    df['sub_category_code'] = sub_category

    d= date.today().strftime('%Y%m%d')

    f_name = '{}_{}.csv'.format(sub_category, d)

    df.head()
    df.to_csv(f_name,index = False)

def crawling(df):
    for i in range(len(df)):
        #c_code = df['category_code'][i]
        p_count = df['page_count'][i]
        sub_category = str(df['sub_category_code'][i])

        item_info(p_count,sub_category)
        to_csv(sub_category)
        print(len(item_id_c), len(img_url_c),len(page_num_c),len(like_c))
    return item_id_c, img_url_c, page_num_c,like_c

if __name__ == "__main__":
    path = os.getcwd()

    #options = webdriver.ChromeOptions() # 크롬 브라우저 옵션
    #options.add_argument('headless') # 브라우저 안 띄우기
    #driver = webdriver.Chrome(ChromeDriverManager().install(),options = options)

    category_df = pd.read_csv(path+'/'+"category_count_20210330.csv",index_col = 0,converters={'sub_category_code':str})
    category_df =category_df.iloc[1:2,]
    category_df = category_df.reset_index() 
    item_id_c = []
    img_url_c = []
    page_num_c = []
    like_c = []
    #count_c = []
    carwling = crawling(category_df)

    #몇 개 들어왔나 확인.
    print(len(item_id_c), len(img_url_c),len(page_num_c),len(like_c))
