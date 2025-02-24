import argparse


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-seed", "-s", type=int, help="random video seed")
    return parser

def parse_args() -> argparse.Namespace:
    parser = _create_parser()
    return parser.parse_args()


