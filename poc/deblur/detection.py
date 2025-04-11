import cv2
import numpy
import numpy as np


def calc_blur_laplacian(image: numpy.ndarray) -> float:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()


def calc_blur_fft(image: numpy.ndarray) -> float:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate FFT and shift zero frequency to center
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = np.abs(fshift)

    # Get image dimensions
    rows, cols = gray.shape
    center_row, center_col = rows // 2, cols // 2

    # Create circular mask
    radius = 10  # Adjust this value to change sensitivity
    y, x = np.ogrid[-center_row:rows - center_row, -center_col:cols - center_col]
    mask_area = x * x + y * y <= radius * radius

    # Calculate a ratio of high frequencies to low frequencies
    low_freq = np.sum(magnitude_spectrum[mask_area])
    high_freq = np.sum(magnitude_spectrum) - low_freq
    blur_score = high_freq / low_freq if low_freq > 0 else 0

    # Normalize score for easier interpretation
    normalized_score = np.log10(blur_score + 1) * 100
    return normalized_score
