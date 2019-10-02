#
# (c) Chomsky-Halle Finder 2019
#
# Author: Michal Dacko
# Email: dackomichal@gmail.com
# Github: https://github.com/dachckol/
#


import csv
import sys


def create_reader():
    reader = csv.DictReader(
        open("data.csv", "r", encoding="windows-1252"))
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


def process_input(data):
    sound = input("Enter feature (press enter to restart):")
    return data.get(sound, [])


if __name__=="__main__":
    reader = create_reader()
    data = parse_reader(reader)

    sounds = process_input(data)
    while len(sounds) != 0:
        print(' , '.join(sounds))
        more_sounds = process_input(data)
        sounds = set(sounds) & set(more_sounds)
