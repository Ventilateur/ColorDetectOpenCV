from constance import *

ORIGIN_IMG = 'origin'
MASKED_IMG = 'masked'
FILTERED_IMG = 'filtered'
MAX_SIZE = (40 * 40)
K_SIZE = (5, 5)


class ColorDetect:

    HSV, RGB, HLS, LUV, LAB, No_filter = range(6)

    def __init__(self):
        self._click_position = (0, 0)
        self._upper_color = np.array([0, 0, 0])
        self._lower_color = np.array([0, 0, 0])
        self._tolerance = np.array([0.40, 0.40, 0.40])
        self._img = None
        self._masked_img = None
        self._filtered_img = None
        self._contours = None

    # --------------------------------------- #
    # ----------- PRIVATE METHODS ----------- #
    # --------------------------------------- #

    def _set_pixel_color_thresh(self, pixel_color):
        # Set lower and upper thresholds
        self._upper_color = np.array([pixel_color[0] * (1 + self._tolerance[0]),
                                      pixel_color[1] * (1 + self._tolerance[1]),
                                      pixel_color[2] * (1 + self._tolerance[2])])
        self._lower_color = np.array([pixel_color[0] * (1 - self._tolerance[0]),
                                      pixel_color[1] * (1 - self._tolerance[1]),
                                      pixel_color[2] * (1 - self._tolerance[2])])

    def _on_mouse(self, event, x, y, flag, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Get mouse position
            self._click_position = (y, x)

    def _opening_op(self, k_size):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, k_size)
        open_img = cv2.morphologyEx(self._masked_img, cv2.MORPH_OPEN, kernel)
        return open_img

    def initialize(self):
        cv2.namedWindow(ORIGIN_IMG)
        cv2.namedWindow(FILTERED_IMG)
        cv2.setMouseCallback(FILTERED_IMG, self._on_mouse)

    # --------------------------------------- #
    # ------------ PUBLIC METHODS ----------- #
    # --------------------------------------- #

    def run(self, img, filter_mode=HSV):
        self._img = img
        blurred_img = cv2.GaussianBlur(self._img, (11, 11), 5)

        if filter_mode == ColorDetect.HSV:
            self._filtered_img = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2HSV)
        elif filter_mode == ColorDetect.HLS:
            self._filtered_img = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2HLS)
        elif filter_mode == ColorDetect.RGB:
            self._filtered_img = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2RGB)
        elif filter_mode == ColorDetect.LUV:
            self._filtered_img = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2LUV)
        elif filter_mode == ColorDetect.LAB:
            self._filtered_img = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2LAB)
        else:
            self._filtered_img = blurred_img

        self._set_pixel_color_thresh(self._filtered_img[self._click_position])
        self._masked_img = cv2.inRange(self._filtered_img, self._lower_color, self._upper_color)
        self._masked_img = self._opening_op(K_SIZE)

    def set_tolerance(self, val):
        self._tolerance = val

    def display(self, show_mask=False):
        cv2.imshow(ORIGIN_IMG, self._img)
        cv2.imshow(FILTERED_IMG, self._filtered_img)
        if show_mask:
            cv2.imshow(MASKED_IMG, self._masked_img)

    def draw_contours(self, color=GREEN, thickness=3, filtered=False, show_center=False):
        _, self._contours, _ = cv2.findContours(self._masked_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if filtered:
            if len(self._contours) != 0:
                for i in xrange(len(self._contours)):
                    # Finding the center of a contour
                    moment = cv2.moments(self._contours[i])
                    if moment['m00'] > MAX_SIZE:
                        cx = int(moment['m10'] / moment['m00'])
                        cy = int(moment['m01'] / moment['m00'])
                        if show_center:
                            cv2.circle(self._img, (cx, cy), 3, RED)
                        cv2.drawContours(self._img, self._contours, i, color, thickness=thickness)
        else:
            cv2.drawContours(self._img, self._contours, ALL_CONTOURS, color, thickness=thickness)
            # print 'Number of contours = ', len(self._contours)


if __name__ == '__main__':

    color_detect = ColorDetect()
    cam = cv2.VideoCapture(0)
    color_detect.initialize()

    while cv2.waitKey(1) != ord('q'):
        _, frame = cam.read()
        color_detect.run(frame)
        color_detect.draw_contours()
        color_detect.display()

    cam.release()
    cv2.destroyAllWindows()
