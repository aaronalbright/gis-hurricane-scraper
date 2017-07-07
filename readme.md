This is a simple python script I wrote to parse the [National Hurricane Center's data feed](http://www.nhc.noaa.gov/gis/) for it's GIS hurricane forecast shapefile.

Then, it downloads the file to an SFTP server for use in my apps.

The current version checks for an updated feed every five minutes. **This is only for testing**. In actual deployment, it would ideally only check every hour or so.

To get up and running, simply fill out the HOST, PASSWORD, USERNAME and DEST fields and you should be good to go.
