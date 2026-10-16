import math

EARTH_RADIUS_KM = 6371.0088


def _helper(degrees):
    return math.radians(degrees)


def validate(lat, lon):
    if not -90 <= lat <= 90:
        raise ValueError(f"latitude out of range: {lat}")
    if not -180 <= lon <= 180:
        raise ValueError(f"longitude out of range: {lon}")


def distance_km(lat1, lon1, lat2, lon2):
    p1, p2 = _helper(lat1), _helper(lat2)
    dp = p2 - p1
    dl = _helper(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def bearing(lat1, lon1, lat2, lon2):
    p1, p2 = _helper(lat1), _helper(lat2)
    dl = _helper(lon2 - lon1)
    x = math.sin(dl) * math.cos(p2)
    y = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return (math.degrees(math.atan2(x, y)) + 360) % 360


def destination(lat, lon, bearing_deg, distance):
    p1 = _helper(lat)
    l1 = _helper(lon)
    b = _helper(bearing_deg)
    d = distance / EARTH_RADIUS_KM
    p2 = math.asin(math.sin(p1) * math.cos(d) + math.cos(p1) * math.sin(d) * math.cos(b))
    l2 = l1 + math.atan2(math.sin(b) * math.sin(d) * math.cos(p1), math.cos(d) - math.sin(p1) * math.sin(p2))
    return math.degrees(p2), (math.degrees(l2) + 540) % 360 - 180


def format_dms(value, axis):
    if axis == "lat":
        hemisphere = "N" if value >= 0 else "S"
    elif axis == "lon":
        hemisphere = "E" if value >= 0 else "W"
    else:
        raise ValueError(f"axis must be 'lat' or 'lon', got {axis!r}")
    total = abs(value) * 3600
    degrees, rem = divmod(total, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{int(degrees)}°{int(minutes)}'{seconds:.1f}\"{hemisphere}"


def waypoints(lat1, lon1, lat2, lon2, count):
    for i in range(1, count + 1):
        f = i / (count + 1)
        yield lat1 + (lat2 - lat1) * f, lon1 + (lon2 - lon1) * f
