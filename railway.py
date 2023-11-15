import matplotlib.pyplot as plt
import numpy as np


def fare_price(distance, different_regions, hubs_in_dest_region):
    """
    A function to compute the fare price using the distance, different_regions and hubs_in_dest_region parameters
    with the formula given to calculate fare prices in GBP of direct travel between 2 connected stations and return
    the result
    """
    fareprice = 1 + distance * np.exp((-1 * distance) / 100) * (1 + (different_regions * hubs_in_dest_region) / 10)
    return fareprice


class Station:
    """
    A class to represent a station.
    """

    def __init__(self, name: str, region: str, crs: str, lat: float, lon: float, hub: bool):
        """
        Constructor method that defines all the necessary attributes for station objects created from this class.
        """
        self.name = name
        self.region = region
        self.crs = crs
        if type(name) != str or type(region) != str or type(crs) != str:  # Checks whether any of the name,
            # region and crs attributes are of a type other than a string.
            raise TypeError("The Station's name, region and CRS code should all be strings.")
        if len(crs) > 3 or len(crs) < 3 or crs.isupper() is False:  # Checks whether the length of the crs attribute
            # is above or below 3 or whether it is not fully uppercase.
            raise ValueError("The Station's CRS code should be a 3-character string that only has UPPERCASE letters")
        self.lat = lat
        self.lon = lon
        if type(lat) != float or type(lon) != float:  # Checks whether either the latitude or longitude attributes
            # are of a type other than a float.
            raise TypeError("The latitude and longitude of the Station should both be decimal numbers in degrees ("
                            "should be a float value).")
        if lat < -90.0 or lat > 90.0:  # Checks whether the latitude is below -90.0 degrees or above 90.0 degrees
            raise ValueError("The latitude of the Station should be between -90.0 degrees and 90.0 degrees")
        if lon < -180.0 or lon > 180.0:  # Checks whether the longitude is below -180.0 degrees or above 180.0 degrees
            raise ValueError("The longitude of the Station should be between -180.0 degrees and 180.0 degrees")
        self.hub = hub
        if type(hub) != bool:  # Checks whether the hub attribute is of a type other than a boolean.
            raise TypeError("Whether the Station is a Hub Station should either be Boolean True or False.")

    def __repr__(self):
        """
        Method that returns a string when the station objects created from this class are displayed by name.
        """
        if self.hub:  # Checks whether the station is a hub station
            return "Station(" + self.crs + "-" + self.name + "/" + self.region + "-hub)"
        if not self.hub:  # Checks whether the station is not a hub station
            return "Station(" + self.crs + "-" + self.name + "/" + self.region + ")"

    def __str__(self):
        """
        Method that returns a string when print is called on station objects created from this class.
        """
        if self.hub:  # Checks whether the station is a hub station
            return "Station(" + self.crs + "-" + self.name + "/" + self.region + "-hub)"
        if not self.hub:  # Checks whether the station is not a hub station
            return "Station(" + self.crs + "-" + self.name + "/" + self.region + ")"

    def distance_to(self, other_station):
        """
        Method that finds the distance (in km) between a station object created from this class and another station
        object given as a parameter using the Haversine formula.
        """
        r = 6371  # Approximate radius of the Earth in km
        lat1 = self.lat  # Latitude of the station object
        lat2 = other_station.lat  # Latitude of the other_station object given as a parameter
        lon1 = self.lon  # Longitude of the station object
        lon2 = other_station.lon  # Longitude of the other_station object given as a parameter
        distance = 2 * r * np.arcsin(np.sqrt(
            (np.power((np.sin((lat2 - lat1) / 2)), 2)) + np.cos(lat1) * np.cos(lat2) * np.power(
                (np.sin((lon2 - lon1) / 2)), 2)))
        return distance


class RailNetwork:
    """
    A class to represent a rail network.
    """

    def __init__(self, list_of_stations):
        """
        Constructor method that defines all the necessary attributes for rail network objects created from this class.
        """
        self.list_of_stations = list_of_stations
        # Goes through the stations in the list of stations given as a parameter, checks their CRS codes against the
        # ones that have been recorded already, raises an error if the CRS code has been recorded alreay and records
        # the CRS code if not.
        crs = []
        for station in list_of_stations:
            if station.crs in crs:  # Checks whether the CRS code of the current station object is in the crs list
                raise ValueError("The CRS code {} is used for more than 1 station. All Stations used to form a "
                                 "RailNetwork must have unique CRS codes.".format(station.crs))
            crs.append(station.crs)  # Adds the CRS code of the current station to the crs list
        self.stations = {}  # Creates an empty dictionary in a new class variable
        for station in list_of_stations:
            self.stations.update({station.crs: station})  # Updates the dictionary with a new key, value pair with the
            # station's CRS code being the key and the station itself being the value

    def regions(self):
        """
        Method that returns a list of all unique regions within the rail network object.
        """
        unique_regions = []
        for crs, station in self.stations.items():  # Goes through each key, value pair in the stations dictionary
            unique_regions.append(station.region)
        return np.unique(unique_regions)  # Uses numpy to only return the unique station objects in the list

    def n_stations(self):
        """
        Method that returns the number of stations within the rail network object.
        """
        return len(self.stations)

    def hub_stations(self, region=None):
        """
        Method that returns a list of all the hub stations within the rail network object.

        If the optional region parameter is passed, this method would return a list of all the hub stations within
        the rail network object that are also part of the given region instead.
        """
        # Checks whether the region parameter has been passed and whether the region given is not a region for any of
        # the stations within the stations dictionary. Returns an error if these conditions are fulfilled.
        if region is not None and not any(station.region == region for crs, station in self.stations.items()):
            raise ValueError("The given region does not exist in this network.")
        elif region is not None:  # If the above is not fulfilled this checks whether the region parameter has been
            # passed

            hub_stations = []
            for crs, station in self.stations.items():  # Goes through each key, value pair in the stations dictionary
                if station.hub and station.region == region:  # Checks whether the current station object is both a
                    # hub station and is in the given region
                    hub_stations.append(station)
        else:
            hub_stations = []
            for crs, station in self.stations.items():  # Goes through each key, value pair in the stations dictionary
                if station.hub:  # Checks whether the current station object is a hub station
                    hub_stations.append(station)
        return hub_stations

    def closest_hub(self, s):
        """
        Method that takes a station object as a parameter and calculates the nearest hub station that is also within
        the same region as the station object.
        """
        regional_stations = []
        distances = []
        for crs, station in self.stations.items():  # Goes through each key, value pair in the stations dictionary
            # Checks whether the current station has the same region as the station object taken as a parameter,
            # whether the current station is a hub station and whether the CRS code of the current station does not
            # match the CRS code of the station object taken as a parameter
            if station.region == s.region and station.hub and s.crs is not station.crs:
                regional_stations.append(station)
                distances.append(station.distance_to(s))  # Uses the distance_to method of the current station to
                # calculate its distance to the station object taken as a parameter
        if not regional_stations:  # Checks whether the regional_stations list is empty - this indicates that the
            # given station has no hub stations in its region
            raise ValueError("The given station has no hub stations in its region.")
        return regional_stations[distances.index(min(distances))]  # Returns the closest station through using the
        # index of the smallest distance in the distances list to index the regional_stations list

    def journey_planner(self, start, dest):
        if not any(start == crs for crs, station in self.stations.items()):
            raise ValueError("The CRS code provided for the starting station does not match the CRS code of any "
                             "station within the network")
        elif not any(dest == crs for crs, station in self.stations.items()):
            raise ValueError("The CRS code provided for the destination station does not match the CRS code of any "
                             "station within the network")
        else:
            for crs, station in self.stations.items():
                if start == crs:
                    start_station = station
                if dest == crs:
                    dest_station = station
            if start_station.region == dest_station.region or start_station.hub and dest_station.hub:
                return [start_station, dest_station]
            else:
                closest_hub_to_start = self.closest_hub(start_station)
                closest_hub_to_dest = self.closest_hub(dest_station)
                if not start_station.hub and not dest_station.hub:
                    return [start_station, closest_hub_to_start, closest_hub_to_dest, dest_station]
                elif start_station.hub and not dest_station.hub:
                    return [start_station, closest_hub_to_dest, dest_station]
                elif not start_station.hub and dest_station.hub:
                    return [start_station, closest_hub_to_start, dest_station]

    def journey_fare(self, start, dest, summary):
        raise NotImplementedError

    def plot_fares_to(self, crs_code, save, ADDITIONAL_ARGUMENTS):
        raise NotImplementedError

    def plot_network(self, marker_size: int = 5) -> None:
        """
        A function to plot the rail network, for visualisation purposes.
        You can optionally pass a marker size (in pixels) for the plot to use.

        The method will produce a matplotlib figure showing the locations of the stations in the network, and
        attempt to use matplotlib.pyplot.show to display the figure.

        This function will not execute successfully until you have created the regions() function.
        You are NOT required to write tests nor documentation for this function.
        """
        fig, ax = plt.subplots(figsize=(5, 10))
        ax.set_xlabel("Longitude (degrees)")
        ax.set_ylabel("Latitude (degrees)")
        ax.set_title("Railway Network")

        COLOURS = ["b", "r", "g", "c", "m", "y", "k"]
        MARKERS = [".", "o", "x", "*", "+"]

        for i, r in enumerate(self.regions):
            lats = [s.lat for s in self.stations.values() if s.region == r]
            lons = [s.lon for s in self.stations.values() if s.region == r]

            colour = COLOURS[i % len(COLOURS)]
            marker = MARKERS[i % len(MARKERS)]
            ax.scatter(lons, lats, s=marker_size, c=colour, marker=marker, label=r)

        ax.legend()
        plt.tight_layout()
        plt.show()
        return

    def plot_journey(self, start: str, dest: str) -> None:
        """
        Plot the journey between the start and end stations, on top of the rail network map.
        The start and dest inputs should the strings corresponding to the CRS codes of the
        starting and destination stations, respectively.

        The method will overlay the route that your journey_planner method has found on the
        locations of the stations in your network, and draw lines to indicate the route.

        This function will not successfully execute until you have written the journey_planner method.
        You are NOT required to write tests nor documentation for this function.
        """
        # Plot railway network in the background
        network_lats = [s.lat for s in self.stations.values()]
        network_lons = [s.lon for s in self.stations.values()]

        fig, ax = plt.subplots(figsize=(5, 10))
        ax.scatter(network_lons, network_lats, s=1, c="blue", marker="x")
        ax.set_xlabel("Longitude (degrees)")
        ax.set_ylabel("Latitude (degrees)")

        # Compute the journey
        journey = self.journey_planner(start, dest)
        plot_title = f"Journey from {journey[0].name} to {journey[-1].name}"
        ax.set_title(f"Journey from {journey[0].name} to {journey[-1].name}")

        # Draw over the network with the journey
        journey_lats = [s.lat for s in journey]
        journey_lons = [s.lon for s in journey]
        ax.plot(journey_lons, journey_lats, "ro-", markersize=2)

        plt.show()
        return


