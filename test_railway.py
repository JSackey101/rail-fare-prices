import pytest
from railway import fare_price, Station, RailNetwork
import numpy as np


# TODO Add test to ensure that CRS codes loaded into RailNetwork are unique
@pytest.mark.parametrize("name, region, crs, lat, lon, hub",
                         [("Brighton", "South East", "Btn", 50.829659, -0.141234, True),
                          ("Brighton", "South East", "BTNN", 50.829659, -0.141234, True),
                          ("Brighton", "South East", "BT", 50.829659, -0.141234, True),
                          ("Brighton", "South East", "BTN", 91.0, -0.141234, True),
                          ("Brighton", "South East", "BTN", -91.0, -0.141234, True),
                          ("Brighton", "South East", "BTN", 50.829659, 181.0, True),
                          ("Brighton", "South East", "BTN", 50.829659, -181.0, True)])
def test_value_error_station(name, region, crs, lat, lon, hub):
    with pytest.raises(ValueError):
        Station(name, region, crs, lat, lon, hub)


def test_fare_price():
    distance = 100
    different_regions = 1
    hubs_in_dest_region = 3
    result = fare_price(distance, different_regions, hubs_in_dest_region)
    expected = 1 + distance * np.exp((-1 * distance) / 100) * (1 + (different_regions * hubs_in_dest_region) / 10)
    assert result == expected


@pytest.mark.parametrize("name, region, crs, lat, lon, hub",
                         [(6, "South East", "BTN", 50.829659, -0.141234, True),
                          ("Brighton", 6, "BTN", 50.829659, -0.141234, True),
                          ("Brighton", "South East", 6, 50.829659, -0.141234, True),
                          ("Brighton", "South East", "BTN", "50.829659", -0.141234, True),
                          ("Brighton", "South East", "BTN", 50.829659, "-0.141234", True),
                          ("Brighton", "South East", "BTN", 50.829659, -0.141234, "True")])
def test_type_error_station(name, region, crs, lat, lon, hub):
    with pytest.raises(TypeError):
        Station(name, region, crs, lat, lon, hub)


def test_correct_station_input():
    brighton = Station("Brighton", "South East", "BTN", 50.829659, -0.141234, True)
    result = [brighton.name, brighton.region, brighton.crs, brighton.lat, brighton.lon, brighton.hub]
    expected = ["Brighton", "South East", "BTN", 50.829659, -0.141234, True]
    assert result == expected


def test_crs_codes():
    brighton = Station("Brighton", "South East", "BTN", 50.829659, -0.141234, True)
    kings_cross = Station("London Kings Cross", "London", "BTN", 51.530827, -0.122907, True)
    edinburgh_park = Station("Edinburgh Park", "Scotland", "EDP", 55.927615, -3.307829, False)
    list_of_stations = [brighton, kings_cross, edinburgh_park]
    with pytest.raises(ValueError):
        RailNetwork(list_of_stations)

