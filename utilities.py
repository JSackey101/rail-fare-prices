import csv
from railway import RailNetwork, Station

def read_rail_network(filepath):
    with open(filepath, "r", newline="") as uk_stations:
        uk_stations_csv = csv.reader(uk_stations)
        stations_data = [row for row in uk_stations_csv]
        header_info = stations_data[0]
        stations_data.remove(header_info)
        list_of_stations = []
        for row in stations_data:
            station = Station(row[header_info.index("name")], row[header_info.index("region")], row[header_info.index("crs")], float(row[header_info.index("latitude")]), float(row[header_info.index("longitude")]), bool(row[header_info.index("hub")]))
            list_of_stations.append(station)
        railnetwork = RailNetwork(list_of_stations)
    uk_stations.close()
    return railnetwork




