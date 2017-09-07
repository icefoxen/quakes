A small project to process data from the USGS centennial quake catalog
and solar weather data from the GOES series of satellites, to see if there's any correlation between them.

Data sources: 

 * https://earthquake.usgs.gov/data/centennial/ (included)
 * https://www.ngdc.noaa.gov/stp/satellite/goes/dataaccess.html (`download-goes-data.fish` is a slightly-flaky script to fetch
   the necessary data; requires wget and the [fish](https://fishshell.com/) shell.)

The data span investigated is 1986-2008; this was chosen basically because I wanted some nice long single runs of GOES data
from the same satellites, and this is where the data was available.  You could push it back further if you wanted, probably,
but the importing becomes more work.

Note that the GOES data used comes from three separate satellites, and the Centennial quake catalogue is an ensemble of *large* earthquakes collected from all sorts of different sources.  Another reason to start in the 1980's or thereabouts is you know you're going to be using relatively modern seismometers; I personally wouldn't put too much faith in records before the late 60's or so unless I knew a lot more about where they came from.


