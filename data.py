import requests
import json


API_KEY = 'secret_key'
city_list = []
info_list = []

def find_cities():
    cities = requests.get('https://old.bkfon.ru/shopAPI/api/v1.2/city/?format=json')
    cities_json = json.loads(cities.text)
    for city in cities_json:
        city_list.append(city['city'])
    return city_list

def find_info():
    find_cities()
    for city in city_list:
        try:
            r = requests.get(f'https://www.fonbet.ru/shopAPI/api/v1.2/shop/?city={city}&olen=999&format=json')
            json_info = json.loads(r.text)
            DIC = {'city': '', 'addr': '', 'latlon': [], 'schedule': '', 'phone':'[+8 (800) 100-7234]'}
            info = json_info['results']
            DIC['city'] = info[0]['city']
            DIC['addr'] = info[0]['address']
            DIC['latlon'] = [info[0]['latitude'], info[0]['longitude']]
            DIC['schedule'] = info[0]['schedule']
            info_list.append(DIC)
        except Exception:
            DIC['city'] = city
            DIC['addr'] = 'В городе нет офисов'
            DIC['latlon'] = 'В городе нет офисов'
            DIC['schedule'] = 'В городе нет офисов'
            DIC['phone'] = 'В городе нет офисов'
            info_list.append(DIC)
    return info_list

def write(information = find_info()):
    with open('fanbet.json','w') as file:
        json.dump(information,file,indent=2, ensure_ascii=False)

#!--------------------------------------------------------------------------------------------------------------------------
'''def find_phone():
    find_cities()
    club_phones = []
    for city in city_list:
        try:
            r = requests.get(f'https://www.fonbet.ru/shopAPI/api/v1.2/shop/?city={city}&olen=999&format=json')
            a = json.loads(r.text)
            dict_phones = {'city': '', 'addr': '',}
            inf = a['results']
            DIC2 = {}
            dict_phones['city'] = inf[0]['city']
            dict_phones['addr'] = inf[0]['address']
            phone_city = dict_phones['city']
            phone_addr = dict_phones['addr']
            html = requests.get(f'https://search-maps.yandex.ru/v1/?text=ФОНБЕТ, {phone_city}, {phone_addr}&type=biz&lang=ru_RU&results=1&apikey={API_KEY}')
            json_info = json.loads(html.text)
            phone = json_info['features'][0]['properties']['CompanyMetaData']['Phones'][0]['formatted']
            DIC2['phone'] = phone
            club_phones.append(DIC2)
        except Exception:
            pass
    print(club_phones)'''


