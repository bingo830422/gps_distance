"""
    File name: gps_distance.py
    Author: Chu Chun Yang
    Date created: 11/09/2021
    Date last modified: 11/09/2021
    Python Version: Test on 3.8
    Requirment: argparse, pandas, geopy
    Description: Filter GPS coordinates with specific distance
"""
import argparse
from geopy.distance import distance
import pandas as pd

def parse_config():
    parser = argparse.ArgumentParser(description='arg parser')
    parser.add_argument('--gps_file', type=str, default=None, help='specify the gps file for filtering')
    parser.add_argument('--output', type=str, default="new_gps_list.csv", required=False, help='output filename')
    parser.add_argument('--dist', type=int, default=5, required=False, help='distance in meters to filter with')
    args = parser.parse_args()
    return args


args = parse_config()
# Input Filename
INPUT = args.gps_file

# Ouput Filename
OUTPUT = args.output

# Distance to filter (in meters)
THRESHOLD = args.dist

# Latitude and Longtitude Column Name in CSV File
LAT_LONG_COL_NAME = ["latitude", "longitude"]

# Output Column Nmae
OUTPUT_COL_NAME = ["secs", "nsecs", "latitude", "longitude"]

# Read GPS file
gps_list = pd.read_csv(INPUT) 

# Initial Points
coords_1 = gps_list.iloc[0][LAT_LONG_COL_NAME]
new_gps_list = pd.DataFrame(columns=OUTPUT_COL_NAME)
new_gps_list = new_gps_list.append(gps_list.iloc[0][OUTPUT_COL_NAME])

for i in range(1, len(gps_list)):
    coords_2 = gps_list.iloc[i][LAT_LONG_COL_NAME]
    if distance(coords_1, coords_2).m > THRESHOLD:
        new_gps_list = new_gps_list.append(gps_list.iloc[i][OUTPUT_COL_NAME])
        coords_1 = coords_2
    else:
        continue

new_gps_list.to_csv(OUTPUT, index=False)
