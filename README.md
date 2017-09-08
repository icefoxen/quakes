# Abstract

A small project to process data from the USGS centennial quake catalog
and solar weather data from the GOES series of satellites, to see if there's any correlation between them.

Inspired by silly conspiricy posts: https://www.reddit.com/r/conspiracy/comments/6yhv3l/the_ultimate_earthquake_test_is_about_to_commence/  Really I just said "well I have the data and know what to do with it, I might as well."

# Data sources

 * https://earthquake.usgs.gov/data/centennial/ (included)
 * https://www.ngdc.noaa.gov/stp/satellite/goes/dataaccess.html (`download-goes-data.fish` is a slightly-flaky script to fetch
   the necessary data; requires wget and the [fish](https://fishshell.com/) shell.)

The data span investigated is 1986-2008; this was chosen basically because I wanted some nice long single runs of GOES data
from the same satellites, and this is where the data was available.  You could push it back further if you wanted, probably,
but the importing becomes more work.

Note that the GOES data used comes from three separate satellites, and the Centennial quake catalogue is an ensemble of *large* earthquakes collected from all sorts of different sources.  Another reason to start in the 1980's or thereabouts is you know you're going to be using relatively modern seismometers; I personally wouldn't put too much faith in records before the late 60's or so unless I knew a lot more about where they came from.

There ARE some gaps in the GOES data, one of them large from 1991-1994 or something; filling those in someday would be nice.  Should be easy to extend though; just find which satellites were active and add their data into the thing.

![](https://raw.githubusercontent.com/icefoxen/quakes/master/figures/quakes.png)

![](https://raw.githubusercontent.com/icefoxen/quakes/master/figures/magnetometer.png)

# Methods

There's a python script called `mongle.py` to aggregate and process the data, and perform some correlation analysis on it.  It requires python3, numpy, pandas, and matplotlib.

It just very simply and crudely sucks in both data sources, removes the columns we don't care about (everything except magnetometer data and earthquake magnitude) resamples them to hourly resolution, then chops any tailing ends off of both sides so they line up to exactly the same time window.  This process is not great; I don't entirely trust the resampling, mainly, since we're basically smearing discrete events (earthquakes) out into continuous ones.  But, with an hourly resolution and usually several large-ish earthquakes a day, it seems okay.

The analysis itself is just a very simple correlation test, using Pearson, Kendall and Spearman algorithms.  Since the hypothesis is basically that magnetic field and earthquake intensity are related, this should probably be sufficient to show SOME connection if there is one.

I resampled the data and ran the same correlation tests on daily and weekly timeframes, in the hopes that if there's a lag between one event and another it would result in more significance.  IE, if a solar storm on one day causes an earthquake on the next day, then the hourly and daily correlations would not really be significant but the weekly one would likely be higher.  This is pretty stupid and a rolling time window of different sizes would be better.


# Results

Correlation matrices follow.  `he`, `hn`, and `hp` are the magnetic field strengths in three orthogonal directions (east, north, perpendicular to earth's surface) and `ht` is the total field strength.  `mag` is the earthquake magnitude.

```
HOURLY
Pearson
           he        hn        hp        ht       mag
he   1.000000 -0.393394 -0.006958  0.369666  0.056965
hn  -0.393394  1.000000  0.102158 -0.060886 -0.002616
hp  -0.006958  0.102158  1.000000  0.885626  0.024659
ht   0.369666 -0.060886  0.885626  1.000000  0.043586
mag  0.056965 -0.002616  0.024659  0.043586  1.000000
Kendall
           he        hn        hp        ht       mag
he   1.000000 -0.324450  0.028368  0.215625  0.049476
hn  -0.324450  1.000000  0.070566 -0.030686 -0.008495
hp   0.028368  0.070566  1.000000  0.800358  0.021222
ht   0.215625 -0.030686  0.800358  1.000000  0.030717
mag  0.049476 -0.008495  0.021222  0.030717  1.000000
Spearman
           he        hn        hp        ht       mag
he   1.000000 -0.457651  0.068974  0.328915  0.071068
hn  -0.457651  1.000000  0.099440 -0.056915 -0.012322
hp   0.068974  0.099440  1.000000  0.910295  0.030428
ht   0.328915 -0.056915  0.910295  1.000000  0.044038
mag  0.071068 -0.012322  0.030428  0.044038  1.000000

DAILY
Pearson
           he        hn        hp        ht       mag
he   1.000000 -0.407790  0.391497  0.678303  0.074572
hn  -0.407790  1.000000 -0.017532 -0.172377 -0.003053
hp   0.391497 -0.017532  1.000000  0.913490  0.040433
ht   0.678303 -0.172377  0.913490  1.000000  0.060704
mag  0.074572 -0.003053  0.040433  0.060704  1.000000
Kendall
           he        hn        hp        ht       mag
he   1.000000 -0.391922  0.231978  0.501813  0.058045
hn  -0.391922  1.000000 -0.046217 -0.220322 -0.023920
hp   0.231978 -0.046217  1.000000  0.698331  0.023598
ht   0.501813 -0.220322  0.698331  1.000000  0.035158
mag  0.058045 -0.023920  0.023598  0.035158  1.000000
Spearman
           he        hn        hp        ht       mag
he   1.000000 -0.560003  0.345795  0.682911  0.085208
hn  -0.560003  1.000000 -0.099994 -0.359595 -0.035344
hp   0.345795 -0.099994  1.000000  0.851384  0.034671
ht   0.682911 -0.359595  0.851384  1.000000  0.051555
mag  0.085208 -0.035344  0.034671  0.051555  1.000000


WEEKLY
Pearson
           he        hn        hp        ht       mag
he   1.000000 -0.422462  0.520733  0.738327  0.116704
hn  -0.422462  1.000000 -0.047880 -0.194282 -0.003141
hp   0.520733 -0.047880  1.000000  0.944310  0.072319
ht   0.738327 -0.194282  0.944310  1.000000  0.100138
mag  0.116704 -0.003141  0.072319  0.100138  1.000000
Kendall
           he        hn        hp        ht       mag
he   1.000000 -0.453187  0.363682  0.622975  0.087348
hn  -0.453187  1.000000 -0.156163 -0.336612 -0.036928
hp   0.363682 -0.156163  1.000000  0.703276  0.041332
ht   0.622975 -0.336612  0.703276  1.000000  0.061458
mag  0.087348 -0.036928  0.041332  0.061458  1.000000
Spearman
           he        hn        hp        ht       mag
he   1.000000 -0.625116  0.520664  0.798413  0.130210
hn  -0.625116  1.000000 -0.258583 -0.502389 -0.056131
hp   0.520664 -0.258583  1.000000  0.864214  0.062272
ht   0.798413 -0.502389  0.864214  1.000000  0.091716
mag  0.130210 -0.056131  0.062272  0.091716  1.000000
```


![](https://raw.githubusercontent.com/icefoxen/quakes/master/figures/mag-vs-he.png)

![](https://raw.githubusercontent.com/icefoxen/quakes/master/figures/mag-vs-hn.png)

![](https://raw.githubusercontent.com/icefoxen/quakes/master/figures/mag-vs-hp.png)

![](https://raw.githubusercontent.com/icefoxen/quakes/master/figures/mag-vs-ht.png)

# Discussion

We have some sanity check that it's working the way we think it is since the magnetic field strengths are all fairly well correlated with each other.  Meanwhile the earthquake magnitude has a maximum Pearson correlation of 0.116 with `he` in the weekly interpolation setup, which is more than I expected but still basically nothing.  So, to the surprise of probably not many people, there's no significant correlation between magnetic field strength and earthquake magnitude in the time period studied.

# Further work

The resampling is crude, as said, and more sophisticated imputation of data would be interesting and maybe useful.

More advanced statistical tests would probably be good, if anyone knows any that are applicable.

It would be nice to investigate potential time offsets more, either by scanning across a variety of time windows/offsets and looking for changes, or possibly finding some more clever technique.  Signal processing methods may be applicable here.

It would be interesting to apply a Kalman filter or some other machine-learning-y regression method to this data, which may be able to learn more sophisticated relationships.

Submit other ideas as issues.