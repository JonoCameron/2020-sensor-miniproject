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
    time_intervals = [i.total_seconds() for i in time_change]
    time_data = pandas.Series(time_intervals)
    plt.figure()
    time_data.plot.density()
    plt.title('Time Interval PDF')
    plt.xlabel('Time (seconds)')

    meanTimeData = str(time_data.mean())
    varianceTimeData = str(time_data.var())
    
    print('The median temperature of class1 is: ', medianTempData)
    print('The variance of the temperature data of class1 is: ', varianceTempData)

    print('The median occupancy of class1 is: ', medianOccuData)
    print('The variance of the occupancy data of class1 is: ', varianceOccuData)

    print('The median time interval of class1 is: ', meanTimeData)
    print('The variance of the occupancy data of class1 is: ', varianceTimeData)
    
    for i in data:
        plt.figure()
        data[i]['class1'].plot.density()
        plt.title('PDF for '+i+' (class1)')
        
        if i=='temperature':
            plt.xlabel('Temperature')
        elif i == 'occupancy':
            plt.xlabel('Number of People')
        else: 
            plt.xlabel('CO2 Amount')
    plt.show()

