"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2026
All Rights Reserved.
******************************************************************
"""

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path


def normalize_pixel_array(pixel_array, rescale_slope: float, rescale_intercept: float):
    if pixel_array is None:
        raise ValueError("The pixel array provided is invalid.")

    if not isinstance(rescale_slope, (int, float)) or not isinstance(rescale_intercept, (int, float)):
        raise ValueError("The rescale slope and intercept must be numeric values.")

    if rescale_slope != 1.0:
        pixel_array = pixel_array * rescale_slope

    if rescale_intercept != 0.0:
        pixel_array = pixel_array + rescale_intercept

    return pixel_array


@dataclass
class ScanMetadata:
    id: int
    pid: str
    rescale_slope: float
    rescale_intercept: float
    path: Path

    calculated: bool = False
    propensity_score: float = 0.0

    @cached_property
    def pixel_array(self):
        import pydicom
        data: pydicom.FileDataset = pydicom.dcmread(self.path)

        pixels = normalize_pixel_array(data.pixel_array, self.rescale_slope, self.rescale_intercept)

        return pixels
