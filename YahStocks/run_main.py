import sys
from subprocess import Popen

bin_path = sys.argv[1]
symbol_path = sys.argv[2]

symbolFile = open(symbol_path, 'r')
procs = []
for stockline in symbolFile.readlines():
    path2Exe = str(bin_path)+"\Debug\DailyAndRTMain.exe "
    args = stockline.split('=')[1]
    args = args.split('-s')
    args = ['-s' + val for val in args]
    procs.append(Popen([path2Exe] + args))
for p in procs:
    p.wait()
    
