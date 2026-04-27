"""
galvo_drift_correction.correction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Functions to detect and correct galvo line-drift in laser-scanning
microscopy images.

Galvo scanners alternate between odd and even lines. Finite galvo
settling time can offset every odd row by a fixed number of pixels
relative to the even rows. The two public functions here detect that
offset from a single raw image (no groundtruth required) and apply
the inverse correction.
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import match_template


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

def _normalize(img: np.ndarray) -> np.ndarray:
    """Return a float64 copy of *img* with zero mean and unit standard deviation."""
    img = img.astype(np.float64)
    return (img - img.mean()) / img.std()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def find_drift_shift(
    rawimg: np.ndarray,
    N: int = 10,
    plot: bool = False,
) -> int:
    """Estimate the galvo line-drift shift from a single raw image.

    The image is split into its even-row and odd-row sub-images.
    For every candidate integer shift *s* in ``[-N, N]`` the odd rows
    are rolled horizontally by *s* pixels and the normalised
    cross-correlation (NCC) with the even rows is computed.  The shift
    that maximises NCC is the drift present in the raw image.

    Parameters
    ----------
    rawimg:
        2-D grayscale array (any integer or float dtype).
    N:
        Half-width of the search range in pixels.  The function tests
        every integer shift in ``[-N, N]`` (inclusive).
    plot:
        When ``True``, display a score-vs-shift curve and a side-by-side
        comparison of the raw and corrected images.

    Returns
    -------
    int
        The detected shift (pixels, signed).  Pass this directly to
        :func:`apply_drift_correction`.

    Notes
    -----
    The method relies on the assumption that adjacent rows in the
    undrifted image are highly correlated.  It performs poorly on
    featureless images or images with predominantly vertical structure.
    Increase *N* if the true drift might exceed the default search range.

    Examples
    --------
    >>> import tifffile
    >>> from galvo_drift_correction import find_drift_shift, apply_drift_correction
    >>> raw = tifffile.imread("raw.tif")
    >>> shift = find_drift_shift(raw, N=10, plot=True)
    >>> corrected = apply_drift_correction(raw, shift)
    >>> tifffile.imwrite("corrected.tif", corrected)
    """
    even_rows = rawimg[0::2, :]
    odd_rows  = rawimg[1::2, :]

    min_h     = min(even_rows.shape[0], odd_rows.shape[0])
    even_norm = _normalize(even_rows[:min_h, :])
    odd_norm  = _normalize(odd_rows[:min_h, :])

    shifts = np.arange(-N, N + 1)
    scores = np.array([
        np.mean(np.roll(odd_norm, int(s), axis=1) * even_norm)
        for s in shifts
    ])

    best_idx = int(np.argmax(scores))
    # Rolling odd rows by +s aligns them with even — meaning the drift
    # present in the raw image is -s. We negate so that best_shift
    # represents the actual displacement that needs to be undone, and
    # apply_drift_correction simply rolls odd rows by -best_shift.
    best_shift = -int(shifts[best_idx])

    if plot:
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        axes[0].plot(shifts, scores, "o-")
        axes[0].axvline(best_shift, color="red", linestyle="--",
                        label=f"best = {best_shift:+d} px")
        axes[0].set_xlabel("Shift (px)")
        axes[0].set_ylabel("Mean NCC")
        axes[0].set_title("Inter-row similarity vs shift")
        axes[0].legend()

        corrected = apply_drift_correction(rawimg, best_shift)
        axes[1].imshow(np.hstack([rawimg, corrected]), cmap="gray")
        axes[1].set_title("Raw  |  Corrected")
        axes[1].axis("off")

        plt.tight_layout()
        plt.show()

    print(f"[find_drift_shift] best_shift={best_shift:+d} px  "
          f"(score={scores[best_idx]:.4f})")
    return best_shift


def apply_drift_correction(
    img: np.ndarray,
    shift: int,
) -> np.ndarray:
    """Correct galvo line-drift by rolling odd rows by ``-shift``.

    Because :func:`find_drift_shift` detects the shift *present in the
    raw image*, the correction is the inverse: odd rows are rolled by
    ``-shift`` to realign them with the even rows.

    Parameters
    ----------
    img:
        2-D raw image to correct (any dtype; a copy is returned).
    shift:
        Value returned by :func:`find_drift_shift`.

    Returns
    -------
    numpy.ndarray
        Corrected copy of *img* with the same shape and dtype.

    Examples
    --------
    >>> corrected = apply_drift_correction(raw, shift)
    """
    corrected = img.copy()
    corrected[1::2, :] = np.roll(corrected[1::2, :], -shift, axis=1)
    return corrected
