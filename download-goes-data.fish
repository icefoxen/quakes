#!/usr/bin/env fish

# Download GOES satellite magnetometer data.
# Data product page: https://www.ngdc.noaa.gov/stp/satellite/goes/dataaccess.html
# The specific dataset is the "new average" CSV files:
# https://satdat.ngdc.noaa.gov/sem/goes/data/full/magnetometer/
# https://www.ngdc.noaa.gov/stp/satellite/goes/index.html also has other misc useful
# info about the satellites and sensors, such as when they are operational.
#
# For now we're just downloading the 1-minute averages, which should be totally fine.


# GOES 6
for year in (seq 1986 1995)
    for month in (seq -w 01 12)
        echo $month
        if [ $month -eq 02 ]
            wget -nc "https://satdat.ngdc.noaa.gov/sem/goes/data/new_avg/"$year"/"$month"/goes06/csv/g06_magneto_1m_"$year""$month"01_"$year""$month"28.csv"
            wget -nc "https://satdat.ngdc.noaa.gov/sem/goes/data/new_avg/"$year"/"$month"/goes06/csv/g06_magneto_1m_"$year""$month"01_"$year""$month"29.csv"
        else
            wget -nc "https://satdat.ngdc.noaa.gov/sem/goes/data/new_avg/"$year"/"$month"/goes06/csv/g06_magneto_1m_"$year""$month"01_"$year""$month"30.csv"
            wget -nc "https://satdat.ngdc.noaa.gov/sem/goes/data/new_avg/"$year"/"$month"/goes06/csv/g06_magneto_1m_"$year""$month"01_"$year""$month"31.csv"
        end
    end
end

# GOES 8
for year in (seq 1995 2008)
    for month in (seq -w 01 12)
        echo $month
        if [ $month -eq 02 ]
            wget -nc "https://satdat.ngdc.noaa.gov/sem/goes/data/new_avg/"$year"/"$month"/goes08/csv/g08_magneto_1m_"$year""$month"01_"$year""$month"28.csv"
            wget -nc "https://satdat.ngdc.noaa.gov/sem/goes/data/new_avg/"$year"/"$month"/goes08/csv/g08_magneto_1m_"$year""$month"01_"$year""$month"29.csv"
        else
            wget -nc "https://satdat.ngdc.noaa.gov/sem/goes/data/new_avg/"$year"/"$month"/goes08/csv/g08_magneto_1m_"$year""$month"01_"$year""$month"30.csv"
            wget -nc "https://satdat.ngdc.noaa.gov/sem/goes/data/new_avg/"$year"/"$month"/goes08/csv/g08_magneto_1m_"$year""$month"01_"$year""$month"31.csv"
        end
    end
end


# GOES 10
for year in (seq 2003 2008)
    for month in (seq -w 01 12)
        echo $month
        if [ $month -eq 02 ]
            wget -nc "https://satdat.ngdc.noaa.gov/sem/goes/data/new_avg/"$year"/"$month"/goes10/csv/g10_magneto_1m_"$year""$month"01_"$year""$month"28.csv"
            wget -nc "https://satdat.ngdc.noaa.gov/sem/goes/data/new_avg/"$year"/"$month"/goes10/csv/g10_magneto_1m_"$year""$month"01_"$year""$month"29.csv"
        else
            wget -nc "https://satdat.ngdc.noaa.gov/sem/goes/data/new_avg/"$year"/"$month"/goes10/csv/g10_magneto_1m_"$year""$month"01_"$year""$month"30.csv"
            wget -nc "https://satdat.ngdc.noaa.gov/sem/goes/data/new_avg/"$year"/"$month"/goes10/csv/g10_magneto_1m_"$year""$month"01_"$year""$month"31.csv"
        end
    end
end
