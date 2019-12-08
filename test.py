import json

with open('waseda.json') as json_file:
    data = json.load(json_file)
    
    print len(data['12_03_2019']['trace']['82']['hops'])