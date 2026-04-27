"""
tests/test_correction.py
------------------------
Unit tests for galvo_drift_correction.
"""

import numpy as np
import pytest
from galvo_drift_correction.correction import find_drift_shift, apply_drift_correction


def _make_structured(height: int = 64, width: int = 128, seed: int = 42) -> np.ndarray:
    """
    Return a spatially structured base image (smooth + edges) that gives the
    NCC method enough signal to detect alignment.  Pure random noise has no
    inter-row correlation, so it is unsuitable for testing this algorithm.
    """
    rng = np.random.default_rng(seed)
    x = np.linspace(0, 4 * np.pi, width)
    y = np.linspace(0, 4 * np.pi, height)
    xx, yy = np.meshgrid(x, y)
    base = (np.sin(xx) * np.cos(yy) * 127 + 128).astype(np.uint16)
    base += rng.integers(0, 10, base.shape, dtype=np.uint16)
    return base


def _make_synthetic(shift: int, height: int = 64, width: int = 128, seed: int = 42) -> np.ndarray:
    """
    Return a structured image whose odd rows are shifted by *shift* pixels.

    Sign convention matches the library:
      - positive shift  → odd rows rolled right
      - negative shift  → odd rows rolled left
    apply_drift_correction undoes this by rolling odd rows by -shift.
    """
    base = _make_structured(height, width, seed)
    img = base.copy()
    img[1::2, :] = np.roll(base[1::2, :], shift, axis=1)
    return img


# ---------------------------------------------------------------------------
# find_drift_shift
# ---------------------------------------------------------------------------

class TestFindDriftShift:
    @pytest.mark.parametrize("true_shift", [-5, -3, 0, 3, 5])
    def test_detects_known_shift(self, true_shift):
        img = _make_synthetic(true_shift)
        detected = find_drift_shift(img, N=8)
        assert detected == true_shift

    def test_returns_int(self):
        img = _make_synthetic(2)
        result = find_drift_shift(img, N=5)
        assert isinstance(result, int)

    def test_zero_shift_on_aligned_image(self):
        img = _make_structured()
        assert find_drift_shift(img, N=5) == 0

    def test_odd_height_image(self):
        img = _make_synthetic(2, height=63)
        detected = find_drift_shift(img, N=5)
        assert detected == 2


# ---------------------------------------------------------------------------
# apply_drift_correction
# ---------------------------------------------------------------------------

class TestApplyDriftCorrection:
    def test_corrects_known_shift(self):
        true_shift = 4
        base = _make_structured()
        img = _make_synthetic(true_shift)
        corrected = apply_drift_correction(img, true_shift)
        # Odd rows should now match the original unshifted base
        min_h = base[1::2].shape[0]
        diff = np.abs(corrected[1::2, :][:min_h].astype(int) - base[1::2, :][:min_h].astype(int))
        assert diff.mean() < 1.0

    def test_returns_copy(self):
        img = _make_synthetic(3)
        corrected = apply_drift_correction(img, 3)
        assert corrected is not img

    def test_preserves_dtype(self):
        for dtype in [np.uint8, np.uint16, np.float32]:
            img = _make_synthetic(2).astype(dtype)
            out = apply_drift_correction(img, 2)
            assert out.dtype == dtype

    def test_preserves_shape(self):
        img = _make_synthetic(1, height=50, width=100)
        out = apply_drift_correction(img, 1)
        assert out.shape == img.shape

    def test_zero_shift_is_identity(self):
        img = _make_synthetic(0)
        out = apply_drift_correction(img, 0)
        np.testing.assert_array_equal(out, img)


# ---------------------------------------------------------------------------
# Round-trip
# ---------------------------------------------------------------------------

class TestRoundTrip:
    @pytest.mark.parametrize("shift", [-7, -2, 1, 6])
    def test_detect_then_correct(self, shift):
        base = _make_structured(height=80, width=160)
        img = _make_synthetic(shift, height=80, width=160)
        detected = find_drift_shift(img, N=10)
        assert detected == shift
        corrected = apply_drift_correction(img, detected)
        # Odd rows should be restored to the unshifted base
        min_h = base[1::2].shape[0]
        diff = np.abs(corrected[1::2, :][:min_h].astype(int) - base[1::2, :][:min_h].astype(int))
        assert diff.mean() < 1.0
