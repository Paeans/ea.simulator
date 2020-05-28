
import os, sys
import subprocess
import shlex

import numpy as np
import json
import time

import os.path

# mlist = [''.join(['00', str(x+1)])[-2:] for x in range(8)]
# l-3d22- ['01','02','03','04','05','06','07','09','11','12','13','14','15','16','18','19']
# mlist = ['01','02','03','04','05','06','07','08']
mlist = ['{:0>2d}'.format(x + 1) for x in range(16)] 
plist = {x:None for x in mlist}
mutstep = 1 # the mutation step
gnum = 20
topps = 6

def addproc(gain1, gain2, gain3, gain4, gain5, ra, tmr):
  mid = [d for d in plist.keys() if plist[d] == None]
  if not mid:
    return None
  cmd_line = 'ssh -p 222 -o ConnectTimeout=5 gpan@l-' + \
    mid[0] + ' \'bash -ic "date; cd simulator.dnn; python test.py m' + \
    mid[0] + ' ' + str(gain1) + ' ' + str(gain2) + ' ' +str(gain3) + ' ' + \
    str(gain4) + ' ' + str(gain5) + ' ' + str(ra) + ' ' + str(tmr) + \
    ' 2>error.txt; date;" \''
  #print(cmd_line)
  proc = subprocess.Popen(
    shlex.split(cmd_line),
    stdin = subprocess.PIPE,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
    close_fds = True)
  plist[mid[0]] = proc
  return proc

def retproc():
  for d in plist.keys():
    if plist[d] == None or plist[d].poll() == None:
      continue
    output = plist[d].stdout.read().split('\n')
    plist[d] = None
    return output
  return None

def ispsok(new_ps):
  blist = [5,5,5,5,5,5,1]
  ulist = [50,50,50,50,50,30,10]
  for i in range(len(new_ps)):
    if new_ps[i] < blist[i] or new_ps[i] > ulist[i]:
      return False
  return True

def crossover(p1, p2, ppool):
  count = 0
  size = len(p1)
  while count < 2**size * 3:
    pid = np.random.randint(2, size = (size,))
    mutval = np.random.randint(mutstep * 2 + 1, size = (size,))
    new_ps = [[p1[i], p2[i]][pid[i]] + mutval[i] for i in range(size)]
    if ispsok(new_ps) and not tuple(new_ps) in ppool.keys():
      return tuple(new_ps)
    count += 1
  return None

def gettop(ppool, num):
  sorted_pool = sorted(ppool.items(), key=lambda kv:sum(kv[1])/len(kv[1]))
  print([(x,sum(y)/len(y)) for x, y in sorted_pool[:num]])
  return [x for x, y in sorted_pool[:num]]

def evalppl(pps, ppool, num):
  for a,b,c,d,e,f,g in [x for i in range(num) for x in pps ]:
    proc = addproc(a,b,c,d,e,f,g)
    while proc == None:
      output = retproc()
      if output == None:
        time.sleep(1)
        continue
      # print(output)
      res = output[2].split(':')
      tname = tuple([int(x) for x in res[1:8]]) # int(res[1]), int(res[2]), int(res[3])])
      if tname in ppool.keys():
        ppool[tname].append(float(res[8]))
      else:
        ppool[tname] = [float(res[8])]
      proc = addproc(a,b,c,d,e,f,g)

  while [d for d in plist.keys() if not plist[d] == None] :
    output = retproc()
    if output == None:
      time.sleep(1)
    else:
      # print(output)
      res = output[2].split(':')
      tname = tuple([int(x) for x in res[1:8]])
      if tname in ppool.keys():
        ppool[tname].append(float(res[8]))
      else:
        ppool[tname] = [float(res[8])]
      

# RA=10e-12   #ranges from 5e-12 to 20e-12 with "5e-12" steps 
# TMR=100	    #ranges from 100 to 400 with "50" steps
# gain1=10    #ranges from 5 to 50 with "1" steps
# gain2=10    #ranges from 5 to 50 with "1" steps
# gain3=10    #ranges from 5 to 50 with "1" steps
# gain4=10    #ranges from 5 to 50 with "1" steps
# gain5=10    #ranges from 5 to 50 with "1" steps
def run_simulator():
  print('ST:', time.ctime())
  rec_json = {}

  # initial population [(5,5,5),(25,25,25),(35,35,35),(50,50,50)]
  if os.path.isfile('result.json'):
    with open('result.json', 'r') as dfile:
      data = json.load(dfile)
      stgen, stpool = sorted(data.items(), key = lambda kv:int(kv[0]))[-1]
      stgen = int(stgen) + 1
      ppool = {tuple(x):y for [x,y] in stpool[1]}
  else:
    stgen = 0
    ppl = [(5,5,5,5,5,5,2),(15,15,15,15,15,10,4),(25,25,25,25,25,15,6),(30,30,30,30,30,20,4),(35,35,35,35,35,25,8),(40,40,40,40,40,30,8)] # initial population
    ppool = {}
    print('generation 0', time.ctime())
    evalppl(ppl, ppool, 16)    
    print(ppl)
    rec_json[stgen] = [ppl, sorted(ppool.items(), key=lambda kv:kv[1])]
    with open('result.json', 'w') as res_file:
      json.dump(rec_json, res_file)
    stgen += 1

  for i in range(gnum):  
    ppl = gettop(ppool, topps)
    new_ppl = list(set([crossover(x,y, ppool) for x in ppl for y in ppl if ppl.index(x) < ppl.index(y)]))
    print('generation {}'.format(i+1), time.ctime())
    evalppl([x for x in new_ppl if not x== None], ppool, 2)
    print(sorted([(x, sum(ppool[x])/len(ppool[x])) for x in new_ppl if not x == None], key = lambda kv:kv[1]))
    top_new = gettop({x:ppool[x] for x in new_ppl if not x == None}, 5)
    evalppl([x for x in top_new if not x == None], ppool, 16)    
    print(sorted([(x, sum(ppool[x])/len(ppool[x])) for x in top_new if not x == None], key = lambda kv:kv[1]))    
    rec_json[stgen] = [new_ppl, sorted(ppool.items(), key=lambda kv:kv[1])]
    with open('result.json', 'w') as res_file:
      json.dump(rec_json, res_file)
    stgen += 1
    
  gettop(ppool, topps)

  # with open('result.json', 'w') as res_file:
  #  json.dump(rec_json, res_file)

  print('EN:', time.ctime())

def run_evaluation(params): # params (5,5,5,10,10,10,2)
  print('ST:', time.ctime())
  ppl = [params] 
  result = {}
  evalppl(ppl, result, 16)
  print(result)
  print('EN:', time.ctime())

if __name__ == "__main__":
  run_simulator()
  #params = (40, 38, 23, 10, 10, 10, 2)
  #run_evaluation(params)
  