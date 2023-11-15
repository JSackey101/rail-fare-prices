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

        Sets up the attributes:
        - name - The name of the station. -> String
        - region - The region the station resides in. -> String
        - crs - The CRS code of the station. -> String
        - lat - The latitude of the station. -> Float
        - lon - The longitude of the station. -> Float
        - hub - Whether the station is a hub station or not. -> Boolean

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
            (np.power((np.sin(np.radians((lat2 - lat1) / 2))), 2)) + (
                    np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.power(
                (np.sin(np.radians((lon2 - lon1) / 2))), 2))))
        return distance


class RailNetwork:
    """
    A class to represent a rail network.
    """

    def __init__(self, list_of_stations):
        """
        Constructor method that defines all the necessary attributes for rail network objects created from this class.

        Sets up the attributes:
        - list_of_stations - A list of station objects taken as a parameter during object creation
        - stations - A dictionary composing of CRS codes as keys and corresponding Station objects as values.
        """
        self.list_of_stations = list_of_stations
        # Goes through the stations in the list of stations given as a parameter, checks their CRS codes against the
        # ones that have been recorded already, raises an error if the CRS code has been recorded already and records
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
        the rail network object that are also part of the given region instead. By default, this parameter is "None".
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
        """
        Method that takes 2 CRS codes as parameters, being a CRS code for the station the journey starts from and a
        CRS code for the station the journey end at and returns a list of stations that would be travelled to for the
        journey.
        """
        if not any(start == crs for crs, station in self.stations.items()):  # Checks whether the CRS code given in
            # the start parameter matches the CRS code of any of the station objects in the network
            raise ValueError("The CRS code provided for the starting station does not match the CRS code of any "
                             "station within the network")
        elif not any(dest == crs for crs, station in self.stations.items()):  # Checks whether the CRS code given in
            # the dest parameter matches the CRS code of any of the station objects in the network
            raise ValueError("The CRS code provided for the destination station does not match the CRS code of any "
                             "station within the network")
        else:  # Works if both CRS codes match those of station objects found in the network
            for crs, station in self.stations.items():  # Goes through each key, value pair in the stations dictionary
                if start == crs:  # Checks whether the current CRS code matches the one given in the start parameter
                    start_station = station  # Sets a new start variable to the station object
                if dest == crs:  # Checks whether the current CRS code matches the one given in the start parameter
                    dest_station = station  # Sets a new destination variable to the station object
            # Returns a list containing the start and destination station indicating a 1 leg journey if either the
            # regions of both station variables are the same or both station variables are hub stations
            if start_station.region == dest_station.region or start_station.hub and dest_station.hub:
                return [start_station, dest_station]
            else:
                # Uses the closest_hub method to determine the closest hub stations to both the start and the dest
                # station objects
                closest_hub_to_start = self.closest_hub(start_station)
                closest_hub_to_dest = self.closest_hub(dest_station)
                # Checks whether both station objects are not hub stations and returns a list containing the start
                # station, the closest hub station to the start station, the closest hub station to the destination
                # station and the destination station if this is the case
                if not start_station.hub and not dest_station.hub:
                    return [start_station, closest_hub_to_start, closest_hub_to_dest, dest_station]
                # Checks whether only the destination station is not a hub station and returns a list containing the
                # start station. the closest hub station to the destination station and the destination station if
                # this is the case
                elif start_station.hub and not dest_station.hub:
                    return [start_station, closest_hub_to_dest, dest_station]
                # Checks whether only the starting station is not a hub station and returns a list containing the
                # start station, the closest hub station to the start station and the destination station if this is
                # the case
                elif not start_station.hub and dest_station.hub:
                    return [start_station, closest_hub_to_start, dest_station]

    def journey_fare(self, start, dest, summary=False):
        """
        Method that takes 2 CRS codes as parameters, being a CRS code for the station the journey starts from and a
        CRS code for the station the journey ends at and returns a calculated fare price for a journey between the
        two stations.

        Optionally takes summary as a parameter which prints a summary of the journey and its fare price if it is True.
        This is by default False.
        """
        journey_route = self.journey_planner(start, dest)
        fare = 0
        summary_line_one = "Journey from {0} ({1}) to {2} ({3})".format(journey_route[0].name, journey_route[0].crs,
                                                                        journey_route[-1].name, journey_route[-1].crs)
        if len(journey_route) == 2:
            summary_line_two = summary_line_two = "Route: {0} -> {1}".format(journey_route[0].crs, journey_route[1].crs)
        elif len(journey_route) == 3:
            summary_line_two = summary_line_two = "Route: {0} -> {1} ({2}) -> {3}".format(journey_route[0].crs,
                                                                                          journey_route[1].crs,
                                                                                          journey_route[1].name,
                                                                                          journey_route[2].crs)
        elif len(journey_route) == 4:
            summary_line_two = summary_line_two = "Route: {0} -> {1} ({2}) -> {3} ({4}) -> {5}".format(
                journey_route[0].crs,
                journey_route[1].crs,
                journey_route[1].name,
                journey_route[2].crs, journey_route[2].name, journey_route[3].crs)

        for index in range(len(journey_route) - 1):
            start_station = journey_route[index]
            if index == 0:
                summary_line_two.format(start_station.crs)
            dest_station = journey_route[index + 1]
            if start_station.region != dest_station.region:
                diff_regions = 1
            else:
                diff_regions = 0
            distance = float(start_station.distance_to(dest_station))
            regional_hubs_in_dest = int(len(self.hub_stations(dest_station.region)))
            fare += fare_price(distance, diff_regions, regional_hubs_in_dest)
        if summary:
            print(summary_line_one + "\n" + summary_line_two + "\n" + "Fare: \u00a3{}".format(round(fare, 2)) + "\n")
        return fare

    def plot_fares_to(self, crs_code, save=False, bins=10, colour="red", edge_colour="none", line_width=1):
        """
        Method that takes a station's CRS code as a parameter, generates a list of fare prices of journeys from all
        other stations in the network (excluding the station of the given CRS code) to the station of the given CRS
        code and produces a histogram plot from this data which is displayed to the user.

        Optionally takes:
        - A save parameter which will save the histogram plot produced to a .png file instead of
        displaying it to the user. This is by default False.
        - A bins parameter which will determine the number of bins the histogram has. This is by default 10.
        - A colour parameter which will determine the colour of the histogram. This is by default red.
        - A edge_colour parameter which determines the colour of edges of bars in the histogram.
        This is by default "none" meaning the edges are not a different colour to the histogram.
        - A line_width parameter which determines the width of the edge of the bars in the histogram.
        This is by default 1.
        """
        network = self.list_of_stations
        fares = []
        for station in network:
            if station.crs == crs_code:
                input_station = station
                continue
            try:
                journey_cost = self.journey_fare(station.crs, crs_code)
                fares.append(journey_cost)
            except ValueError:
                continue
        if save:
            plt.figure()
            plt.hist(fares, bins, color=colour, ec=edge_colour, lw=line_width)
            plt.xlabel("Fare price (\u00a3)")
            plt.title("Fare Prices to {}".format(input_station.name.replace(" ", "_")))
            plt.savefig("Fare_prices_to_{}".format(input_station.name.replace(" ", "_")))
            print("\nFigure has been saved.")
        else:
            plt.figure()
            plt.hist(fares, bins, color=colour, ec=edge_colour, lw=line_width)
            plt.xlabel("Fare price (\u00a3)")
            plt.title("Fare Prices to {}".format(input_station.name.replace(" ", "_")))
            plt.show()

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
