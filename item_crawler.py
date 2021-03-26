# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
import pandas as pd
import re

def category_info(sub_category):
    page_num = '1' #첫 페이지
    sort = 'pop&sub_sort'

    url = 'https://search.musinsa.com/category/'+ sub_category + \
    '?device=&d_cat_cd=020006&brand=&rate=&page_kind=search&list_kind=small&sort=' + \
    sort+'=&page='+page_num+'&display_cnt=90&sale_goods=&ex_soldout=&color=&price1=&price2=&exclusive_yn=&size=&tags=&sale_campaign_yn=&timesale_yn=&q='

    req = requests.get(url)
    raw = req.text

    html = BeautifulSoup(raw, 'html.parser')

    #해당 카테고리 옷의 전체 페이지 수 긁어오기
    total_item = html.select_one('#goods_list > div.boxed-list-wrapper > div.thumbType_box.box > span.counter.box_num_goods > label').get_text()
    total_page_n= html.select_one('span.totalPagingNum').get_text()

    total_item = re.sub("[^0-9]",'',total_item) #숫자만 남기고 제거
    print(sub_category, "category","item_count: ",total_item,"page_count: ",total_page_n)
    return total_item, total_page_n

def item_crawling(sub_category,total_page_n):
    for i in range(total_page_n):
        page_num = str(i)
        url = 'https://search.musinsa.com/category/'+sub_category+ \
        '?device=&d_cat_cd='+'020006'+'&brand=&rate=&page_kind=search&list_kind=small&sort=pop&sub_sort=& \
        page='+page_num+'&display_cnt=90&sale_goods=&ex_soldout=&color=&price1=&price2=&exclusive_yn=&size=&tags=&sale_campaign_yn=&timesale_yn=&q='

        req = requests.get(url)
        raw = req.text

        html = BeautifulSoup(raw, 'html.parser')
        items = html.select('ul#searchList > li ')

        for item in items:
            item_id_c.append(item['data-no']) #item별 아이디를 가져옴
            img_url_c.append(item.img['data-original']) #item별 img url을 가져옴.
            #좋아요 수 숫자만 가져옴. 없으면 ''
            like_c.append(item.select_one("p.txt_cnt_like").get_text())
            page_num_c.append(i) #몇 페이지에서 가져온건지 기록
    print(len(item_id_c), len(img_url_c),len(page_num_c),len(like_c))

def to_df():
    df = pd.DataFrame()
    df['item_id'] = item_id_c
    df['img_url'] = img_url_c
    df['sub_category'] = '020006'
    df['category'] = '020'
    df['page_num']=page_num_c
    #df['like'] = like_c
    df['date'] = date.today().isoformat() #'yyyy-mm-dd'

    df.category = df.category.astype('str') #앞자리가 0이면 사라져서 다시 str으로 변환
    df.sub_category = df.sub_category.astype('str')

    sub_category ='020006'
    d= date.today().strftime('%Y%m%d')
    f_name = 'mini_onepiece({})_{}_1.csv'.format(sub_category, d)

    df.to_csv(f_name)

if __name__ == "__main__":
    sub_category = '020006' #하위카테고리 미니 원피스
    #각 정보 담을 list 생성
    item_id_c = []
    img_url_c = []
    page_num_c = []
    like_c = []
    
    category_info(sub_category)
    item_crawling(sub_category,total_page_n)
    to_df()