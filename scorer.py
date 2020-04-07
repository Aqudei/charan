import json
import csv
import argparse
from math import sin, cos, sqrt, atan2, radians
from statistics import mean
import difflib


class Scorer:

    def __init__(self, args):
        self.args = args

    def load_project(self):
        with open(self.args.proj, 'rt') as fp:
            return json.load(fp)

    def compute_distance(self, loc1, loc2):
        # Earth radius=
        R = 6373.0

        lat1 = radians(abs(float(loc1['latitude'])))
        lon1 = radians(abs(float(loc1['longitude'])))
        lat2 = radians(abs(float(loc2['latitude'])))
        lon2 = radians(abs(float(loc2['longitude'])))

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance

    def load_participants(self):
        with open(self.args.data, 'rt') as fp1:
            reader = csv.reader(fp1)
            self.participants = list()

            for idx, row in enumerate(reader):
                if idx == 0:
                    header = [r.lower() for r in row]
                    continue
                item = {}
                for x, y in zip(header, row):
                    item[x] = y

                self.participants.append(item)
