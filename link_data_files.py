
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

amazon_small_data = pd.read_csv("amazon_small.csv")
google_small_data = pd.read_csv("google_small.csv")

#to compare each row in amazon_small.csv with each row in google_small.csv

task1a_list = []

for rowa in range(len(amazon_small_data)):
    sum1 = 0
    task1a_list.append([])
    for rowg in range(len(google_small_data)):
        #to compare the title:
        title = fuzz.token_set_ratio(amazon_small_data['title'][rowa], google_small_data['name'][rowg])
        if title > sum1:
            sum1 = title
            task1a_list[-1] = [amazon_small_data['idAmazon'][rowa], google_small_data['idGoogleBase'][rowg], title]

task1a_dic = dict()
for match in task1a_list:
    same_matches = []
    for match2 in task1a_list:
        if match[1] == match2[1]:
            same_matches.append(match2)
    task1a_dic[match[1]] = same_matches
task1a_list = [['idAmazon','idGoogleBase']]

# now only leave the highest one for each 
for value in task1a_dic.values():
    high = 0
    for matches in value:
        if matches[2] > high:
            high = matches[2]
            real_match = [matches[0],matches[1]]
    task1a_list.append(real_match)
            
            

task1a_list = "\n".join([ ",".join(x) for x in task1a_list ]) + "\n"
with open("task1a.csv", "w") as f:
    f.write(task1a_list)
