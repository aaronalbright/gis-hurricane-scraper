import feedparser
import requests
import time
import pysftp
from keys import HOST, PASSWORD, USERNAME, DEST

# downlaods shapefile to SFTP server
def download_shapefile(file_contents):
    host = HOST
    password = PASSWORD
    username = USERNAME

    ssh = pysftp.Connection(host=host, username=username,
    password=password)

    with ssh.cd(DEST):
        f = ssh.open('shp.zip','w')
        f.write(file_contents)
        f.close()

    ssh.close()

# parses NOAA gis rss feed
url = 'http://www.nhc.noaa.gov/gis-at.xml'
last_feed = feedparser.parse(url)

# finds first shapefile
for i in last_feed.entries:
    if 'gis-forecast-shp' in i.id:
        print "Found GIS shapefile"
        print "-------------------"
        last_id = i.id         # <guid> of shapefile item
        link = i.link     # <link> of shapefile item
        r = requests.get(link)
        requested_file = r.content
        download_shapefile(requested_file)
        print "Download successful"
        print "-------------------"


# checks every five minutes if the rss feed has been updated
while True:
    # parses new feed with the last feeds modified date injected. A 304 status means the feed has not been modified
    new_feed = feedparser.parse(url, modified=last_feed.modified)
    if new_feed.status == 304:
        print "Feed not modified..."
        print "Last modified: %s" % last_feed.modified
        print "---------------------------------------"
    else:
        print "Feed updated"
        print new_feed.status
        print "New_Feed Modified: %s" % new_feed.modified
        last_feed = new_feed
        print "last_feed = new_feed modified: %s" % last_feed.modified
        # gets another shapefile
        for i in new_feed.entries:
            if 'gis-forecast-shp' in i.id:
                new_id = i.id
                # checks if the shapefile has been updated. the RSS feed may update more often than the shapefile
                if new_id != last_id:
                    print "New GIS shapefile found"
                    link = i.link
                    r = requests.get(link)
                    requested_file = r.content
                    download_shapefile(requested_file)
                    print "Download successful"
                    last_id = new_id
                else:
                    print "No new shapefile"
                    print "----------------"

    time.sleep(300)
