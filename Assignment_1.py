import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import json


def find_player_name(soup):
    
    # join the header and paragraphs together
    paragraphs = soup.findAll('p')
    full_paragraph = soup.h1.string + ' '
    for paragraph in paragraphs:
        full_paragraph = full_paragraph + ' ' +paragraph.get_text()
    player_names = []
    
    
    with open('tennis.json') as json_file:
        player_data = json.load(json_file)
        
    # iterate through json file and if a name in the json file matches a name in the article, check the amount
    # of characters checked until that point using .find, and return the name with the lowest number
    player_name = ''
    index = len(full_paragraph)
    for player in player_data:
        if player['name'] in full_paragraph.upper():
            index_full_name = full_paragraph.upper().find(player['name'])
            if index_full_name < index:
                player_name = player['name']
                index = index_full_name
    if player_name != '':
        return player_name
    
    return

def check_for_scores(full_paragraph):
    #search for scores in the paragraph recursively
    
    pattern = '\d+[-|\/]\d+'
    first_score = re.search(pattern, full_paragraph)
    
    # find the index of the first match of the pattern in the paragraph
    if first_score != None:
        score = re.search(pattern, full_paragraph).start()
    else:
        return
    i = 0
    
    # once you have acquired the index, keep going through character by character
    # until you reach a character other than a number or '-' '/' '(' ')'
    match_score = ''
    while full_paragraph[score+i] in '0123456789-/() ':
        match_score += full_paragraph[score+i]
        i+=1
        
    # if the found scores are less than two, it is not a valid match score
    # so return nothing, otherwise, return the score
    if len(re.findall(pattern,match_score)) < 2:
        full_paragraph = full_paragraph[score+i::]
        return check_for_scores(full_paragraph)
    else:
        return match_score

def find_match_scores(soup):
    #find the match scores and process them
    
    
    # concatenate the headline and paragraphs together
    paragraphs = soup.findAll('p')
    full_paragraph = soup.h1.string + ' '
    for paragraph in paragraphs:
        full_paragraph = full_paragraph + ' ' +paragraph.get_text()
    
    # remove the tie break points for easier calculations
    raw_scores = remove_tiebreak_points(check_for_scores(full_paragraph))
    
    # check if the returned string was empty or not, if so, also return 'None'
    if raw_scores != None:
        int_scores = [int(s) for s in re.findall('\d+',raw_scores)]
    else:
        return
    
    # conditions that check if the scores are valid scores
    i = 0
    while i < len(int_scores): 
        diff = abs(int_scores[i] - int_scores[i+1])
        
        # if both points in the score are lower than 6, return 'None'
        if int_scores[i] < 6 and int_scores[i+1] <6:
            if int_scores[i+1] < 6:
                return 
            else:
                i+=2
        # if a point in the score is 6 and the other one is higher than 8, return 'None'        
        elif int_scores[i] == 6:
            if int_scores[i+1] - int_scores[i] > 2:
                return
            else:
                i+=2
        elif int_scores[i+1] == 6:
            if int_scores[i] - int_scores[i+1] > 2:
                return
            else:
                i+=2
                
        # if both points are higher than 6 and the difference between them is
        # more than 2, return 'None'
        elif int_scores[i] > 6 and int_scores[i+1] > 6:
            if diff > 2:
                return
            else:
                i+=2
        else:
            i+=2
    return check_for_scores(full_paragraph)
    
def remove_tiebreak_points(match_scores):
    # remove the score with brackets inside for easier calculations
    # by iterating through the string until it reaches '(', then 
    # save the index until it reaches ')' and remove the content
    # from the string
    
    i = 0
    if match_scores != None:
        while i < len(match_scores):
            if match_scores[i] == '(':
                j = i
                i+=1
                while match_scores[i] != ')':
                    i+=1
                i+=1
                match_scores = match_scores[:j-1]+match_scores[i:] #becaues of spacing
                i-=j
            i+=1
        return match_scores
    else:
        return

    
def calculate_game_difference(match_scores):
    # calculate the game difference of the scores
    
    game_difference = 0
    raw_scores = remove_tiebreak_points(match_scores)
    if raw_scores != None:
        int_scores = [int(s) for s in re.findall('\d+',raw_scores)]
    else:
        return
    i = 0
    
    while i < len(int_scores): 
        diff = int_scores[i] - int_scores[i+1]
        game_difference+= diff
        i+=2
        
    # absolute value as the difference may be negative
    return abs(game_difference)



# the initiation of web crawling
# get the seed url and parse through it.
seed_url = 'http://comp20008-jh.eng.unimelb.edu.au:9889/main/'
page = requests.get(seed_url)
soup = BeautifulSoup(page.text, 'html.parser')

# make a dictionary of visited a pages and add the seed url as well
visited = {}; 
visited[seed_url] = True


# find the next URL in the page and add it to a 
# list of URLs to be visited
links = soup.findAll('a')
to_visit = []
for link in links:
    to_visit.append(urljoin(seed_url, link['href']))

    
# flags, empty lists and dictionaries to be filled in the while loop
break_while = False
headline_list = []
link_list = []
t2_headlines = []
t2_links = []
player_list = []
score_list = []
game_diff_list = []
player_dic = dict()
first_article = True

# while loop to crawl and parse through every webpage
# while calling functions to extract data
while (to_visit):
    
    # consume the list of urls
    link = to_visit.pop(0)
    link_list.append(link)
    
    # parse through the webpage to scrape
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # extract headlines
    new_headline = soup.h1.string
    headline_list.append(new_headline)
    
    # get the name of the first player in that appears in the article from the tennis.jason file.
    with open('tennis.json') as json_file:
        player_data = json.load(json_file)
    match_scores = find_match_scores(soup)
    player_name = find_player_name(soup)
    game_diff = calculate_game_difference(match_scores)
    
    # only add the data of when both functions have returned something other
    # than 'None', if 'None' is returned, do not add the information 
    # to the lists
    if find_player_name(soup) != None and find_match_scores(soup) != None:
        t2_headlines.append(new_headline)
        t2_links.append(link)
        player_list.append(player_name)
        score_list.append(match_scores)
        game_diff_list.append(game_diff)
        if player_name not in player_dic:
            player_dic[player_name] = {'frequency': 0, 'game_diff': 0, 'avg_diff': 0, 'win_percentage': 0}
        player_dic[player_name]['frequency'] += 1
        player_dic[player_name]['game_diff'] += game_diff
        for player in player_data:
            if player['name'] in player_name:
                player_dic[player_name]['win_percentage'] = float(player['wonPct'][:4])
    
    # mark the item as visited, i.e., add to visited list, remove from to_visit
    visited[link] = True
    new_links = soup.findAll('a')
    
    # this is to make sure to go on to the next page and not the previous while checking if it is in visited
    for new_link in new_links:
        new_item = new_link['href']
        new_url = urljoin(link, new_item)
        
        # check if its the first article to make sure the parsing goes through one direction
        # this is only done specifically for this assignment to order the articles
        # but to web crawl other pages, the first_article can made be False at the start
        if first_article == True:
            first_article = False
            continue
        elif new_url in visited:
            continue
        else:
            if new_url not in to_visit:
                to_visit.append(new_url)
                continue
            else:
                break_while = True

    # break the loop if no more URLs are found in to_visit
    if break_while == True:
        break
        


# TASK 1        
#put link and headline dataframe into csv file
headline = pd.Series(headline_list)
url = pd.Series(link_list)
task1 = pd.DataFrame({'url': url,'headline': headline})
task1.to_csv('task1.csv')

# TASK 2
# make the headline, URLs, players and scores into a DataFrame and convert to csv file
t2headline = pd.Series(t2_headlines)
t2link = pd.Series(t2_links)
player = pd.Series(player_list)
score = pd.Series(score_list)
task2 = pd.DataFrame({'url': t2link,'headline': t2headline, 'player': player, 'score': score})
task2.to_csv('task2.csv')

# for loop to add information into a dictionary and sort the information
# for plotting data later
task5_list = []
t3player_list = []
freq_list = []
avg_diff = []
for player in player_dic:
    player_dic[player]['avg_diff'] = player_dic[player]['game_diff']/player_dic[player]['frequency']
    task5_list.append([player_dic[player]["win_percentage"], player_dic[player]['avg_diff'], player])
    t3player_list.append(player)
    avg_diff.append(player_dic[player]['avg_diff'])
    freq_list.append([player_dic[player]['frequency'], player])

t5player_list = t3player_list
freq_list.sort()
task5_list.sort()


# TASK3
# make the players and average game difference into a Dataframe and convert to a csv file
t3player = pd.Series(t3player_list)
avg_game_difference = pd.Series(avg_diff)
task3 = pd.DataFrame({'player': t3player,'avg_game_difference': avg_game_difference})
task3.to_csv('task3.csv')

# TASK 4
# organise the players and frequency of appearance in articles into
# into a DataFrame and plot the data
top_5_player = [freq_list[-1][1],freq_list[-2][1],freq_list[-3][1],freq_list[-4][1],freq_list[-5][1]]
top_5_frequency = [freq_list[-1][0],freq_list[-2][0],freq_list[-3][0],freq_list[-4][0],freq_list[-5][0]]

fig = plt.figure(figsize = (20,10))

bar_graph = pd.DataFrame({'player': top_5_player, 'frequency': top_5_frequency})

y_pos = np.arange(len(bar_graph['player']))
plt.bar(y_pos, bar_graph['frequency'], align = 'center', alpha = 1, width = 0.5)
plt.xticks(y_pos, bar_graph['player'], fontsize = 20)
plt.yticks(fontsize = 20)
plt.ylabel('Frequency', fontsize = 25)
plt.xlabel('Players', fontsize = 25)
plt.title('Top 5 Players that appeared most Frequently in Articles', fontsize = 30, fontweight="bold")
plt.savefig('task4.png')
plt.clf()

# TASK 5
# for loop to organise player, winrate and average score difference into lists
# and make it into a DataFrame to plot a double bar plot
t5player = []
t5winrate = []
t5avg_diff = []
for player in task5_list:
    t5player.append(player[2])
    t5winrate.append(player[0])
    t5avg_diff.append(player[1])
    
t5player = pd.Series(t5player)
t5winrate = pd.Series(t5winrate)
t5avg_diff = pd.Series(t5avg_diff)
task5 = pd.DataFrame({'player': t5player, 'winrate': t5winrate, 'avg_diff': t5avg_diff})

ax = fig.add_subplot(111)
ax2 = ax.twinx() # Create the second axis fot the second set of data
width = 0.4

task5['winrate'].plot(kind='bar', color='red', ax=ax, width=width, position=1, label ='win_percentage(%)', figsize = (20, 11))
task5['avg_diff'].plot(kind='bar', color='blue', ax=ax2, width=width, position=0, label = 'avg_score_difference', figsize = (20, 11))
fig.legend(fontsize = 15)
ax.set_ylabel('win_percentage(%)', fontsize = 20)
ax.set_ylim(0, 100)
ax2.set_ylabel('avg_score_difference', fontsize = 20)
ax.set_xlabel('Player', fontsize = 20)
plt.title('The win rate and average score difference of tennis players found the articles', fontsize = 25, fontweight="bold")
ax.set_xticks(range(0,len(task5['player'])))
ax.set_xticklabels(task5['player'], rotation = 25, fontsize = 15, ha = 'right')

plt.savefig('task5.png')
plt.clf()


