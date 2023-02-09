from subprocess import Popen, PIPE, STDOUT
import maskpass


usr = input('Please enter username: ')
pwd = maskpass.askpass('Please enter password: ')
command1 = ('su ' + usr).split()
command2 = 'sudo -S cat /etc/shadow'.split()

p1 = Popen(command1, stdin=PIPE, stdout=PIPE, universal_newlines=True).communicate(pwd+'\n')
clear = Popen(['clear']).wait()
p2 = Popen(command2, stdin=PIPE, stdout=PIPE, universal_newlines=True,start_new_session=False).communicate(pwd+'\n')[0].split('\n')
for i in p2:
    if usr in i and 'root' not in i:
        info = i.split(':')
        result = info[1]
        break
print('\nPassword hash of '+ usr+': '+result)