import scorer
import json
import csv
import argparse
from math import sin, cos, sqrt, atan2, radians
from statistics import mean
import difflib


def compute_distance(loc1, loc2):
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


def load_project(args):
    with open(args.proj, 'rt') as fp:
        return json.load(fp)


def load_data(args):
    with open(args.data, 'rt') as fp1:
        reader = csv.reader(fp1)
        items = list()

        for idx, row in enumerate(reader):
            if idx == 0:
                header = [r.lower() for r in row]
                continue
            item = {}
            for x, y in zip(header, row):
                item[x] = y
            items.append(item)

    return items


def compute_nearest(proj, item):
    distances = list()
    for c in proj['cities']:
        distance = compute_distance(c['location']['location'], item)
        distances.append(distance)

    return min(distances)


def is_within_100(proj, item):
    nearest = compute_nearest(proj, item)
    return nearest <= 100


def compute_score(args, proj, item):
    func = mean if args.mode == 'average' else max
    jt_score = func([difflib.SequenceMatcher(None, jt, item['jobtitle']).ratio()
                     for jt in proj['professionalJobTitles']]) * args.job_weight

    ind_score = func([difflib.SequenceMatcher(None, ind, item['industry']).ratio()
                      for ind in proj['professionalIndustry']]) * args.industry_weight

    nearest_score = compute_nearest(proj, item) * args.loc_weight

    return jt_score + ind_score + nearest_score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='participants.csv',
                        help='Path of Participants csv file.')
    parser.add_argument('--proj', default='project.json',
                        help='Path of Project data/info')
    parser.add_argument('--mode', default='average')
    parser.add_argument('--limit', default=5, type=int,
                        help='Display result limit')
    parser.add_argument('--loc-weight', default=0.40, type=float,
                        help='Location distance weight')
    parser.add_argument('--job-weight', default=0.30, type=float,
                        help='Job Title Weight')
    parser.add_argument('--industry-weight', default=0.30, type=float,
                        help='Industry Type Weight')
    args = parser.parse_args()

    scorer = scorer.Scorer(**args.__dict__)
    scorer.run()
    
    # items = load_data(args)
    # project = load_project(args)

    # processed = list()
    # for item in items:
    #     if not is_within_100(project, item):
    #         print(f"Excluding participant {item['firstname']} > 100 km")
    #         continue

    #     score = compute_score(args, project, item)
    #     item['score'] = score
    #     processed.append(item)

    # for idx, item in enumerate(sorted(processed, key=lambda x: x['score'], reverse=True)):
    #     print(item)
    #     if idx == (args.limit-1):
    #         break
