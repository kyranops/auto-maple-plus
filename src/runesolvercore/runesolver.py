import time
import src.runesolvercore.gdi_capture as gdi_capture
from interception import press
import numpy as np
import cv2 as cv
import mss
import src.common.utils as utils
import src.common.config as config
import math

# DEFINE CV Variables
RUNE_BGRA = (255, 102, 221, 255)
INSIDE_CS_TEMPLATE = cv.imread('assets/insidecashshop.png', 0)
CS_FAIL_TEMPLATE = cv.imread('assets/csFail.png',0)

def find_arrow_directions(img, debug=False):
    bgr = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
    hsv = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
    m, n = len(h), len(h[0])
    valid_gradient = []
    directions = []

    if debug:
        visited = [[False for _ in range(n)] for _ in range(m)]
        canvas = np.zeros(img.shape[:2], dtype="uint8")

    def hue_is_red(r, c):
        return 5 <= h[r][c] <= 12 and s[r][c] >= 65 and v[r][c] >= 128

    def hue_is_valid(r1, c1, r2, c2, diff):
        return abs(int(h[r1][c1]) - int(h[r2][c2])) <= diff and s[r2][c2] >= 150 and v[r2][c2] >= 150 and h[r2][c2] <= 70

    def near_gradient(r, c):
        for i, j in valid_gradient:
            if abs(i-r) < 15 and abs(c-j) < 15:
                return True
        return False

    def gradient_exists(r1, c1, delta_r, delta_c):
        if near_gradient(r1, c1):
            return False

        tmp_r1, tmp_c1 = r1, c1
        rune_gradient = False
        # The directional arrows that appear in runes are around 30 pixels long.
        for _ in range(30):
            r2 = tmp_r1 + delta_r
            c2 = tmp_c1 + delta_c
            if 0 <= r2 < m and 0 <= c2 < n:
                # Check if the next pixel maintains the gradient.
                if hue_is_valid(tmp_r1, tmp_c1, r2, c2, 10):
                    # If the pixel is a green-ish color, it is a possible arrow.
                    if 50 <= h[r2][c2] <= 70:
                        rune_gradient = True
                        valid_gradient.append((r1, c1))
                        break
                    tmp_r1 = r2
                    tmp_c1 = c2
                else:
                    break
            else:
                break

        return rune_gradient

    def expand_gradient(r1, c1, direction):
        stack = [(r1, c1)]
        while stack:
            r2, c2 = stack.pop()
            visited[r2][c2] = True
            if r2 + 1 < m:
                if not visited[r2 + 1][c2] and hue_is_valid(r2, c2, r2 + 1, c2, 2 if direction else 10):
                    stack.append((r2 + 1, c2))
            if r2 - 1 >= 0:
                if not visited[r2 - 1][c2] and hue_is_valid(r2, c2, r2 - 1, c2, 2 if direction else 10):
                    stack.append((r2 - 1, c2))
            if c2 + 1 < n:
                if not visited[r2][c2 + 1] and hue_is_valid(r2, c2, r2, c2 + 1, 10 if direction else 2):
                    stack.append((r2, c2 + 1))
            if c2 - 1 >= 0:
                if not visited[r2][c2 - 1] and hue_is_valid(r2, c2, r2, c2 - 1, 10 if direction else 2):
                    stack.append((r2, c2 - 1))
            canvas[r2][c2] = 180

    def find_direction(r, c):
        if gradient_exists(r, c, 0, -1):
            return "right"
        elif gradient_exists(r, c, 0, 1):
            return "left"
        elif gradient_exists(r, c, -1, 0):
            return "down"
        elif gradient_exists(r, c, 1, 0):
            return "up"
        else:
            return None

    _, imw, _ = img.shape
    rune_left_bound = math.trunc((imw - 500)/2)
    rune_right_bound = rune_left_bound + 500

    print("left: {}, right: {}".format(rune_left_bound,rune_right_bound))

    # The rune captcha was observed to appear within this part of the application window on 1366x768 resolution.
    for r in range(150, 300):
        for c in range(rune_left_bound, rune_right_bound):
            # Arrows start at a red-ish color and are around 15 pixels apart.
            if hue_is_red(r, c) and not near_gradient(r, c):
                direction = find_direction(r, c)
                if direction:
                    directions.append((direction, (r, c)))
                    if debug:
                        if direction == "LEFT" or direction == "RIGHT":
                            expand_gradient(r, c, 1)
                        else:
                            expand_gradient(r, c, 0)

    if debug:
        cv.imshow("Hue", h)
        cv.imshow("Saturation", s)
        cv.imshow("Value", v)
        cv.imshow("Original", img)
        cv.imshow("Parsed", canvas)
        cv.waitKey(0)

    return sorted(directions, key=lambda x: x[1][1])

def locate(self, *color):
    with gdi_capture.CaptureWindow(self.hwnd) as img:
        locations = []
        if img is None:
            pass
        else:
            # Crop the image to show only the mini-map.
            img_cropped = img[self.left:self.right, self.top:self.bottom]
            height, width = img_cropped.shape[0], img_cropped.shape[1]
            # Reshape the image from 3-d to 2-d by row-major order.
            img_reshaped = np.reshape(img_cropped, ((width * height), 4), order="C")
            for c in color:
                sum_x, sum_y, count = 0, 0, 0
                # Find all index(s) of np.ndarray matching a specified BGRA tuple.
                matches = np.where(np.all((img_reshaped == c), axis=1))[0]
                for idx in matches:
                    # Calculate the original (x, y) position of each matching index.
                    sum_x += idx % width
                    sum_y += idx // width
                    count += 1
                if count > 0:
                    x_pos = sum_x / count
        
                    y_pos = sum_y / count
                    locations.append((x_pos, y_pos))
        return locations

def get_rune_location(self):
    location = locate(self,RUNE_BGRA)
    return location[0] if len(location) > 0 else None

def enterCashshop(self):
    print("Entering Cashshop..")
    cashShopKey = self.config['Cash Shop']
    press(cashShopKey, 1)
    time.sleep(2)
    while utils.multi_match(config.capture.frame,INSIDE_CS_TEMPLATE,threshold=0.9) == [] or utils.multi_match(config.capture.frame,CS_FAIL_TEMPLATE,threshold=0.9) != []:
        if config.enabled == False:
            return True
        print("Inside CS: {}".format(utils.multi_match(config.capture.frame,INSIDE_CS_TEMPLATE, threshold=0.8)))
        print("CS Fail: {}".format(utils.multi_match(config.capture.frame,INSIDE_CS_TEMPLATE, threshold=0.8)))
        print("Fail to enter cash shop, trying again")
        press("esc" ,1)
        time.sleep(0.5)
        press(cashShopKey, 1)
        time.sleep(2)
    print("Exiting Cashshop")
    while utils.multi_match(config.capture.frame,INSIDE_CS_TEMPLATE,threshold=0.9) != []:
        if config.enabled == False:
            return True
        press("esc", 1)
        time.sleep(0.5)
        press("esc", 1)
        time.sleep(0.5)
        press("enter", 1)
        time.sleep(2.5)

def get_rune_image(win):
        with gdi_capture.CaptureWindow(win) as img:
            return img.copy()

def solve_rune_raw(self):
    #assumes user is already at rune
    attempts = 0
    while attempts <= 3 and config.enabled == True:
        npcChatKey = self.config['NPC/Gather']
        press(npcChatKey, 1)
        time.sleep(0.2)

        with mss.mss() as sct:
            # The screen part to capture
            window = config.capture.window
            output = "assets/rune_capture.png"
            sct_img = sct.grab(window)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

        directions = find_arrow_directions(cv.imread(output))
        if len(directions) == 4:
            print(f"Directions: {directions}.")
            for d, _ in directions:
                press(d, 1)
            
            time.sleep(1)
            rune_location = get_rune_location(self)
            if rune_location is None:
                print("Rune has been solved.")
                time.sleep(1)
                return True
            else:
                print("Trying again...")
        else:
            print("Rune unidentifiable. Trying again...")
            press(npcChatKey, 1)
            time.sleep(1.5)
            attempts += 1
            if attempts > 3:
                enterCashshop(self)
                attempts = 0
                time.sleep(0.5)
                return False
        time.sleep(3)
    return False