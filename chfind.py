#
# (c) Chomsky-Halle Finder 2019
#
# Author: Michal Dacko
# Email: dackomichal@gmail.com
# Github: https://github.com/dachckol/
#


import csv
import sys


def create_reader(file_path):
    reader = csv.DictReader(
        open(file_path, "r")
    )
    return reader


def parse_reader(reader):
    data = {}
    for row in reader:
        sound = row["Phoneme"]
        for row_name, row_value in row.items():
            if row_name == "Phoneme" or row_value == 'N/A':
                continue

            feature = get_feature(row_name, int(row_value))

            if feature in data:
                data[feature].add(sound)
            else:
                data[feature] = set(sound)

    return data


def get_feature(feature_name, value):
    return "{value}{feature}".format(
        feature=feature_name,
        value='+' if value == 1 else '-'
    )


class NoMoreArgs(Exception):
    pass


_LAST_ARG = 1
def _read_argv():
    global _LAST_ARG
    if len(sys.argv) == _LAST_ARG:
        raise NoMoreArgs
    sound = sys.argv[_LAST_ARG]
    _LAST_ARG += 1
    return sound


def _read_input():
    return input("Enter feature (press enter to quit):")


_USING_ARGS=False
def _process_input(data):
    sound = _read_input() if not _USING_ARGS else _read_argv()
    return data.get(sound, [])


if __name__=="__main__":
    reader = create_reader("data.csv")
    data = parse_reader(reader)

    _USING_ARGS = len(sys.argv) > 1

    sounds = _process_input(data)
    while len(sounds) != 0:
        if not _USING_ARGS:
            print(' , '.join(sounds))
        try:
            more_sounds = _process_input(data)
        except NoMoreArgs:
            print(' , '.join(sounds))
            exit(-1)
        sounds = set(sounds) & set(more_sounds)
