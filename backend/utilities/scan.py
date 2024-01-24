"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************
"""
import numpy as np
import pydicom
import matplotlib.pyplot as plt
import cv2


class Scan:
    def __init__(self, data: pydicom.FileDataset):

        if data is None:
            raise ValueError("The data provided is invalid.")

        self._pixel_array: np.array(float) = data.pixel_array
        self._id: int = data.InstanceNumber
        self._pid: str = data.PatientID
        self._RescaleSlope: float = data.RescaleSlope
        self._RescaleIntercept: float = data.RescaleIntercept

        self._normalized: bool = False
        self._shaped: bool = False
        self._shaped_pixel_array: np.array(float) = None
        self._ratio: int = 0

    def shape(self):
        if not self._normalized:
            self._normalize()

        self._shaped = self._shape()

    def _shape(self):

        threshold = cv2.threshold(cv2.GaussianBlur(self._shaped_pixel_array, (5, 5), 0),
                                  0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        contours = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

        if len(contours) == 0:
            return False

        cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)

        self._shaped_pixel_array = self._shaped_pixel_array[y:y+h, x:x+w]

        plt.imshow(self._shaped_pixel_array, cmap="gray")
        plt.show()

        return True

    def _normalize(self):
        self._shaped_pixel_array = self._pixel_array * self._RescaleSlope + self._RescaleIntercept
        self._shaped_pixel_array = self._shaped_pixel_array.clip(min=0, max=255).astype(np.uint8)
        self._normalized = True

    @property
    def id(self):
        return self._id

    @property
    def ratio(self):
        return self._ratio

    @property
    def patient_id(self):
        return self._pid

    @property
    def shaped(self):
        return self._shaped

    @property
    def shaped_pixel_array(self):
        return self._shaped_pixel_array
