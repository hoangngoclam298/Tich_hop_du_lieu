import json
import csv
import regex as re
from unidecode import unidecode

def convert(text):
    if(text == None):
        return ''
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

def get_phone(text):
    if (text == None):
        return ''
    numbers = re.findall(r'\d+', text)
    res = ''
    for x in numbers:
        res += str(x)
    res = res[:4] + '.' + res[4:7] + '.' + res[7:]
    return res

def load_item_mogi(item):
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
    item['juridical'] = item['juridical'] if (not convert(item['juridical']) == 'khong xac dinh') else ''
    item['name_contact'] = normalized(item['name_contact'])
    item['name_contact'] = re.sub('\s+', ' ', item['name_contact']).strip()
    item['phone_contact'] = get_phone(item['phone_contact'])
    return item

def load_mogi():
    with open(r'../crawl_THDL/mogi.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open('mogi.csv', 'w', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ['title', 'price', 'address', 'area', 'date', 'description', 'link_image',
                  'url_page', 'juridical', 'name_contact', 'phone_contact']
        writer.writerow(header)

        for x in data:
            item = load_item_mogi(x)
            tmp = []
            for y in header:
                tmp.append(item[y])
            writer.writerow(tmp)