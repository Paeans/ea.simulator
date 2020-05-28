import os, shlex, sys
import subprocess
import time

import numpy as np

def update_testFC (RA,TMR,testnum):
	ff=open("testFC.py", "r+")
	i=0
	data= ff.readlines()
	for line in data:
		i+=1
		if  'RA=' in line:
			data[i-1]='RA=' + str(RA) +'\n'
		if  'TMR=' in line:
			data[i-1]='TMR=' + str(TMR) +'\n'
		if  'testnum=' in line:
			data[i-1]='testnum=' + str(testnum) +'\n'

	ff.seek(0)
	ff.truncate()
	ff.writelines(data)
	ff.close()


def update_diff1 (gain1):
	ff=open("diff1.sp", "r+")
	i=0
	data= ff.readlines()
	for line in data:
		i+=1
		if  'R3' in line:
			data[i-1]='R3 n1 out ' + str(gain1) +'k\n'
		if  'R4' in line:
			data[i-1]='R4 n2 0 ' + str(gain1) +'k\n'

	ff.seek(0)
	ff.truncate()
	ff.writelines(data)
	ff.close()

def update_diff2 (gain2):
	ff=open("diff2.sp", "r+")
	i=0
	data= ff.readlines()
	for line in data:
		i+=1
		if  'R3' in line:
			data[i-1]='R3 n1 out ' + str(gain2) +'k\n'
		if  'R4' in line:
			data[i-1]='R4 n2 0 ' + str(gain2) +'k\n'

	ff.seek(0)
	ff.truncate()
	ff.writelines(data)
	ff.close()

def update_diff3 (gain3):
	ff=open("diff3.sp", "r+")
	i=0
	data= ff.readlines()
	for line in data:
		i+=1
		if  'R3' in line:
			data[i-1]='R3 n1 out ' + str(gain2) +'k\n'
		if  'R4' in line:
			data[i-1]='R4 n2 0 ' + str(gain2) +'k\n'

	ff.seek(0)
	ff.truncate()
	ff.writelines(data)
	ff.close()

def update_diff4 (gain4):
	ff=open("diff4.sp", "r+")
	i=0
	data= ff.readlines()
	for line in data:
		i+=1
		if  'R3' in line:
			data[i-1]='R3 n1 out ' + str(gain2) +'k\n'
		if  'R4' in line:
			data[i-1]='R4 n2 0 ' + str(gain2) +'k\n'

	ff.seek(0)
	ff.truncate()
	ff.writelines(data)
	ff.close()

def update_diff5 (gain5):
	ff=open("diff5.sp", "r+")
	i=0
	data= ff.readlines()
	for line in data:
		i+=1
		if  'R3' in line:
			data[i-1]='R3 n1 out ' + str(gain2) +'k\n'
		if  'R4' in line:
			data[i-1]='R4 n2 0 ' + str(gain2) +'k\n'

	ff.seek(0)
	ff.truncate()
	ff.writelines(data)
	ff.close()

testnum=200   #This is NOT a tunable parameter, it is just the number of test inputs you want to use from MNIST data set; Its max value is 10000
#The lower the testnum is the faster the optimization but it might not be accurate since you are not using the entire dataset



RA=sys.argv[7] + 'e-12' #10e-12   #ranges from 5e-12 to 20e-12 with "5e-12" steps 
TMR=int(sys.argv[8]) * 50 # 100	    #ranges from 100 to 400 with "50" steps
gain1=sys.argv[2]    #ranges from 5 to 20 with "1" steps
gain2=sys.argv[3]    #ranges from 5 to 20 with "1" steps
gain3=sys.argv[4]    #ranges from 5 to 20 with "1" steps
gain4=sys.argv[5] #10    #ranges from 5 to 20 with "1" steps
gain5=sys.argv[6] #10    #ranges from 5 to 20 with "1" steps




plist = []
index = 0
st_time = time.time()
image = np.random.choice(range(10000/testnum), 3, replace = False)
print(':'.join([str(x) for x in image]))
for i in image: #np.random.choice(range(100), 6, replace = False):
  curr = os.getcwd()
  os.chdir(sys.argv[1] + '/p' + str(index))
  update_testFC (RA,TMR,testnum)
  update_diff1 (gain1)
  update_diff2 (gain2)
  update_diff2 (gain3)
  plist.append(subprocess.Popen(
      shlex.split('bash -c \'python testFC.py {} | grep " = " \''.format(i * testnum)), 
      stdout = subprocess.PIPE,
      close_fds = True))
  os.chdir(curr)
  index += 1

tag = True
err_rate = 0.0  
while(tag):
  time.sleep(1)
  tag = False
  for i in range(len(plist)):
    proc = plist[i]
    if proc == None:
      continue
    tag = True
    if proc.poll() == None:
      continue
    output = proc.stdout.read().split('\n')
    err_rate += float(output[0].split('=')[1].strip())
    plist[i] = None
#print(sys.argv[1] + ':' + gain1 + ':' + gain2 + ':' + gain3 + ':' + str(err_rate/index))
print('{}:{}:{}:{}:{}:{}:{}:{}:{:.4f}'.format(sys.argv[1], gain1, gain2, gain3,gain4,gain5,sys.argv[7],sys.argv[8], err_rate/index))
print('TM:{:0>8.2f}'.format(time.time() - st_time))
'''
os.chdir(sys.argv[1] + '/p0')
output = os.popen('python testFC.py {} | grep " = " '.format(10*testnum)).read().split('\n')
print(output)
''' 
