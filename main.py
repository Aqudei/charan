import scorer
import json
import csv
import argparse
from math import sin, cos, sqrt, atan2, radians
from statistics import mean
import difflib


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
