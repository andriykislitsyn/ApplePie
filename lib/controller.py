import os
from time import time

import PIL.ImageGrab
import cv2
import numpy as np

from lib.condition import wait_for

MIN_SIM = 0.92
WAIT_TIME = 5


class Controller:
    def __init__(self):
        self.directory = os.path.dirname(os.path.dirname(__file__))
        self.binary_cliclick = '{0}/bin/cliclick'.format(self.directory)

    def click(self, pattern, sim=MIN_SIM, wait=WAIT_TIME, x_off=0, y_off=0):
        """ Move the cursor to the center of the pattern and clicks once.
                :param str pattern: Path to the pattern to search for.
                :param float sim: Sensitivity parameter 90% match required for success
                :param int x_off: Move cursor left or right concerning the patter center
                :param int y_off: Move cursor above or below the patter center
                :param int wait: Time in seconds the method waits until a pattern appears on the Screen. """
        x, y = self.exists(pattern=pattern, sim=sim, wait=wait)
        os.system('{0} c:{1},{2}'.format(self.binary_cliclick, x + x_off, y + y_off))

    def exists(self, pattern, sim=MIN_SIM, wait=WAIT_TIME):
        """ Locate pattern on the Screen and returns its center coordinates
                :param pattern: Path to the pattern to search for.
                :param sim: Sensitivity parameter 90% match required for success
                :param wait: Time the method waits until a pattern appears on the Screen. """
        return wait_for(self.find_pattern, wait=wait, pattern=pattern, sim=sim)

    def double_click(self, pattern, sim=MIN_SIM, wait=WAIT_TIME, x_off=0, y_off=0):
        x, y = self.exists(pattern=pattern, sim=sim, wait=wait)
        os.system('{0} dc:{1},{2}'.format(self.binary_cliclick, x + x_off, y + y_off))

    def right_click(self, pattern, sim=MIN_SIM, wait=WAIT_TIME, x_off=0, y_off=0):
        x, y = self.exists(pattern=pattern, sim=sim, wait=wait)
        os.system('{0} kd:ctrl'.format(self.binary_cliclick))
        os.system('{0} c:{1},{2}'.format(self.binary_cliclick, x + x_off, y + y_off))
        os.system('{0} ku:ctrl'.format(self.binary_cliclick))

    def move(self, pattern, sim=MIN_SIM, wait=WAIT_TIME, x_off=0, y_off=0):
        x, y = self.exists(pattern=pattern, sim=sim, wait=wait)
        os.system('{0} m:{1},{2}'.format(self.binary_cliclick, x + x_off, y + y_off))

    def paste(self, pattern, sim=MIN_SIM, wait=WAIT_TIME, x_off=0, y_off=0, phrase=''):
        x, y = self.exists(pattern=pattern, sim=sim, wait=wait)
        os.system('{0} c:{1},{2}'.format(self.binary_cliclick, x + x_off, y + y_off))
        os.system('{0} p:"{1}"'.format(self.binary_cliclick, phrase))

    def count_matches(self, pattern, sim=MIN_SIM, wait=WAIT_TIME):
        return wait_for(self.find_pattern, wait=wait, pattern=pattern, sim=sim, get_matches_count=True)

    def find_pattern(self, pattern, sim=MIN_SIM, get_matches_count=False):
        """ Locate pattern(s) on the Screen and returns their number (its center coordinates)
                :param pattern: Path to the pattern to search for.
                :param sim: Sensitivity parameter 90% match required for success
                :param get_matches_count: Optional parameter, when set to True, counts number of times the pattern found
                :return: Number of times the pattern was found or coordinates of the first discovered pattern. """
        total = []
        cv2_pattern = cv2.imread(pattern, 0)
        w, h = cv2_pattern.shape[::-1]
        result = cv2.matchTemplate(self._snapshot(), cv2_pattern, cv2.TM_CCOEFF_NORMED)
        matches = np.where(result >= sim)
        for match in zip(*matches[::-1]):
            total.append((int(match[0] + w / 2), int(match[1] + h / 2)))
        if get_matches_count:
            return len(total)
        if total:
            return total[0]

    def wait_vanish(self, pattern, sim=MIN_SIM, wait=WAIT_TIME):
        end = time() + wait
        while time() < end:
            if not self.exists(pattern=pattern, sim=sim, wait=wait):
                return True

    @staticmethod
    def _snapshot():
        """ Make a screenshot of the Screen and converts it from PIL(Pillow) to CV2 Image object.
            :return numpy array: cv2 ready Image object. """
        desktop = PIL.ImageGrab.grab()
        pil_image = desktop.convert('RGB')
        open_cv_image = np.array(pil_image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        open_cv_image_gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        return open_cv_image_gray


controller = Controller()
