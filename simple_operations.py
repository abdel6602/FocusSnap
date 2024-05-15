import cv2
import numpy as np

def load_image(image_path):
    return cv2.imread(image_path)

def show_image(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def save_image(image, image_path):
    cv2.imwrite(image_path, image)

def resize_image(image, width, height):
    return cv2.resize(image, (width, height))

def crop_image(image, x, y, width, height):
    return image[y:y+height, x:x+width]

def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h))

def flip_image(image, direction):
    return cv2.flip(image, direction)

def convert_to_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def convert_to_hsv(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

def convert_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def apply_threshold(image, threshold):
    _, thresholded_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return thresholded_image

def apply_blur(image, kernel_size):
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def apply_dilation(image, kernel_size):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.dilate(image, kernel, iterations=1)

def apply_erosion(image, kernel_size):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.erode(image, kernel, iterations=1)

def apply_morphological_transformation(image, kernel_size, operation):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.morphologyEx(image, operation, kernel)

def apply_canny(image, threshold1, threshold2):
    return cv2.Canny(image, threshold1, threshold2)

def apply_contours(image):
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def draw_contours(image, contours):
    return cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

def get_contour_area(contour):
    return cv2.contourArea(contour)

def get_contour_perimeter(contour):
    return cv2.arcLength(contour, True)

def get_contour_center(contour):
    M = cv2.moments(contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (cX, cY)

def get_contour_approximation(contour, epsilon):
    return cv2.approxPolyDP(contour, epsilon, True)

def get_contour_convex_hull(contour):
    return cv2.convexHull(contour)

def get_contour_bounding_box(contour):
    x, y, w, h = cv2.boundingRect(contour)
    return (x, y, w, h)

def get_contour_min_area_rect(contour):
    return cv2.minAreaRect(contour)

def get_contour_min_enclosing_circle(contour):
    return cv2.minEnclosingCircle(contour)

def get_contour_orientation(contour):
    ellipse = cv2.fitEllipse(contour)
    return ellipse

def get_contour_aspect_ratio(contour):
    x, y, w, h = cv2.boundingRect(contour)
    return float(w) / h

def get_contour_extent(contour):
    area = cv2.contourArea(contour)
    x, y, w, h = cv2.boundingRect(contour)
    rect_area = w * h
    return float(area) / rect_area

def get_contour_solidity(contour):
    area = cv2.contourArea(contour)
    hull = cv2.convexHull(contour)
    hull_area = cv2.contourArea(hull)
    return float(area) / hull_area

def get_contour_equivalent_diameter(contour):
    area = cv2.contourArea(contour)
    return 2 * ((area / 3.14159265) ** 0.5)

def get_contour_mask(image, contour):
    mask = np.zeros(image.shape, np.uint8)
    return cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)

def get_contour_hull_mask(image, contour):
    mask = np.zeros(image.shape, np.uint8)
    hull = cv2.convexHull(contour)
    return cv2.drawContours(mask, [hull], -1, (255, 255, 255), -1)

def median_blur(image, kernel_size):
    return cv2.medianBlur(image, kernel_size)

def apply_filter(image, kernel):
    return cv2.filter2D(image, -1, kernel)

def apply_sobel(image, dx, dy, kernel_size):
    return cv2.Sobel(image, cv2.CV_64F, dx, dy, ksize=kernel_size)

def apply_prewitt(image, dx, dy):
    kernel_x = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    kernel_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    gradient_x = cv2.filter2D(image, -1, kernel_x)
    gradient_y = cv2.filter2D(image, -1, kernel_y)
    return gradient_x, gradient_y

def apply_shear(image, shear_x_factor, shear_y_factor):
    shear_matrix = np.array([[1, shear_x_factor, 0], [shear_y_factor, 1, 0], [0,0,1]])
    return cv2.warpAffine(image, shear_matrix, (image.shape[1], image.shape[0]))

def apply_affine_transform(image, transformation_matrix):
    return cv2.warpAffine(image, transformation_matrix, (image.shape[1], image.shape[0]))

def apply_perspective_transform(image, transformation_matrix):
    return cv2.warpPerspective(image, transformation_matrix, (image.shape[1], image.shape[0]))

def apply_histogram_equalization(image):
    return cv2.equalizeHist(image)

def hough_lines(image, rho, theta, threshold):
    return cv2.HoughLines(image, rho, theta, threshold)

def harries_corners(image, max_corners, quality_level, min_distance):
    return cv2.goodFeaturesToTrack(image, max_corners, quality_level, min_distance)

def draw_harries_corners(image, corners):
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(image, (x, y), 3, 255, -1)
    return image

def draw_hough_lines(image, lines):
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image, (x1, y1), (x2, y2), 255, 2)
    return image

def apply_harris_corner_detection(image, block_size, ksize, k):
    return cv2.cornerHarris(image, block_size, ksize, k)

def convert_to_frequency_domain(image):
    return np.fft.fft2(image)

def convert_to_spatial_domain(image):
    return np.fft.ifft2(image)

def apply_high_pass_filter(image, cutoff_frequency):
    rows, cols = image.shape
    crow, ccol = rows / 2, cols / 2
    fshift = np.fft.fftshift(image)
    fshift[crow - cutoff_frequency:crow + cutoff_frequency, ccol - cutoff_frequency:ccol + cutoff_frequency] = 0
    return np.fft.ifftshift(fshift)

def apply_low_pass_filter(image, cutoff_frequency):
    rows, cols = image.shape
    crow, ccol = rows / 2, cols / 2
    fshift = np.fft.fftshift(image)
    mask = np.zeros((rows, cols), np.uint8)
    mask[crow - cutoff_frequency:crow + cutoff_frequency, ccol - cutoff_frequency:ccol + cutoff_frequency] = 1
    fshift = fshift * mask
    return np.fft.ifftshift(fshift)

def apply_band_pass_filter(image, low_cutoff, high_cutoff):
    rows, cols = image.shape
    crow, ccol = rows / 2, cols / 2
    fshift = np.fft.fftshift(image)
    mask = np.zeros((rows, cols), np.uint8)
    mask[crow - high_cutoff:crow + high_cutoff, ccol - high_cutoff:ccol + high_cutoff] = 1
    mask[crow - low_cutoff:crow + low_cutoff, ccol - low_cutoff:ccol + low_cutoff] = 0
    fshift = fshift * mask
    return np.fft.ifftshift(fshift)
