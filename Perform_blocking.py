import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

amazon_data = pd.read_csv("amazon.csv")
google_data = pd.read_csv("google.csv")


old_block_key_dic = dict()
for rowa in range(len(amazon_data)):
    for words in amazon_data['title'][rowa].split(' '):
        if words == '(' or words == ')' or words == '-':
            continue
        elif words in old_block_key_dic:
            old_block_key_dic[words] += 1
        else:
            old_block_key_dic[words] = 0

#only leave the ones with value 0 (1 occurence)
new_block_key_dic = dict()
for key, value in old_block_key_dic.items():
    if value != 0:
        new_block_key_dic[key] = []
       
        
rowa = 0
amazon_list = [['block_key', 'product_id']]
assigned_aproduct_list = []
for rowa in range(len(amazon_data)):
    for words in amazon_data['title'][rowa].split():
        for key in new_block_key_dic.keys():
            if key == words:
                if amazon_data['idAmazon'][rowa] not in assigned_aproduct_list:
                    amazon_list.append([key, amazon_data['idAmazon'][rowa]])
                    assigned_aproduct_list.append(amazon_data['idAmazon'][rowa])

        
amazon_list = "\n".join([ ",".join(x) for x in amazon_list ]) + "\n"
with open("amazon_blocks.csv", "w") as f:
    f.write(amazon_list)
    
rowg = 0
google_list = [['block_key', 'product_id']]
assigned_gproduct_list = []
for rowg in range(len(google_data)):
    for words in google_data['name'][rowg].split():
        for key in new_block_key_dic.keys():
            if key == words:
                if amazon_data['idAmazon'][rowa] not in assigned_gproduct_list:
                    google_list.append([key, google_data['id'][rowg]])
                    assigned_gproduct_list.append(google_data['id'][rowg])
                
google_list = "\n".join([ ",".join(x) for x in google_list ]) + "\n"
with open("google_blocks.csv", "w") as f:
    f.write(google_list)            
