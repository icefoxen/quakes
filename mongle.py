#!/usr/bin/env python3
# centennial_Y2K.csv is a slightly-cleaned-up-in-Excel CSV version
# of the https://earthquake.usgs.gov/data/centennial/ catalog file,
# which is in fixed-width FORTRAN-style format.

import calendar
import datetime
import os
import logging
import pandas as pd
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

def index_by_dates(ds):
    """
    Takes a DataFrame with an ordtime column containing Python datetime objects,
    and returns a DataFrame indexed by those datetime's as a pandas.DatetimeIndex.
    """
    # set_index() makes a different column the index.
    # It also makes a copy by default.
    # But copying even the large magnetometer dataset doesn't seem to take long, so.
    ds2 = ds.set_index(['ordtime'])
    ds2.index = pd.DatetimeIndex(data=ds['ordtime'])
    return ds2

def read_magnetometer():
    goes = 6
    year = 1986
    month = 1
    start_day = 1
    end_day = 31

    format_str = 'g{goes:02}_magneto_1m_{year:04}{month:02}{start_day:02}_{year:04}{month:02}{end_day:02}.csv'
    
    logging.info("Collecting files")
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
        logging.info("Reading file %s", f)
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
    full_dataset = pd.concat(dat, ignore_index=True)
    # -99999.0 is used as an "invalid" reading
    print("Cleaning data")
    clean_dataset = full_dataset[full_dataset.hp != -99999.0]
    clean_dataset = clean_dataset[clean_dataset.he != -99999.0]
    clean_dataset = clean_dataset[clean_dataset.hn != -99999.0]
    clean_dataset = clean_dataset[clean_dataset.ht != -99999.0]

    # Now we parse and add an ordinal time column
    # The GOES time columns are like this: 2006-04-02 12:01:00.000
    def make_date(row):
        return datetime.datetime.strptime(row.time_tag, '%Y-%m-%d %H:%M:%S.000')

    logging.info("Translating dates")
    dates = clean_dataset.apply(make_date, axis=1)
    clean_dataset = clean_dataset.assign(ordtime=dates)

    logging.info("Reindexing...")
    return index_by_dates(clean_dataset)

def read_quakes():
    logging.info("Reading quakes file")
    quakes = pd.read_csv('centennial_Y2K.csv')
    # We just skip past any earthquakes before 1986
    recent_quakes = quakes[quakes.yr > 1985]

    # Now we add an absolute ordinal time column, so we can compare
    # apples to apples easily.
    def make_date(row):
        return datetime.datetime(row.yr, row.mon, row.day, row.hr, row['min'], int(row.sec))
        # print(x)
    # ord_date = date.timestamp()
    logging.info("Translating dates")
    dates = recent_quakes.apply(make_date, axis=1)
    recent_quakes = recent_quakes.assign(ordtime=dates)

    logging.info("Reindexing...")
    return index_by_dates(recent_quakes)

def read_cached(reader, cachename):
    if os.path.isfile(cachename):
        logging.info("Reading cached file %s", cachename)
        return pd.read_csv(cachename, parse_dates=[0], index_col=0)
    else:
        logging.info("No cached file found")
        d = reader()
        logging.info("Saving cache to %s", cachename)
        d.to_csv(cachename)
        return d


def extract_important_quake_columns(q):
    # ind = q['ordtime']
    data = q['mag']
    # Ok, index doesn't work the way I want it to here, apparently...
    return pd.DataFrame(data=data, index=q.index)
    # set_index() makes a different column the index.
    # It also makes a copy by default.
    # But copying even the large magnetometer dataset doesn't seem to take long, so.
    # return q.set_index(['ordtime'])

def extract_important_mag_columns(m):
    # ind = m['ordtime']
    data = {
        'hp': m['hp'],
        'he': m['he'],
        'hn': m['hn'],
        'ht': m['ht'],
    }
    return pd.DataFrame(data=data, index=m.index)
    # return m.set_index(['ordtime'])

def fully_process_data():

    q = read_cached(read_quakes, 'quake.cache')
    m = read_cached(read_magnetometer, 'mag.cache')
    logging.info("Extracting only the data we care about")
    q = extract_important_quake_columns(q)
    m = extract_important_mag_columns(m)

    # Resample everything to hourly.
    logging.info("Resampling and joining data")
    q_resampled = q.resample('H').mean().bfill(0)
    m_resampled = m.resample('H').mean().bfill(0)
    # Ditch the old values 'cause we don't need them anymore.
    q = q_resampled
    m = m_resampled
    # return (q,m)

    # Now we chop off the start and end bits of the data so they both
    # line up perfectly.  Which is more annoying than it should be for
    # some reason because pandas is just NOT properly indexing by 
    # datetime, no matter WHAT the docs say should be happening.
    # Bah.
    data_start = max(q.index[0], m.index[0])
    data_end = min(q.index[-1], m.index[-1])
    q_index_start = q.index.get_loc(data_start)
    q_index_end = q.index.get_loc(data_end)
    m_index_start = m.index.get_loc(data_start)
    m_index_end = m.index.get_loc(data_end)

    q_sliced = q[q_index_start:q_index_end]
    m_sliced = m[m_index_start:m_index_end]

    # Now we can finally join the two dataframes together
    alldata = m_sliced.join(q_sliced)
    return alldata

def correlation_results(alldata):
    print("CORRELATION MATRICES")
    print("Pearson")
    print(alldata.corr('pearson'))
    print("Kendall")
    print(alldata.corr('kendall'))
    print("Spearman")
    print(alldata.corr('spearman'))

    alldata_daily = alldata.resample('D').mean().bfill(0)
    print("DAILY CORRELATIONS")
    print("Pearson")
    print(alldata_daily.corr('pearson'))
    print("Kendall")
    print(alldata_daily.corr('kendall'))
    print("Spearman")
    print(alldata_daily.corr('spearman'))

    alldata_weekly = alldata.resample('W').mean().bfill(0)
    print("WEEKLY CORRELATIONS")
    print("Pearson")
    print(alldata_weekly.corr('pearson'))
    print("Kendall")
    print(alldata_weekly.corr('kendall'))
    print("Spearman")
    print(alldata_weekly.corr('spearman'))


def plot_data(alldata):
    print("Plotting quakes")
    alldata.mag.plot()
    plt.title("Earthquake magnitude")
    plt.show()


    print("Plotting mag stuffs")
    magdata = alldata.filter(['he', 'hn', 'hp', 'ht'])
    magdata.plot()
    plt.title("Magnetometer intensity")
    plt.show()

    print("Making scatter plots")
    plt.title("Earthquakes vs. total magnetic field")
    plt.scatter(alldata.mag, alldata.ht)
    plt.xlabel("Earthquake magnitude")
    plt.ylabel("nT")
    plt.show()

    plt.title("Earthquakes vs. he")
    plt.scatter(alldata.mag, alldata.he)
    plt.xlabel("Earthquake magnitude")
    plt.ylabel("nT")
    plt.show()


    plt.title("Earthquakes vs. hn")
    plt.scatter(alldata.mag, alldata.hn)
    plt.xlabel("Earthquake magnitude")
    plt.ylabel("nT")
    plt.show()


    plt.title("Earthquakes vs. hp")
    plt.scatter(alldata.mag, alldata.hp)
    plt.xlabel("Earthquake magnitude")
    plt.ylabel("nT")
    plt.show()

def main():
    alldata = fully_process_data()
    correlation_results(alldata)
    plot_data(alldata)

if __name__ == '__main__':
    main()