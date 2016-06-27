"""
example read for json file
"""
import json
from collections import OrderedDict

filename = 'testdata/bondurant.json'
with open(filename,'r') as f:
    week_list = json.load(f,object_pairs_hook=OrderedDict)

#
# print valid forecast periods for each week
#
for week in week_list:
    print(week['valid'])

#
# print temperatures for week3 (index starts at 0)
#
temps = week_list[2]['temps']
print(temps)
