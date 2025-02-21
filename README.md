# Rail Fare Prices

## Description

Loads Train Station data for the UK (obtained from ) 

## Information about the data.

Amalgamation of 2 publically available datasets:

1. Obtained from the [https://www.orr.gov.uk](Office of Rail and Road (ORR)) dataset of estimates of station usage between April 2020 and May 2021 with the raw data being found [https://dataportal.orr.gov.uk/media/2148/table-1410-estimates-of-station-usage-2020-21.ods](here) - providing station names, regions and CRS codes.

2. [https://www.github.com/davwheat/uk-railway-stations/tree/main](This GitHub repository) - providing latitude and longitude coordinates.



utilities.py contains the function read_rail_network which loads a dataset containing station data (e.g. in uk_stations.csv) and creates a RailNetwork object containing Station objects for each station.

railway.py contains the code needed to produce both Station objects and RailNetwork objects which can be used alongside the fare_price function to estimate rail fares within a rail network.

Repository contains tests made for the functions I made in both railway.py and utilities.py in test_railway.py.

