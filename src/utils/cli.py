import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="ThrustOptima CLI")

    parser.add_argument("path", type=str, help="Path to DICOM directory")

    parser.add_argument("--start", type=int, default=0, help="Starting scan index")
    parser.add_argument("--finish", type=int, default=-1, help="Ending scan index")

    parser.add_argument("-t", "--trace", action="store_true", help="Enable detailed trace logging")

    return parser.parse_args()
