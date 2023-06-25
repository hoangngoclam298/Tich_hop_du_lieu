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
    text = text.replace("\n", " ").replace("\r", "")
    return text

def get_num(text):
    if(text == None):
        return ''
    numbers = re.findall(r'\d+', text)
    res = ''
    for x in numbers:
        res += str(x)
    return res
def load_item_alomuabannhadat(item):
    prices = item['price']
    prices = prices.split(' ')
    price = 0
    for i in range(len(prices)):
        if(prices[i].isdigit()):
            if(convert(prices[i+1]) == 'ty' or convert(prices[i+1]) == 'ti'):
                price += float(prices[i])*1000
            if (convert(prices[i + 1]) == 'trieu'):
                price += float(prices[i])
            if (convert(prices[i + 1]) == 'nghin'):
                price += float(prices[i])/1000
    item['price'] = price
    area = ''
    for x in item['area']:
        if(x.isdigit()):
            area += x
    if(area != ''):
        item['area'] = area
    features = item['features']
    item['length'], item['width'], item['juridical'], item['floor'], item['direct'] = '','','','',''
    for x in features:
        tmp = x.split(':')
        if(convert(tmp[0]) == 'chieu dai'):
            item['length'] = convert(tmp[1])
        if(convert(tmp[0]) == 'chieu ngang'):
            item['width'] = convert(tmp[1])
        if(convert(tmp[0]) == 'loai dia oc'):
            item['juridical'] = convert(tmp[1])
        if(convert(tmp[0]) == 'so lau'):
            item['floor'] = convert(tmp[1])
        if(convert(tmp[0]) == 'huong xay dung'):
            item['direct'] = convert(tmp[1])
    item['phone_contact'] = get_num(item['phone_contact'])
    text_desc = ''
    for x in item['description']:
        text_desc += normalized(x)
    item['description'] = text_desc
    return item

def load_alomuabatnhadat():
    with open(r'../crawl_THDL/alomuabannhadat.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open('alomuabannhadat.csv', 'w', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ['title', 'price', 'address', 'area', 'width', 'length', 'description', 'link_image',
                  'url_page', 'direct', 'floor', 'juridical', 'name_contact', 'phone_contact']
        writer.writerow(header)

        for x in data:
            item = load_item_alomuabannhadat(x)
            tmp = []
            for y in header:
                tmp.append(item[y])
            writer.writerow(tmp)