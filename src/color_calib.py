from constance import *


class HSVToleranceCalib:

    def __init__(self, window_name='Color calibrator'):
        self._h_tol_val = 0
        self._s_tol_val = 0
        self._v_tol_val = 0
        self._wname = window_name

    def _on_change_h(self, pos):
        self._h_tol_val = pos / 100.0

    def _on_change_s(self, pos):
        self._s_tol_val = pos / 100.0

    def _on_change_v(self, pos):
        self._v_tol_val = pos / 100.0

    def get_tolerance(self):
        # print 'tolerance = ', [self._h_tol_val, self._s_tol_val, self._v_tol_val]
        return [self._h_tol_val, self._s_tol_val, self._v_tol_val]

    def create(self):
        cv2.namedWindow(self._wname)
        cv2.createTrackbar('Hue tolerance', self._wname, MIN_TOLERANCE, MAX_TOLERANCE, self._on_change_h)
        cv2.createTrackbar('Saturation tolerance', self._wname, MIN_TOLERANCE, MAX_TOLERANCE, self._on_change_s)
        cv2.createTrackbar('Value tolerance', self._wname, MIN_TOLERANCE, MAX_TOLERANCE, self._on_change_v)


class ColorPickerBGR:

    def __init__(self, window_name='BGR color picker'):
        self._b = 0
        self._g = 0
        self._r = 0
        self._wname = window_name
        self._img = np.zeros((300, 500, 3), np.uint8)

    def _on_change_b(self, pos):
        self._b = pos

    def _on_change_g(self, pos):
        self._g = pos

    def _on_change_r(self, pos):
        self._r = pos

    def set_color(self):
        self._img[:] = [self._b, self._g, self._r]
        cv2.imshow(self._wname, self._img)

    def get_color(self):
        return self._b, self._g, self._r

    def create(self):
        cv2.namedWindow(self._wname)
        cv2.createTrackbar('Blue', self._wname, MIN_VAL, MAX_VAL, self._on_change_b)
        cv2.createTrackbar('Green', self._wname, MIN_VAL, MAX_VAL, self._on_change_g)
        cv2.createTrackbar('Red', self._wname, MIN_VAL, MAX_VAL, self._on_change_r)


if __name__ == '__main__':

    color_picker = ColorPickerBGR()
    color_picker.create()

    while cv2.waitKey(1) != ord('q'):
        color_picker.set_color()


