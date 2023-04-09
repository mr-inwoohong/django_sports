import json
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
#from ebaysdk.finding import Connection as Finding


def home(request):
    return render(request, 'stats/home.html')



@csrf_exempt
def get_data(request, searchterm):
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={searchterm}&_sacat=0&LH_PrefLoc=1&LH_Auction=1&rt=nc&LH_Sold=1&LH_Complete=1'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    productslist = []
    results = soup.find_all('div', {'class': 's-item__info clearfix'})

    solddate = soup.find('div', class_='s-item__title--tagblock')

    for item in results:
        product = {
            'title': item.find('div', {'class': 's-item__title'}).text,
            'soldprice': float(item.find('span', {'class': 's-item__price'}).text.replace('$','').replace(',','').strip()),
            'solddate': solddate.find('span', {'class': 'POSITIVE'}).text,
            'link': item.find('a', {'class': 's-item__link'})['href'],
        }
        productslist.append(product)

    context = {
        'searchterm': searchterm,
        'productslist': productslist,
    }

    return render(request, 'stats/ebay_sold.html', context)



@csrf_exempt
def get_headlines(request, searchterm):

    # searchterm = searchterm.title().replace(' ', '')

    url = f'https://news.google.com/rss/search?q={searchterm}'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    results = soup.find_all('item')
    links = soup.find('link')
    
    productslist = []

    for item in results:
        product = {
            'title': item.find('title').text,
            'link': item.find('link').text,
        }
        productslist.append(product)


    context = {
        'searchterm': searchterm,
        'productslist': productslist,

    }
    return render(request, 'stats/headlines.html', context)




APPLICATION_ID = 'ianhong-weezy-PRD-bbfa4472b-704c86fb'


@csrf_exempt
def get_current(request, searchterm):
    # searchterm = searchterm.title().replace(' ', '')
    url = f'https://www.ebay.com/sch/i.html?_nkw={searchterm}&_sacat=0'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    productslist = []
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    for item in results:
     
        product = {
            'price': item.find('span', {'class': 's-item__price'}).text.replace('$','').replace(',',''),
            'title': item.find('div', {'class': 's-item__title'}).text,
            'link': item.find('a', {'class': 's-item__link'})['href'],
        }
        productslist.append(product)

    context = {
        'searchterm': searchterm,
        'productslist': productslist,
    }

    return render(request, 'stats/ebay_current.html', context)


@csrf_exempt
def nba_stats(request, player_name, season):
    url = f"https://www.balldontlie.io/api/v1/players?search={player_name}"
    response = requests.get(url)
    player_id = response.json()['data'][0]['id']

    url = f"https://www.balldontlie.io/api/v1/season_averages?player_ids[]={player_id}&season={season}"
    response = requests.get(url)
    data = response.json()['data'][0]
    productslist = []
    stats = {
        "Player": player_name,
        "Season": data['season'],
        "PPG": data['pts'],
        "FG": data['fg_pct'],
        "FG3": data['fg3_pct'],
        "FT": data['ft_pct'],
        "REB": data['reb'],
        "APG": data['ast'],
        "STL": data['stl'],
        "BLK": data['blk'],
        "TO": data['turnover'],
        "FGM": data['fgm'],
        "FGA": data['fga'],
        "FG3M": data['fg3m'],
        "FG3A": data['fg3a'],
        "FTM": data['ftm'],
        "FTA": data['fta'],
        "OREB": data['oreb'],
        "DREB": data['dreb'],
    }
    
    # context = {
    #     'productslist': productslist,
    #     'player_name': player_name,
    #     'season': season,
    # }
    return JsonResponse(stats, safe=False)



@csrf_exempt
def player_batting_stats(request, player_name):

    #if request.method == 'POST':
    # player_name = request.get({{ player_name }})
    player_first_name, player_last_name = player_name.split(" ")
    player_first_name = player_first_name.lower()
    player_last_name = player_last_name.lower().replace(" ", "_")   
        

    url = f"https://www.baseball-reference.com/players/{player_last_name[0]}/{player_last_name[0:5]}{player_first_name[0:2]}01.shtml"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'id': 'batting_standard'})

    data_rows = table.find('tbody').find_all('tr')

    data_dict = {}
    for row in data_rows:
        cols = row.find_all(['th', 'td'])
        cols = [col.text.strip() for col in cols]
        key = cols[0]  
        data_dict[key] = [{'Age': cols[0], 'Team': cols[1], 'League': cols[2], 'Games_Played': cols[3], 'Plate_Appearances': cols[4], 'AB': cols[5], ' Runs': cols[6], 'Hits': cols[7], 'Doubles': cols[8], 'Triples': cols[9], 'Homeruns': cols[10], 'RBI': cols[11], 'Stolen_Bases': cols[12], 'Caught_Stealing': cols[13], 'BB': cols[14], 'Strikeouts': cols[15], 'BA': cols[16], 'OBP': cols[17], 'SLG': cols[18], 'OPS': cols[19]}]

    #stats = json.dumps(data_dict)

    context = {
        'data_dict': data_dict,
        'player_name': player_name,
    }
    return render(request, 'stats/player_batting_stats.html', context)

    #return render(request, 'stats/player_batting_stats.html')





@csrf_exempt
def nfl_stats(request, player_name, season):
    player_name = player_name.title()
    football_url = f'https://www.pro-football-reference.com/years/{season}/fantasy.htm'
   
    r = requests.get(football_url)

    soup = BeautifulSoup(r.content, "html.parser")
    headers = [th.getText() for th in soup.findAll('tr')[1].findAll('th')]
    headers = headers[1:]

    rows = [row for row in soup.findAll('tr', class_=lambda table_rows: table_rows != "thead")
        if row.find("a", string=lambda text: text and player_name in text)]

    stats = {
        "Player": rows[0].findAll('td')[0].getText(),
        "Team": rows[0].findAll('td')[1].getText(),
        "Position": rows[0].findAll('td')[2].getText(),
        "Age": rows[0].findAll('td')[3].getText(),
        "Games_Played": rows[0].findAll('td')[4].getText(),
        "Games_Started": rows[0].findAll('td')[5].getText(),
        "Completions": rows[0].findAll('td')[6].getText(),
        "Pass_Attempts": rows[0].findAll('td')[7].getText(),
        "Passing_Yards": rows[0].findAll('td')[8].getText(),
        "Passing_TD": rows[0].findAll('td')[9].getText(),
        "INT": rows[0].findAll('td')[10].getText(),
        "Rushing_Attempts": rows[0].findAll('td')[11].getText(),
        "Rushing_Yards": rows[0].findAll('td')[12].getText(),
        "Yards_Per_Attempt": rows[0].findAll('td')[13].getText(),
        "Rushing_TD": rows[0].findAll('td')[14].getText(),
        "Targets": rows[0].findAll('td')[15].getText(),
        "Receptions": rows[0].findAll('td')[16].getText(),
        "Receiving_Yards": rows[0].findAll('td')[17].getText(),
        "Yards_Per_Reception": rows[0].findAll('td')[18].getText(),
        "Receiving_TD": rows[0].findAll('td')[19].getText(),
        "Fumble": rows[0].findAll('td')[20].getText(),
        "Fumble_Lost": rows[0].findAll('td')[21].getText(),
        "Total_TD": rows[0].findAll('td')[22].getText(),
        "2PM": rows[0].findAll('td')[23].getText(),
        "2PP": rows[0].findAll('td')[24].getText()
    }


    context = {
        'stats': stats,
        'player_name': player_name,
        'season': season,
    }

    return render(request, 'stats/nfl_stats.html', context)






@csrf_exempt
def psa(request, cert_number):
    
    url = 'https://www.psacard.com/cert/' + str(cert_number)
    print(url)    

    
    context = {
        'url': url,
        'cert_number': cert_number,
    }

    return render(request, 'stats/psa.html', context)
