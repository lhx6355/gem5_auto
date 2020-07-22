import sys, json, os

with open('configure_auto.json', 'r', encoding = 'utf-8') as f:
    json_data = json.load(f)

input_cmd = json_data['cmd'].split()
os_path = json_data['benchmark_path']
stats_file = json_data['--stats-file']
checkpoint_params = []

stats_resuming_name = stats_file.split('.')[0]
input_resuming_files = [os_path + stats_resuming_name + '_' + str(i + 1)  + '.txt'for i in range(json_data['checkpoint_num'])]

save_resuming_names = json_data['save_resuming_names']
out_resuming_data = {}
for i in save_resuming_names:
    out_resuming_data[i] = 0.0

input_o3_file = os_path + json_data['input_o3_file']
save_o3_names = json_data['save_o3_names']
out_o3_data = {}
for i in save_o3_names:
    out_o3_data[i] = 0.0

output_file = open(os_path + json_data['output_name'], 'w')

def print_and_write(x):
    global output_file
    if isinstance(x, list) and len(x) > 2:
        for i in x:
            print(str(i))
            output_file.write(str(i) + '\n')
    else:
        print(str(x))
        output_file.write(str(x) + '\n')

# get the checkpoint param and resuming name
for root, dirs, files in os.walk(os_path):
    for d in dirs:
        dir_split = d.split('_')
        if dir_split[0] == 'cpt.simpoint':
            checkpoint_params.append(dict(zip(dir_split[0::2], dir_split[1::2])))
checkpoint_params = sorted(checkpoint_params, key = lambda k: k.__getitem__('cpt.simpoint'))


# check the weight sum is 1.0?
sum_weight = 0.0
for i in checkpoint_params:
    sum_weight = sum_weight + float(i['weight'])
print_and_write('The sum of weight is {:<.2f}' .format(sum_weight))
print_and_write('--------------------The selected parameters-----------------')
print_and_write(save_resuming_names)
print_and_write('\n' + '-------------------The data from input file-----------------')

# get the resuming data
for index, filename in enumerate(input_resuming_files):
    file_num = filename.split('_')[-1].split('.')[0]
    flag = 0
    print_and_write('The data is from ' + filename + '~~~~~~~~~~')
    for line in open(filename, 'r'):
        line_list = line.split()
        # pass spece
        if len(line_list) > 1: 
            if line_list[0] == '----------':
                flag = flag + 1
                continue
            for save_list_name in save_resuming_names:
                if line_list[0] == save_list_name and flag > 2:
                    print_and_write(line_list[0:2])
                    checkpoint_params[int(file_num) - 1][line_list[0]] = line_list[1]
            for save_list_name in save_resuming_names:
            	if save_list_name in checkpoint_params[int(file_num) - 1]:
            	    pass
            	else:
            	    checkpoint_params[int(file_num) - 1][save_list_name] = 0.000000
    print_and_write('\n')

for i in range(len(checkpoint_params)):
    checkpoint_params[i][save_resuming_names[-3]] = float(checkpoint_params[i][save_resuming_names[-2]]) / float(checkpoint_params[i][save_resuming_names[-1]])

print_and_write(checkpoint_params)

# calculate weighted sum
for i in save_resuming_names:
    for j in range(len(checkpoint_params)):
        if checkpoint_params[j][i]:
            out_resuming_data[i] = out_resuming_data[i] + float(checkpoint_params[j]['weight']) * float(checkpoint_params[j][i])
out_resuming_data.pop(save_resuming_names[-1])
out_resuming_data.pop(save_resuming_names[-2])


print_and_write('\n' + '-------------------The data to save------------------')
for k, v in out_resuming_data.items():
    print_and_write('{:<60}{:<.6f}' .format(k, v))

# get the O3 data
for line in open(input_o3_file, 'r'):
    line_list = line.split()
    if len(line_list) > 3:
        for save_o3_name in save_o3_names:
            if line_list[0] == save_o3_name:
                out_o3_data[line_list[0]] = float(line_list[1])        
out_o3_data[save_o3_names[-3]] = float(out_o3_data[save_o3_names[-2]]) / float(out_o3_data[save_o3_names[-1]])

out_o3_data.pop(save_o3_names[-1])
out_o3_data.pop(save_o3_names[-2])

print_and_write('\n' + '-----------------------The data of O3----------------------')
for k, v in out_o3_data.items():
    print_and_write('{:<60}{:<.6f}' .format(k, v))

print_and_write('\n' + '-------------The err--------(abs(resuming - O3) / O3) * 100%-----------------')
for i, v in enumerate(out_resuming_data.values()):
    for j, k in enumerate(out_o3_data.keys()):
        if i == j:
            if out_o3_data[k] == 0.000000:
                print_and_write('{:<60}{:<}' .format(k, 'the data of O3 is zero'))
            else:
                print_and_write('{:<60}{:<.2f}%' .format(k, (abs(v - out_o3_data[k]) / out_o3_data[k]) * 100))

output_file.close
