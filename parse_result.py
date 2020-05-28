
import json

with open('result.json','r') as dfile:
  data = json.load(dfile)
  
data = sorted(data.items(), key = lambda kv:int(kv[0]))

for gnum, [a,b] in data:
  print('generation {}'.format(gnum))
  sorted_ppl = sorted(b, key = lambda kv:sum(kv[1])/len(kv[1]))
  for ppl in sorted_ppl:
    if len(ppl[1]) >= 1:
      print('{}\t{:.4f}\t{}'.format(ppl[0], sum(ppl[1])/len(ppl[1]), len(ppl[1])))
