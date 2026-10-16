import argparse
import sys

from geocalc import __version__, bearing, distance_km, midpoint


def main(argv=None):
    parser = argparse.ArgumentParser(prog="geocalc", description="Great-circle calculations between two coordinates.")
    parser.add_argument("--version", action="version", version=f"geocalc {__version__}")
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (("distance", "distance in kilometers"), ("bearing", "initial bearing in degrees"), ("midpoint", "midpoint as LAT LON")):
        p = sub.add_parser(name, help=help_text)
        for arg in ("lat1", "lon1", "lat2", "lon2"):
            p.add_argument(arg, type=float)
    args = parser.parse_args(argv)
    fn = {"distance": distance_km, "bearing": bearing, "midpoint": midpoint}[args.command]
    try:
        result = fn(args.lat1, args.lon1, args.lat2, args.lon2)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        import json
        print(json.dumps({"command": args.command, "result": result}))
    elif isinstance(result, tuple):
        print(f"{result[0]:.6f} {result[1]:.6f}")
    else:
        print(f"{result:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
