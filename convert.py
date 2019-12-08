import json
import os
import math


def get_paths():

    dates = ["11_28_2019", "11_29_2019", "11_30_2019", "12_01_2019", "12_02_2019", "12_03_2019", "12_04_2019",
             "12_05_2019", "12_06_2019"]
    links = []
    final_path = []

    basepath = 'data/'
    for entry in os.listdir(basepath):
        links.append(entry)
        print entry

    for link in links:
        path = basepath + link

        for date in dates:
            final_path.append(path + '/' + date)

    return final_path


def get_ping_data(filepath):

        f = open(filepath, "r")
        lines = f.readlines()
        dic = {}
        for line in lines:
            tokens = line.split(' ')
            if tokens[0].__contains__('Time'):

                time_dict = {}
                time_dict['month'] = tokens[2]

                if tokens[2] == 'Dec':
                    time_dict['date'] = tokens[4]
                    chunks = tokens[5].split(':')
                    time_dict['hour'] = chunks[0]
                    time_dict['minute'] = chunks[1]
                    time_dict['second'] = chunks[2]
                else:
                    time_dict['date'] = tokens[3]
                    chunks = tokens[4].split(':')
                    time_dict['hour'] = chunks[0]
                    time_dict['minute'] = chunks[1]
                    time_dict['second'] = chunks[2]

                dic['time'] = time_dict

            elif tokens[0].__contains__('PING'):

                dic['des'] = tokens[1]
                dic['IP'] = tokens[2][1:len(tokens[2])-1]

            elif tokens[0].__contains__('rtt'):

                chunks = tokens[3].split('/')
                rtt_dic = {}
                rtt_dic['min'] = chunks[0]
                rtt_dic['max'] = chunks[1]
                rtt_dic['avg'] = chunks[2]
                rtt_dic['mdev'] = chunks[3]

                dic['rtt'] = rtt_dic

            elif line.__contains__('packets'):

                packet_dict = {}

                packet_dict['transmitted'] = tokens[0]
                packet_dict['received'] = tokens[3]
                packet_dict['loss'] = tokens[5][:len(tokens[5])-1]
                packet_dict['time'] = tokens[9][:len(tokens[9])-4]

                dic['packets'] = packet_dict

        return dic


def get_trace_data(filepath):

    f = open(filepath, "r")
    lines = f.readlines()
    dic = {}
    if len(lines) == 0:
        return -1
    tokens = lines[0].split(' ')
    info_dict = {}
    info_dict['des'] = tokens[2]
    info_dict['IP'] = tokens[3][1:len(tokens[2])-1]
    info_dict['max_hop'] = tokens[4]
    info_dict['p_size'] = tokens[7]

    dic['info'] = info_dict

    hop = {}
    index = 1
    for line in lines[1:]:
        hop_dict = {}
        tokens = line.split(' ')
        print tokens
        if tokens[0] == '':
            shift = 1
            if tokens[shift].__contains__('*') or tokens[3].__contains__(''):
                continue
            hop_dict['index'] = tokens[shift]
            hop_dict['node'] = tokens[shift+2]
            if tokens[shift + 2] == '*':
                hop_dict['node'] = "***"
                continue
            hop_dict['IP'] = tokens[shift+3][1:len(tokens[2])-1]
            hop_dict['time_1'] = tokens[shift+5]
            if shift+8 >= len(tokens):
                continue
            hop_dict['time_2'] = tokens[shift+8]
            if shift + 11 >= len(tokens):
                continue
            hop_dict['time_3'] = tokens[shift+11]
        else:
            shift = 0
            hop_dict['index'] = tokens[shift]
            if shift+2>=len(tokens):
                continue
            hop_dict['node'] = tokens[shift + 2]
            if tokens[shift + 2].__contains__('*'):
                hop_dict['node'] = "***"
                continue
            hop_dict['IP'] = tokens[shift + 3][1:len(tokens[2]) - 1]
            hop_dict['time_1'] = tokens[shift + 5]
            if shift + 8 >= len(tokens):
                continue
            hop_dict['time_2'] = tokens[shift + 8]
            if shift + 11 >= len(tokens):
                continue
            hop_dict['time_3'] = tokens[shift + 11]

        hop[str(index)] = hop_dict
        if hop_dict['node'] == info_dict['des']:
            break
        index += 1

    dic['hops'] = hop

    return dic


def main():

    paths = get_paths()
    connection_dic = {}

    for path in paths:

        tokens = path.split('/')
        connection = tokens[1]
        date = tokens[2]

        print connection + '/' + date
        
        file_list = []
        for entry in os.listdir(path):
            if os.path.isfile(os.path.join(path, entry)):
                file_list.append(entry)
        
        ping_dict = {}
        index = 1
        for filepath in file_list:
            if filepath.__contains__('ping'):
                targetpath = path+'/'+filepath
                dic = get_ping_data(targetpath)
                ping_dict[str(index)] = dic
                index += 1
        
        trace_dict = {}
        index = 1
        for filepath in file_list:
            if filepath.__contains__('trace'):
                targetpath = path + '/' + filepath
                dic = get_trace_data(targetpath)
                trace_dict[str(index)] = dic
                index += 1
        
        final_dict = {}
        final_dict['ping'] = ping_dict
        final_dict['trace'] = trace_dict
        connection_dic[str(date)] = final_dict

        if str(date) == "12_06_2019":
            name = connection + '.json'
            with open(name, "w") as write_file:
                json.dump(connection_dic, write_file)
            connection_dic = {}


main()