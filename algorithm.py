#!/usr/bin/env python3
"""
This example assumes the JSON data is saved one line per timestamp (message from server).

It shows how to read and process a text file line-by-line in Python, converting JSON fragments
to per-sensor dictionaries indexed by time.
These dictionaries are immediately put into Pandas DataFrames for easier processing.

Feel free to save your data in a better format--I was just showing what one might do quickly.
"""
import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np
import statistics as statistics
from scipy.stats import norm


def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}

    with open(file, "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])

            temperature[time] = {room: r[room]["temperature"][0]}
            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}\

    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(ascending=False),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(ascending=False),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(ascending=False),
    }

    return data


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()

    file = Path(P.file).expanduser()

    data = load_data(file)

    tempData = data['temperature']['class1']

    tempData = tempData.dropna()
    tempData = tempData.sort_values(axis='index', ascending=False)

    dataLen = (len(tempData))

    lowQuart = round(dataLen/4)
    uppQuart = round(dataLen*3/4)
    IQR = tempData[uppQuart] - tempData[lowQuart]

    print(IQR)
    lowOutlier = round(tempData[lowQuart] - (4 * IQR))
    uppOutlier = round(tempData[uppQuart] + (4 * IQR))

    print(lowOutlier)
    print(uppOutlier)

    for i in range(dataLen):
        if (tempData[i] < uppOutlier) or (tempData[i] > lowOutlier):
            print(tempData[i])

#   if tempData[i] in range(lowOutlier, uppOutlier)

#if (tempData[i] < (tempData[lowQuart] - (1.5 * IQR))) or (tempData[i] > (tempData[uppQuart] - (1.5 * IQR))):
