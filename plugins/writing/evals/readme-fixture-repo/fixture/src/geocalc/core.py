import math

EARTH_RADIUS_KM = 6371.0088


def _check(lat, lon):
    if not -90 <= lat <= 90:
        raise ValueError(f"latitude out of range: {lat}")
    if not -180 <= lon <= 180:
        raise ValueError(f"longitude out of range: {lon}")


def distance_km(lat1, lon1, lat2, lon2):
    _check(lat1, lon1)
    _check(lat2, lon2)
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def bearing(lat1, lon1, lat2, lon2):
    _check(lat1, lon1)
    _check(lat2, lon2)
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    x = math.sin(dl) * math.cos(p2)
    y = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return (math.degrees(math.atan2(x, y)) + 360) % 360


def midpoint(lat1, lon1, lat2, lon2):
    _check(lat1, lon1)
    _check(lat2, lon2)
    p1, p2 = math.radians(lat1), math.radians(lat2)
    l1 = math.radians(lon1)
    dl = math.radians(lon2 - lon1)
    bx = math.cos(p2) * math.cos(dl)
    by = math.cos(p2) * math.sin(dl)
    lat = math.atan2(math.sin(p1) + math.sin(p2), math.sqrt((math.cos(p1) + bx) ** 2 + by**2))
    lon = l1 + math.atan2(by, math.cos(p1) + bx)
    return math.degrees(lat), (math.degrees(lon) + 540) % 360 - 180
