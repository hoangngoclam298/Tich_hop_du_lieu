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
    areao = text.split(" ")[0]
    areao = areao.split("M")[0]
    area = areao.replace(",", ".").replace(" ", "")
    try:
        return str(float(area))
    except:
        return ''

def split_text_price(text):
    list_text = text.split(' ')
    result = []
    for text in list_text:
        start = 0
        for i in range(1, len(text)):
            if((text[i-1].isdigit() and text[i].isalpha()) or (text[i].isdigit() and text[i-1].isalpha())):
                result.append(text[start:i])
                start = i
        result.append(text[start:])
    return result

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
    if(text == None):
        return ''
    numbers = re.findall(r'\d+', text)
    res = ''
    for x in numbers:
        res += str(x)
    res = res[:4] + '.' + res[4:7] + '.' +res[7:]
    return res

def load_item_nhadat24h(item):
    item['title'] = normalized(item['title'])
    try:
        prices = split_text_price(item['price'])
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
    item['width'] = get_area(item['width']) + 'm' if(get_area(item['width']) != '') else ''
    text_desc = ''
    for x in item['description']:
        text_desc += normalized(x)
    item['description'] = text_desc
    item['name_contact'] = normalized(item['name_contact'])
    item['name_contact'] = re.sub('\s+', ' ', item['name_contact']).strip()
    item['phone_contact'] = get_phone(item['phone_contact'])
    return item

def load_nhadat24h():
    with open(r'../crawl_THDL/nhadat24h.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open('nhadat24h.csv', 'w', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ['title', 'price', 'address', 'area', 'width', 'description', 'link_image',
                  'url_page', 'name_contact', 'phone_contact']
        writer.writerow(header)

        for x in data:
            item = load_item_nhadat24h(x)
            tmp = []
            for y in header:
                tmp.append(item[y])
            writer.writerow(tmp)