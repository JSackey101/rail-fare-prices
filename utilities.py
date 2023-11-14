import csv
from railway import RailNetwork, Station


def read_rail_network(filepath):
    """
    Function that takes a file containing station data with the format of providing a station's: name, crs, region,
    latitude, longitude and whether it is a hub station, reads the data within the file, uses the data to create one
    or more station objects and returns a rail network object created using the station objects created previously.
    """
    with open(filepath, "r", newline="") as uk_stations: # Opens the file the filepath parameter leads to in read
        # mode as a file object in the uk_stations variable and the newline parameter overwrites the newline escape
        # characters from the file
        uk_stations_csv = csv.reader(uk_stations) # Creates a csv reader object from the file object
        stations_data = [row for row in uk_stations_csv]  # Goes through every line in the csv reader object and adds
        # them to a nested list in the stations_data nested list
        header_info = stations_data[0]  # Saves the header list - as this would always be the first row
        stations_data.remove(header_info)  # Removes the header list from the stations_data nested list
        # Goes through each individual list in the stations_data nested list and creates a Station object from each row,
        # using the header_info variable to determine which column contains the right piece of information,
        # and adds each station object to the list_of_stations list.
        list_of_stations = []
        for row in stations_data:
            station = Station(row[header_info.index("name")], row[header_info.index("region")],
                              row[header_info.index("crs")], float(row[header_info.index("latitude")]),
                              float(row[header_info.index("longitude")]), bool(row[header_info.index("hub")]))
            list_of_stations.append(station)
        rail_network = RailNetwork(list_of_stations) # Creates a rail network from the list of station objects
    return rail_network
