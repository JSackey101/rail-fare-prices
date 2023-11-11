import pytest
from railway import fare_price, Station, RailNetwork


@pytest.mark.parametrize("name, region, crs, lat, lon, hub",
                         [(6, "South East", "BTN", 50.829659, -0.141234, True),
                          ("Brighton", 6, "BTN", 50.829659, -0.141234, True),
                          ("Brighton", "South East", 6, 50.829659, -0.141234, True),
                          ("Brighton", "South East", "BTN", "50.829659", -0.141234, True),
                          ("Brighton", "South East", "BTN", 50.829659, "-0.141234", True),
                          ("Brighton", "South East", "BTN", 50.829659, -0.141234, "True")])
def test_type_error(name, region, crs, lat, lon, hub):
    with pytest.raises(TypeError):
        Station(name, region, crs, lat, lon, hub)
