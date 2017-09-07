#!/usr/bin/env python3
# centennial_Y2K.csv is a slightly-cleaned-up-in-Excel CSV version
# of the https://earthquake.usgs.gov/data/centennial/ catalog file,
# which is in fixed-width FORTRAN-style format.

import calendar
import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt

def read_magnetometer():
    goes = 6
    year = 1986
    month = 1
    start_day = 1
    end_day = 31

    format_str = 'g{goes:02}_magneto_1m_{year:04}{month:02}{start_day:02}_{year:04}{month:02}{end_day:02}.csv'
    
    print("Collecting files")
    files = []
    for year in range(1986,2009):
    # for year in range(1986,1987):
        for month in range(1, 13):
            start_day = 1
            (_, end_day) = calendar.monthrange(year, month)
            g6 = format_str.format(
                    goes=6,
                    year=year,
                    month=month,
                    start_day=start_day,
                    end_day=end_day
                    )
            g8 = format_str.format(
                    goes=8,
                    year=year,
                    month=month,
                    start_day=start_day,
                    end_day=end_day
                    )
            g10 = format_str.format(
                    goes=10,
                    year=year,
                    month=month,
                    start_day=start_day,
                    end_day=end_day
                    )
            if os.path.isfile(g6):
                files.append(g6)
            elif os.path.isfile(g8):
                files.append(g8)
            elif os.path.isfile(g10):
                files.append(g10)
    dat = []
    for f in files:
        print("Reading file", f)
        with open(f, 'r') as fdata:
            # Headers aren't always the same size.  :/
            # So we have to skip past it manually.
            line = fdata.readline()
            while line.strip() != 'data:':
                # print("Line is: '{}'".format(line))
                line = fdata.readline()
                continue
            dat.append(pd.read_csv(fdata))
    # print(dat)
    full_dataset = pd.concat(dat)
    # -99999.0 is used as an "invalid" reading
    print("Cleaning data")
    clean_dataset = full_dataset[full_dataset.hp != -99999.0]
    clean_dataset = clean_dataset[clean_dataset.he != -99999.0]
    clean_dataset = clean_dataset[clean_dataset.hn != -99999.0]
    clean_dataset = clean_dataset[clean_dataset.ht != -99999.0]

    # Now we parse and add an ordinal time column
    # The GOES time columns are like this: 2006-04-02 12:01:00.000
    def make_date(row):
        return datetime.datetime.strptime(row.time_tag, '%Y-%m-%d %H:%M:%S.000').timestamp()

    print("Translating dates")
    dates = clean_dataset.apply(make_date, axis=1)
    clean_dataset = clean_dataset.assign(ordtime=dates)

    print("Normalizing magnetometer data")
    d = clean_dataset
    d.hp = (d.hp - d.hp.mean())  / (d.hp.max() - d.hp.min())
    d.he = (d.he - d.he.mean())  / (d.he.max() - d.he.min())
    d.hn = (d.hn - d.hn.mean())  / (d.hn.max() - d.hn.min())
    d.ht = (d.ht - d.ht.mean())  / (d.ht.max() - d.ht.min())
    return d

def read_quakes():
    print("Reading quakes file")
    quakes = pd.read_csv('centennial_Y2K.csv')
    # We just skip past any earthquakes before 1986
    recent_quakes = quakes[quakes.yr > 1985]

    # Now we add an absolute ordinal time column, so we can compare
    # apples to apples easily.
    def make_date(row):
        return datetime.datetime(row.yr, row.mon, row.day, row.hr, row['min'], int(row.sec)).timestamp()
        # print(x)
    # ord_date = date.timestamp()
    print("Translating dates")
    dates = recent_quakes.apply(make_date, axis=1)
    recent_quakes = recent_quakes.assign(ordtime=dates)

    print("Normalizing quakes")
    q = recent_quakes
    q.mag = (q.mag - q.mag.mean())  / (q.mag.max() - q.mag.min())
    return q

def read_cached(reader, cachename):
    if os.path.isfile(cachename):
        print("Using cached file", cachename)
        return pd.read_csv(cachename)
    else:
        print("No cached file found")
        d = reader()
        print("Saving cache to", cachename)
        d.to_csv(cachename)
        return d

def main():

    q = read_cached(read_quakes, 'quake.cache')


    d = read_cached(read_magnetometer, 'mag.cache')

    # print("Plotting quakes")
    # plt.plot(q.ordtime, q.mag)
    # print("Plotting magnetometer data")
    # plt.plot(d.ordtime, d['hp'])
    # plt.plot(d.ordtime, d['he'])
    # plt.plot(d.ordtime, d['hn'])
    # plt.plot(d.ordtime, d['ht'])
    # plt.show()

    # from pandas.tools.plotting import autocorrelation_plot
    # # autocorrelation_plot(q.mag)
    # print("Autocorrelating plottingses")
    # autocorrelation_plot(d.hp)
    # plt.show()


if __name__ == '__main__':
    main()