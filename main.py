from bs4 import BeautifulSoup
from requests import Session
from json import load, dump, decoder
from os import listdir, chdir, path


group_id = 5
session_cookie = '<здесь кук "session" из залогиненой сессии на shadowservants.ru (для доступа к стоимости тасков)>'
categories = 'Crypto', 'Web', 'Networking', 'PPC', 'Forensic', 'PWN', 'Reverse', 'Stegano'
domain = 'http://shadowservants.ru'
session = Session()
task_cache = {}



def print_rate(num):
    print(str(num), end=' ' * (10 - len(str(num))) + '| ')


def print_name(name):
    max_len = 10 + 1
    if len(name) > max_len:
        print(name[:max_len-3]+'...| ', end='')
    else:
        print(name, end=' ' * (max_len - len(name)) + '| ')


def task_rate(url):
    if url in task_cache:
        return task_cache[url]
    task_html = session.get(domain + url, data={}).text
    soup = BeautifulSoup(task_html, 'lxml')
    if soup.title.string == '404 Not Found':
        task_cache[url] = None
        return
    text = soup.find_all('h5', class_='text-center')[0].text
    rate = int(text.split('/')[-1])
    task_cache[url] = rate
    return rate


def show_player(url, name):
    player_html = session.get(domain + url).text
    soup = BeautifulSoup(player_html, 'lxml')
    score = str(soup.find('h4')).split()[2]

    categories_dict = {}
    for category in categories:
        categories_dict[category] = 0
    # categories_dict = {'Crypto': 0, 'Web': 0 ...}

    for i, tr in enumerate(soup.find_all('tr')):
        if i == 0:
            continue
        # 1 - href, 3 - category, 5 - timestamp
        task_href = list(tr)[1].find('a').get('href')
        category = list(tr)[3].text
        if category in categories:
            rate = task_rate(task_href)
            if rate is None:
                continue
            categories_dict[category] += rate

    print_name(name)
    print_rate(score)
    for category in categories:
        print_rate(categories_dict[category])
    print('\n', ('-'*(10 + 1) + '|')*10, sep='')

def init_shower():
    print('\n Wait...\n')
    print(' Name      | Score     ', *['| ' + category + ' '*(10 - len(category)) for category in categories], '|', sep='')
    print(('-'*(10 + 1) + '|')*10, sep='')
    
    session.cookies['session'] = session_cookie
    html = session.get('{}/score?group_id={}'.format(domain, group_id)).text
    soup = BeautifulSoup(html, features="html5lib")
    table = soup.find('table').tbody
    return table

def task_loader():
    # load tasks from file
    chdir(path.dirname(__file__))
    if 'task_cache.json' in listdir():
        cache_file = open('task_cache.json', 'r')
        try:
            task_cache = load(cache_file)
        except decoder.JSONDecodeError:
            task_cache = {}
    else:
        task_cache = {}

def show_scores():
    task_loader()
    for tr in init_shower():
        a = tr.find('a')
        if type(a) == int: continue
        name = a.text
        show_player(a.get('href'), name)

def show_user_score():
    nicks = input('\n Who do you need?:\n ').split()
    task_loader()
    for tr in init_shower():
        a = tr.find('a')
        if type(a) == int: continue
        name = a.text
        for nick in nicks:
            if ' ' + nick + ' ' == name:
                show_player(a.get('href'), name)

if __name__ == '__main__':
    i = input(' Do you want to see the entire table or just a specific player? [Y/n]: ')
    if i == "y" or i == "Y" or i == 'yes' or i == "YES" or i == "Yes" or  i =='YEs' or i == 'yeS' or i == 'yEs' or i == 'yES' or i == 'Д' or i == 'д' or i== 'Да' or i == 'ДА' or i == 'дА':
        show_scores()
    else:
        show_user_score()
    # save tasks to file
    cache_file = open('task_cache.json', 'w')
    dump(task_cache, cache_file)
    cache_file.close()    