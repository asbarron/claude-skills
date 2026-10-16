import pytest

from geocalc import bearing, distance_km, midpoint


def test_distance_london_paris():
    assert round(distance_km(51.5074, -0.1278, 48.8566, 2.3522)) == 344


def test_bearing_north():
    assert round(bearing(0, 0, 10, 0)) == 0


def test_midpoint_equator():
    lat, lon = midpoint(0, 0, 0, 10)
    assert round(lat, 6) == 0 and round(lon, 6) == 5


def test_rejects_bad_latitude():
    with pytest.raises(ValueError):
        distance_km(91, 0, 0, 0)
