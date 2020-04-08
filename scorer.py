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
        self.name = kwargs['name']
        self.professionalJobTitles = kwargs['professionalJobTitles']
        self.professionalIndustry = kwargs['professionalIndustry']
        self.education = kwargs['education']

        self.locations = list([c['location']['location']
                               for c in kwargs['cities']])

        def __str__(self):
            return self.name


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
        self.score = 0

    def __str__(self):
        return f"First Name: {self.firstName}, Job Title: {self.jobTitle}, Score: {self.score}"


class Scorer:

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs

        self.participants = []
        self.project = None

    def loadProject(self):
        with open(self.kwargs['proj'], 'rt') as fp:
            self.project = Project(**json.load(fp))

    def computeDistance(self, loc1, loc2):
        # Earth radius
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

    def computeNearestFromProject(self, participant):
        distances = list()
        for loc in self.project.locations:
            distance = self.computeDistance(
                loc, {"latitude": participant.latitude, "longitude": participant.longitude})
            distances.append(distance)

        return min(distances)

    def isWithin100(self, proj, item):
        nearest = self.computeNearestFromProject(item)
        return nearest <= 100

    def computeScore(self, participant):
        func = mean if self.kwargs['mode'] == 'average' else max

        jt_score = func([difflib.SequenceMatcher(None, jt, participant.jobTitle).ratio()
                         for jt in self.project.professionalJobTitles]) * self.kwargs['job_weight']

        ind_score = func([difflib.SequenceMatcher(None, ind, participant.industry).ratio()
                          for ind in self.project.professionalIndustry]) * self.kwargs['industry_weight']

        nearest_distance = self.computeNearestFromProject(participant)

        nearest_score = (-0.01 * (nearest_distance)) + 1

        weighted_nearest_score = nearest_score * self.kwargs['loc_weight']

        return jt_score + ind_score + weighted_nearest_score

    def run(self):
        self.loadProject()
        self.loadParticipants()

        print(self.project)
        processing = list([participant for participant in self.participants if self.isWithin100(
            self.project, participant)])

        for participant in processing:
            participant.score = self.computeScore(participant)

        for p in sorted(processing, key=lambda x: x.score, reverse=True):
            print(p)
