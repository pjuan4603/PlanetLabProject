import json
import os


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


def main():

    """
    paths = get_paths()

    for path in paths:
        file_list = []
        for entry in os.listdir(path):
            if os.path.isfile(os.path.join(path, entry)):
                file_list.append(entry)

        for file in file_list:
    """
    f = open("data/hk2washington/11_28_2019/ping_1.txt", "r")
    lines = f.readlines()
    dic = {}
    time_dict = {}
    for line in lines:
        tokens = line.split(' ')
        print tokens
        if tokens[0].__contains__('Time'):
            time_dict['month'] = tokens[2]
            time_dict['date'] = tokens[3]
            chunks = tokens[4].split(':')
            time_dict['hour'] = chunks[0]
            time_dict['minute'] = chunks[1]
            time_dict['second'] = chunks[2]

            dic['time'] = time_dict



main()