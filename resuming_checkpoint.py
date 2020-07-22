from multiprocessing import Pool
import os, time, sys, json

with open('configure_auto.json', 'r', encoding = 'utf-8') as f:
    json_data = json.load(f)

process_num = json_data['cpu_num']
checkpoint_num = json_data['checkpoint_num']
name = json_data['benchmark_name']
gem5_path = json_data['gem5_path']
benchmark_path = json_data['benchmark_path']
stats_file = json_data['--stats-file']

input_cmd = (gem5_path + 'build/X86/gem5.opt --outdir=' + benchmark_path + ' --stats-file=' + stats_file + ' ' + gem5_path + 'configs/example/se.py -c ' + benchmark_path + name + ' --cpu-type=DerivO3CPU --caches ' + json_data['cmd'] + ' --restore-simpoint-checkpoint -r 1 --checkpoint-dir ' + benchmark_path).split()

print(input_cmd)
for index, i in enumerate(input_cmd):
    a = i.split('=')
    if a[0] == '--stats-file': 
        stats_name_index = index

# generate the cmd list
cmd_list = ['' for n in range(checkpoint_num)]
for i in range(checkpoint_num):
    for index, j in enumerate(input_cmd):
        if index == input_cmd.index('-r') + 1:
            cmd_list[i] = cmd_list[i] + str(i + 1) + ' '
        elif index == stats_name_index:
            cmd_list[i] = cmd_list[i] + j.split('.')[0] + '_' + str(i + 1) + '.txt' + ' '
        else:
            cmd_list[i] = cmd_list[i] + j + ' '
print("----------Will execute the following commands----------" + '\n')
for i in cmd_list:
    print(i)
input_user = input("Whether to contiune? [y/n] : ")

def gem5_start(i):
    global cmd_list
    os.system(cmd_list[i])
if input_user == 'y':
    p = Pool(int(process_num))
    starttime = time.time()
    print(starttime)
    for i in range(checkpoint_num):
        time.sleep(1) 
        p.apply_async(gem5_start, args=(i,))
    p.close()
    p.join()
    endtime = time.time()
    print(endtime)
    print(endtime - starttime)
    print("----------gem5 is over!!!----------" + '\n' + '\n')
    sys.exit(1)
else:
    print("----------gem5 don't executed!!!----------" + '\n' + '\n')
    sys.exit(0)
