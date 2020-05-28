for i in `seq 1 50`; do t=00$i; t=${t: -2}; echo l-$t; ssh -p 222 gpan@l-$t -o ConnectTimeout=2 -t 'top -d .5 -n 2 | grep Cpu'; done 2>/dev/null
# for i in `seq 1 36`; do t=00$i; t=${t: -2}; echo l-1d43-$t; ssh -p 222 gpan@l-1d43-$t -o ConnectTimeout=2 -t 'top -d .5 -n 2 | grep Cpu'; done 2>/dev/null
# for i in `seq 1 20`; do t=00$i; t=${t: -2}; echo l-3d22-$t; ssh -p 222 gpan@l-3d22-$t -o ConnectTimeout=2 -t 'top -d .5 -n 2 | grep Cpu'; done 2>/dev/null
