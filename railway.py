import matplotlib.pyplot as plt
import numpy as np


def fare_price(distance, different_regions, hubs_in_dest_region):
    """
    A function to compute the fare price using the below inputs and return the result

    :param distance: Distance between the two stations
    :param different_regions: This is 1 if the stations belong to different regions and 0 otherwise
    :param hubs_in_dest_region: Number of hub stations in the same region as the destination station
    :return: Returns the fare price
    """
    fareprice = 1 + distance * np.exp((-1 * distance) / 100) * (1 + (different_regions * hubs_in_dest_region) / 10)
    return fareprice


class Station:
    def __init__(self, name: str, region: str, crs: str, lat: float, lon: float, hub: bool):
        self.name = name
        self.region = region
        self.crs = crs
        if type(name) != str or type(region) != str or type(crs) != str:
            raise TypeError("The Station's name, region and CRS code should all be strings.")
        if len(crs) > 3 or len(crs) < 3 or crs.isupper() is False:
            raise ValueError("The Station's CRS code should be a 3-character string that only has UPPERCASE letters")
        self.lat = lat
        self.lon = lon
        if type(lat) != float or type(lon) != float:
            raise TypeError("The latitude and longitude of the Station should both be decimal numbers in degrees ("
                            "should be a float value).")
        if lat < -90.0 or lat > 90.0:
            raise ValueError("The latitude of the Station should be between -90.0 degrees and 90.0 degrees")
        if lon < -180.0 or lon > 180.0:
            raise ValueError("The longitude of the Station should be between -180.0 degrees and 180.0 degrees")
        self.hub = hub
        if type(hub) != bool:
            raise TypeError("Whether the Station is a Hub Station should either be Boolean True or False.")

    def __repr__(self):
        if self.hub:
            return "Station(" + self.crs + "-" + self.name + "/" + self.region + "-hub)"
        if not self.hub:
            return "Station(" + self.crs + "-" + self.name + "/" + self.region + ")"

    def __str__(self):
        if self.hub:
            return "Station(" + self.crs + "-" + self.name + "/" + self.region + "-hub)"
        if not self.hub:
            return "Station(" + self.crs + "-" + self.name + "/" + self.region + ")"

    def distance_to(self, other_station):
        r = 6371
        lat1 = self.lat
        lat2 = other_station.lat
        lon1 = self.lon
        lon2 = other_station.lon
        distance = 2*r*np.arcsin(np.sqrt((np.power((np.sin((lat2-lat1)/2)),2)) + np.cos(lat1) * np.cos(lat2) * np.power((np.sin((lon2 - lon1) / 2)), 2)))
        return distance



class RailNetwork:
    def __init__(self, list_of_stations):
        self.list_of_stations = list_of_stations
        CRS = []
        for station in list_of_stations:
            if station.crs in CRS:
                raise ValueError("The CRS code {} is used for more than 1 station. All Stations used to form a "
                                 "RailNetwork must have unique CRS codes.".format(station.crs))
            CRS.append(station.crs)
        self.stations = {}
        for station in list_of_stations:
            print(station)
            self.stations.update({station.crs: station})

    def regions(self):
        unique_regions = []
        for crs, station in self.stations.items():
            unique_regions.append(station.region)
        return np.unique(unique_regions)


    def n_stations(self):
        raise NotImplementedError

    def hub_stations(self, region):
        raise NotImplementedError

    def closest_hub(self, s):
        raise NotImplementedError

    def journey_planner(self, start, dest):
        raise NotImplementedError

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
