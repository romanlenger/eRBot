import re
import json
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from app.variables import url_nbu, headers, url_mukachevo, url_mb, url_banks


# Курс НБУ
def get_nbu(url, headers):
    response = requests.get(url, headers=headers).json()
    
    with open('nbu_api.json', 'w', encoding='utf-8') as json_file:
        json.dump(response, json_file, ensure_ascii=False, indent=4, default=str)

    nbu_list = []

    for n in response:
        if n.get('r030') == 840:
            nbu_list.append(str(n.get('rate')).replace('.', ','))
            nbu_list.append(None)
        elif n.get('r030') == 978:
            nbu_list.append(str(n.get('rate')).replace('.', ','))
            nbu_list.append(None)
            
    return nbu_list


# Середній курс в банках
def get_banks(url, headers):
    html = requests.get(url,headers=headers).text
    soup = bs(html, 'html.parser')

    raw = []
    try:
        for tr in soup.find_all('td', {'data-title' : 'Середній курс'}):
            raw.append(tr.text.replace('.', ','))
    except Exception as e:
        print(f'{e} ---------Banks')
        raw.append(None)
        return raw
    
    pattern = r'\d{2}\,\d{2}'

    return [re.findall(pattern, b) for b in raw]


# Курс на Межбанке
def get_mb(url, headers):
    html = requests.get(url, headers=headers).text
    soup = bs(html, 'html.parser')

    mb = []
    for td in soup.find_all('td', {'class' : 'sc-1x32wa2-8 tWvco'}):
        try:
            value = (td.find("div", {"class" : "sc-1x32wa2-9 bKmKjX"}).text)[:5].replace('-', '0')
            mb.append(value)
        except Exception as e:
            mb.append(None)
            print(f'{e} ----------MB')
            continue

    return mb


# MINFIN Мукачево Євро
def get_euro_m(url, headers):
    html = requests.get(url, headers=headers).text
    soup = bs(html, 'html.parser')

    mukachevo_euro = []

    for td in soup.find_all('td', {'class' : 'sc-1x32wa2-8 tWvco'}):
        try:
            value = ''.join((td.find("div", {"class" : "sc-1x32wa2-9 bKmKjX"}).text.split()))[:5].replace('-', '0')
            mukachevo_euro.append(value)
        except Exception as e:
            mukachevo_euro.append(None)
            print(f'{e} ----------Mukachevo')
            continue

    return mukachevo_euro[:2]


def main():
    mukachevo_euro = get_euro_m(url_mukachevo, headers)
    time.sleep(1.1)
    mb = get_mb(url_mb, headers)
    nbu = get_nbu(url_nbu, headers)
    time.sleep(1.1)
    banks = get_banks(url_banks, headers)

    dfdict = {
        'Мукачево EUR' : mukachevo_euro,
        'Межбанк USD' : mb[:2],
        'Межбанк EUR' : mb[2:],
        'НБУ USD' : nbu[:2],
        'НБУ EUR' : nbu[2:],
        'Банки USD' : banks[0],
        'Банки EUR' : banks[1]
    }

    try:
        result_df = pd.DataFrame.from_dict(dfdict, orient='index').transpose().apply(lambda x: x.explode() if x.dtype == 'O' else x)

        with pd.ExcelWriter(f'exchange_rates.xlsx', engine='xlsxwriter', mode='w') as writer:
            result_df.to_excel(writer, sheet_name='курсы', index=False)
    except Exception as e:
        print(e)
        pass

    
if __name__ == '__main__':
    main()








