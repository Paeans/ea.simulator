
import json

with open('result.json','r') as dfile:
  data = json.load(dfile)

# with open('cov_time.json', 'r') as cfile:
  # cdata = json.load(cfile)
  
data = sorted(data.items(), key = lambda kv:int(kv[0]))

# cov_time = {}
# for x,y in cdata:
  # cov_time[tuple(x)] = y

all_ppl = []
for gnum, [a,b] in data:
  print('generation {}'.format(gnum))
  sorted_ppl = sorted(b, key = lambda kv:sum(kv[1])/len(kv[1]))
  for ppl in sorted_ppl:#[:6]:
    if len(ppl[1]) >= 2:
      if not tuple(ppl[0]) in all_ppl:
        print('*', end='')
        all_ppl.append(tuple(ppl[0]))
      print('{}\t{:.4f}\t{}\t{}'.format(ppl[0], sum(ppl[1])/len(ppl[1]), len(ppl[1]), ' ')) #, cov_time[tuple(ppl[0])]))
