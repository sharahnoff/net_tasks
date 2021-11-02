import subprocess
import re
import json
import requests
from beautifultable import BeautifulTable


def make_table(data):
    table = BeautifulTable()
    table.columns.header = ['№', 'IP', 'AS/PROVIDER', 'COUNTRY']
    for i, x in enumerate(data):
        try:
            table.rows.append([i, x['ip'], x['org'], x['country']])
        except KeyError:
            table.rows.append([i, x['ip'], '*', '*'])
    return table

def get_data(route):
    route = route.stdout.readline
    data = []
    reg = re.compile("([0-9]{1,3}[\.]){3}[0-9]{1,3}")
    for line in iter(route, ''):
        if not line:
            break
        line = line.decode('utf-8', errors='ignore').strip()
        ip = reg.search(line)
        if not ip or not line[0].isdigit():
            continue
        req = requests.get(f"http://ipinfo.io/{ip.group(0)}/json")
        data.append(json.loads(req.text))
    return data

def main():
    addr = input('Введите доменное имя или ip-адрес: ')
    if len(addr) < 3 :
        print("Завершаем работу")
        return
    route = subprocess.Popen(["tracert", addr], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(make_table(get_data(route)))
    input("Нажмите ENTER для выхода")
    

if __name__ == '__main__':
    main()
