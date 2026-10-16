import pytest

from geo import bearing, destination, distance_km, format_dms, validate, waypoints


def test_distance_london_paris():
    assert round(distance_km(51.5074, -0.1278, 48.8566, 2.3522)) == 344


def test_bearing_north():
    assert round(bearing(0, 0, 10, 0)) == 0


def test_destination_due_east_on_equator():
    lat, lon = destination(0, 0, 90, 111.195)
    assert round(lat, 3) == 0 and round(lon, 2) == 1.0


def test_format_dms():
    assert format_dms(-0.1278, "lon") == "0°7'40.1\"W"


def test_format_dms_rejects_axis():
    with pytest.raises(ValueError):
        format_dms(1.0, "alt")


def test_validate_rejects_bad_latitude():
    with pytest.raises(ValueError):
        validate(91, 0)


def test_waypoints_count_and_spacing():
    points = list(waypoints(0, 0, 0, 10, 4))
    assert len(points) == 5
    assert [round(lon, 6) for _, lon in points] == [2, 4, 6, 8]
