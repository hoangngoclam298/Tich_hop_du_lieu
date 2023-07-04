import json
import csv
import regex as re
from unidecode import unidecode

def convert(text):
    text = re.sub('\s+', ' ', text).strip()
    text = unidecode(text)
    text = text.lower()
    return text

def normalized(text):
    if(text == None):
        return ''
    text = text.replace("\n", " ").replace("\r", "")
    return text

def get_area(text):
    if(text == None or text == '---'):
        return ''
    areao = text.split("m")[0]
    area = areao.replace(",", ".").replace(" ", "")
    try:
        area = area.split("-")
        if(len(area)==1):
            area = float(area[0])
        elif(len(area)==2):
            area = (float(area[0]) + float(area[1]))/2
        if(area == 0):
            return ''
        return str(area)
    except:
        return ''

def check_price(priceo):
    price = priceo.replace(",", ".").replace(" ", "")
    try:
        price = price.split("-")
        if(len(price)==1):
            price = float(price[0])
        elif(len(price)==2):
            price = (float(price[0]) + float(price[1]))/2
        return True, price
    except:
        return False, priceo

def load_item_homedy(item):
    item['title'] = normalized(item['title'])
    try:
        prices = item['price'].split(' ')
        price = 0
        for i in range(len(prices)):
            check_digit, tmp_price = check_price(prices[i])
            if(check_digit):
                if(convert(prices[i+1]) == 'ty' or convert(prices[i+1]) == 'ti'):
                    price += tmp_price*1000
                if (convert(prices[i + 1]) == 'trieu'):
                    price += tmp_price
                if (convert(prices[i + 1]) == 'nghin'):
                    price += tmp_price
        item['price'] = price
    except:
        pass
    item['area'] = get_area(item['area']) + 'm2' if(get_area(item['area']) != '') else ''
    text_desc = ''
    for x in item['description']:
        text_desc += normalized(x)
    item['description'] = text_desc
    item['width'] = get_area(item['width']) + 'm' if(get_area(item['width']) != '') else ''
    item['length'] = get_area(item['length']) + 'm' if(get_area(item['length']) != '') else ''
    item['floor'] = item['floor'] if(item['floor'].isdigit()) else ''
    item['direct'] = item['direct'] if (not item['direct'] == '_') else ''
    item['juridical'] = item['juridical'] if (not item['juridical'] == '---') else ''
    if(item['date'] == 'Hôm nay'):
        item['date'] = '14/06/2023'
    elif(item['date'] == 'Hôm qua'):
        item['date'] = '13/06/2023'
    item['address'] = item['address'][0]
    return item

def load_ibatdongsan():
    with open(r'../crawl_THDL/ibatdongsan.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open('ibatdongsan.csv', 'w', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ['title', 'price', 'address', 'area', 'date', 'width', 'length', 'description', 'link_image',
                  'url_page', 'direct', 'floor', 'juridical', 'name_contact', 'phone_contact']
        writer.writerow(header)

        for x in data:
            item = load_item_homedy(x)
            tmp = []
            for y in header:
                tmp.append(item[y])
            writer.writerow(tmp)