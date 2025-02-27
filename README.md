# Rail Fare Prices

## Description

Contains the functionality to load UK train station data and visualise rail networks loaded in, alongside calculating details regarding journeys made within the rail networks (such as what stations would be involved and fare prices) and visualising them.

## Components 

### 1. railway.py

Station class - code needed to produce Station objects
RailNetwork class - code needed to produce RailNetwork objects that contain a list of Station objects
fare_price function - calculates the fare price in £-GBP between 2 stations

### 2. utilities.py

read_rail_network function - oads a dataset containing station data (e.g. in uk_stations.csv) and creates a RailNetwork object from the data.

### 3. test_railway,py

Contains tests for the functions and classes.

## Information about the data.

Amalgamation of 2 publically available datasets:

1. Obtained from the [Office of Rail and Road (ORR)](https://www.orr.gov.uk) dataset of estimates of station usage between April 2020 and May 2021 with the raw data being found [here](https://dataportal.orr.gov.uk/media/2148/table-1410-estimates-of-station-usage-2020-21.ods) - providing station names, regions and CRS codes.

2. [This GitHub repository](https://www.github.com/davwheat/uk-railway-stations/tree/main) - providing latitude and longitude coordinates.



utilities.py contains the function read_rail_network which loads a dataset containing station data (e.g. in uk_stations.csv) and creates a RailNetwork object containing Station objects for each station.

railway.py contains the code needed to produce both Station objects and RailNetwork objects which can be used alongside the fare_price function to estimate rail fares within a rail network.

Repository contains tests made for the functions I made in both railway.py and utilities.py in test_railway.py.

