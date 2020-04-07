import json
import csv
import argparse
from math import sin, cos, sqrt, atan2, radians
from statistics import mean
import difflib


class Project:
    def __init__(self, *args, **kwargs):
        self.numberOfParticipants = kwargs['numberOfParticipants']
        self.timezone = kwargs['timezone']
        self.locations = []
        self.name = kwargs['name']
        self.professionalJobTitles = kwargs['professionalJobTitles']
        self.professionalIndustry = kwargs['professionalIndustry']
        self.education = kwargs['education']


class Participant:
    def __init__(self, *args, **kwargs):
        # import pdb; pdb.set_trace()
        self.firstName = kwargs['firstName']
        self.gender = kwargs['gender']
        self.jobTitle = kwargs['jobTitle']
        self.industry = kwargs['industry']
        self.city = kwargs['city']
        self.latitude = kwargs['latitude']
        self.longitude = kwargs['longitude']


class Scorer:

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs

        self.participants = []
        self.project = None

    def loadProject(self):
        with open(self.kwargs['proj'], 'rt') as fp:
            self.project = Project(**json.load(fp))

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

    def loadParticipants(self):
        with open(self.kwargs['data'], 'rt') as fp1:
            reader = csv.reader(fp1)

            for idx, row in enumerate(reader):
                if idx == 0:
                    header = [r for r in row]
                    continue
                item = {}
                for x, y in zip(header, row):
                    item[x] = y

                self.participants.append(Participant(**item))
