from bs4 import BeautifulSoup, element
from requests import Session
from json import load, dump, decoder
from os import listdir, chdir, path
from argparse import ArgumentParser


session_cookie = '<здесь кук "session" из залогиненой сессии на shadowservants.ru (для доступа к стоимости тасков)>'

categories = 'Crypto', 'Web', 'Networking', 'PPC', 'Forensic', 'PWN', 'Reverse', 'Stegano'
domain = 'http://shadowservants.ru'
session = Session()
session.cookies['session'] = session_cookie
task_cache = {}


def load_tasks():
    # load tasks from file
    chdir(path.dirname(path.abspath(__file__)))
    global task_cache
    if 'task_cache.json' in listdir():
        cache_file = open('task_cache.json', 'r')
        try:
            task_cache = load(cache_file)
        except decoder.JSONDecodeError:
            task_cache = {}
    else:
        task_cache = {}


def save_tasks():
    cache_file = open('task_cache.json', 'w')
    dump(task_cache, cache_file)
    cache_file.close()


def init_table():
    print('Wait...')
    print(' Name      | Score     ', *['| ' + category + ' ' * (10 - len(category)) for category in categories], '|',
          sep='')
    print(('-' * (10 + 1) + '|') * 10, sep='')


def print_rate(num):
    print(str(num), end=' ' * (10 - len(str(num))) + '| ')


def print_name(name):
    max_len = 10 + 1
    if len(name) > max_len:
        print(name[:max_len - 3] + '...| ', end='')
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
        category = list(tr)[3].text.replace('Stego', 'Stegano')
        if category in categories:
            rate = task_rate(task_href)
            if rate is None:
                continue
            categories_dict[category] += rate

    print_name(name)
    print_rate(score)
    for category in categories:
        print_rate(categories_dict[category])
    print('\n', ('-' * (10 + 1) + '|') * 10, sep='')


def get_group_players(group_id):
    try:
        html = session.get('{}/score?group_id={}'.format(domain, group_id)).text
    except UnicodeEncodeError:
        print('I think you forgot to substitute cookies...')
        exit()
    soup = BeautifulSoup(html, features="html5lib")
    table = soup.find('table').tbody
    return table


def show_scores(group_id):
    for tr in get_group_players(group_id):
        a = tr.find('a')
        if type(a) == int: continue
        name = a.text.strip()
        show_player(a.get('href'), name)


def find_nick_urls(nicks):
    html = session.get('{}/score'.format(domain)).text
    soup = BeautifulSoup(html, features="html5lib")
    table = soup.find('table').tbody
    urls = {}
    for line in table:
        if type(line) == element.Tag:
            current_nick = str(line.contents[1].string).strip()
            if current_nick in nicks:
                urls[current_nick] = line.contents[1].next.attrs['href']
    return urls


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-g', '--group-id', dest='id', metavar='ID', type=int, default=5,
                        help='Вывести всех участников группы (по умолчанию: 5)')
    parser.add_argument('-n', '--nicks', dest='nicks', metavar='NICK', nargs='+', help='Вывести score игроков')
    args = parser.parse_args()

    load_tasks()
    init_table()
    if args.nicks is not None:
        nick_urls = find_nick_urls(args.nicks)
        for nick, nick_url in nick_urls.items():
            show_player(nick_url, nick)
    else:
        show_scores(args.id)
    save_tasks()
