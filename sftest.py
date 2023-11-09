import subprocess
import time

process= subprocess.Popen('stockfish', stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
process.stdin.write('xboard\n')
process.stdin.write('protover 2\n')
process.stdin.write('option EvalFile=janggi-4d3de2fee245.nnue\n')
process.stdin.write('option Use NNUE=1\n')
process.stdin.write('option VariantPath=variants.ini\n')
process.stdin.flush()
#process.stdin.write('option UCI_AnalyseMode=1')# 이거 쓰면 move 안함, eval만 받을 수 있음
process.stdin.write('new\n')
process.stdin.write('variant {}\n'.format('janggi_ehehHEEH'))
process.stdin.write('eval\n')
process.stdin.flush()
while True:
    line=process.stdout.readline()
    if line.startswith('Final evaluation'):
        loc=line.find('+') if line.find('+')!=-1 else line.find('-')
        print(line[loc:loc+5])
        break
process.stdin.write('d\n')
process.stdin.flush()
for i in ' '*24:
    line=process.stdout.readline()
    print(line)
while True:
    user=input()
    process.stdin.write('usermove {}\n'.format(user))
    process.stdin.flush()
    time.sleep(2)
    process.stdin.write('?\n')
    process.stdin.flush()
    while True:
        line=process.stdout.readline()
        if line.startswith('move'):
            print(line.split()[-1])
            break
    process.stdin.write('eval\n')
    process.stdin.flush()
    while True:
        line=process.stdout.readline()
        if line.startswith('Final evaluation'):
            loc=line.find('+') if line.find('+')!=-1 else line.find('-')
            print(line[loc:loc+5])
            break
    process.stdin.write('d\n')
    process.stdin.flush()
    for i in ' '*24:
        line=process.stdout.readline()
        print(line)

process.kill()