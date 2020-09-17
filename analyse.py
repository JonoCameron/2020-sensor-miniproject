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
    occuData = data['occupancy']['class1']
    co2Data = data['co2']['class1']

    tempData = tempData.dropna()
    occuData = occuData.dropna()
    co2Data = co2Data.dropna()

    tempData = tempData.sort_values(axis='index', ascending=False)
    occuData = occuData.sort_values(axis='index', ascending=False)
    co2Data = co2Data.sort_values(axis='index', ascending=False)

    medianTempData = statistics.median(tempData)
    medianOccuData = statistics.median(occuData)

    varianceTempData = statistics.variance(tempData)
    varianceOccuData = statistics.variance(occuData)

    time = data['temperature'].index
    time_change = time[1:] - time[:-1]
    for i in time_change:
        time_intervals=i.total_seconds()
    time_data = pandas.Series(time_intervals)
    time_data = time_data.sort_values(axis='index', ascending=False)
    
    meanTimeData = statistics.mean(time_data)
    varianceTimeData = time_data.var()
    
    print('The median temperature of class1 is: ', medianTempData)
    print('The variance of the temperature data of class1 is: ', varianceTempData)
    
    print('The median occupancy of class1 is: ', medianOccuData)
    print('The variance of the occupancy data of class1 is: ', varianceOccuData)
    
    print('The mean time interval is: ', meanTimeData)
    print('THe variance of time intervals is: ', varianceTimeData)

    fig1 = plt.subplot(2, 2, 1) 
    fig1.plot(occuData, norm.pdf(occuData), label='Occupancy PDF')
    plt.show()

    fig2 = plt.subplot(2, 2, 2)
    fig2.plot(tempData, norm.pdf(tempData), label='Temperature PDF')
    plt.show()

    fig3 = plt.subplot(2, 2, 3)
    fig3.plot(co2Data, norm.pdf(co2Data), label='CO2 PDF')
    plt.show()
    
    fig4 = plt.subplot(2, 2, 4)
    fig4.plot(time_data, norm.pdf(time_data), label = 'Time-interval PDF')
