#!/usr/bin/env python

import csv
import json
import re
import locale
import argparse
import datetime
from dateutil.relativedelta import relativedelta

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def date_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

# required arg
parser = argparse.ArgumentParser()
parser.add_argument('start_date')
parser.add_argument('end_date')
parser.add_argument('price')
parser.add_argument('out_filename')

args = parser.parse_args()

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')


start_date = args.start_date
end_date = args.end_date
out_filename_csv = args.out_filename + ".csv"
out_filename_json = args.out_filename + ".json"
price = float(args.price)

start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')

delta_date = start_date_obj - end_date_obj
delta_month = diff_month(end_date_obj, start_date_obj)

price_per_month = price / delta_month

parsed_res = []

print(price_per_month)

for x in range(0, delta_month):
    three_mon_rel = relativedelta(months=x)

    new_date = start_date_obj + three_mon_rel
    new_price = price - price_per_month * x

    #print(new_date, new_price)

    dict = {'date': new_date,
        'close': new_price
        }

    parsed_res.append(dict)


dict_json = {
    'start_date' : start_date_obj,
    'end_date' : end_date_obj,
    'initial_value' : price,
    'loss_of_value_per_month' : price_per_month,
    'data' : parsed_res
}

with open(out_filename_csv, mode='w') as csv_file:
    fieldnames = parsed_res[0].keys()
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()

    for dataset in parsed_res:
        writer.writerow(dataset)

with open(out_filename_json, 'w') as json_file:
  json.dump(dict_json, json_file, default = date_converter)