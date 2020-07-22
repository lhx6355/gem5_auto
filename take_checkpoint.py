import os, time, sys, json

with open('configure_auto.json', 'r', encoding = 'utf-8') as f:
    json_data = json.load(f)

name = json_data['benchmark_name']
warmup = json_data['warmup']
gem5_path = json_data['gem5_path']
benchmark_path = json_data['benchmark_path']
simpoint_interval = json_data['simpoint-interval']

take_checkpoint_cmd = gem5_path + 'build/X86/gem5.opt --outdir=' + benchmark_path + ' ' + gem5_path + 'configs/example/se.py -c ' + benchmark_path + name + ' ' + '--take-simpoint-checkpoint=' + benchmark_path + name + '.simpoints,' + benchmark_path + name + '.weights,' + str(simpoint_interval) + ',' + str(warmup)

print('take_checkpoint_cmd : '+ take_checkpoint_cmd)
input_user = input("Whether to contiune? [y/n] : ")
if input_user == 'y':
    os.system(take_checkpoint_cmd)


