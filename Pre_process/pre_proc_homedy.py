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
    if(text == None):
        return ''
    areao = text.split("\n")[0]
    area = areao.replace(",", ".").replace(" ", "")
    try:
        area = area.split("-")
        if(len(area)==1):
            area = float(area[0])
        elif(len(area)==2):
            area = (float(area[0]) + float(area[1]))/2
        return str(area)
    except:
        return areao

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

def get_phone(res):
    if(res == None):
        return ''
    res = res[:4] + '.' + res[4:7] + '.' +res[7:]
    return res


def load_item_homedy(item):
    item['title'] = normalized(item['title'])
    try:
        prices = item['price'].split('\n')
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
    tmp = ''
    for i in range(len(item['address'])):
        tmp += item['address'][i]
        if(i != len(item['address'])-1):
            tmp += ', '
    item['address'] = tmp
    item['phone_contact'] = get_phone(item['phone_contact'])
    return item

def load_homedy():
    with open(r'../crawl_THDL/homedy.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open('homedy.csv', 'w', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ['title', 'price', 'address', 'area', 'description', 'link_image',
                  'url_page', 'name_contact', 'phone_contact']
        writer.writerow(header)

        for x in data:
            item = load_item_homedy(x)
            tmp = []
            for y in header:
                tmp.append(item[y])
            writer.writerow(tmp)