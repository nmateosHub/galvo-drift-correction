"""
example_usage.py
----------------
Minimal end-to-end example: detect the galvo drift shift from a single
raw image and write the corrected version to disk.
"""

import tifffile
from galvo_drift_correction.correction import find_drift_shift, apply_drift_correction
import pathlib

# ── 1. Load a raw image ───────────────────────────────────────────────────────
raw = tifffile.imread("sample_data/raw.tif")

# ── 2. Detect the drift (no groundtruth needed) ───────────────────────────────
#    N=10 searches shifts in [-10, +10] pixels.
#    Set plot=True to visualise the score curve and a before/after preview.
shift = find_drift_shift(raw, N=10, plot=True)

# ── 3. Apply the correction ───────────────────────────────────────────────────
corrected = apply_drift_correction(raw, shift)

# ── 4. Save ───────────────────────────────────────────────────────────────────
tifffile.imwrite("sample_data/corrected.tif", corrected)
print("Saved corrected image to sample_data/corrected.tif")

# ── 5. Reuse the same shift for a batch of new acquisitions ───────────────────


for path in sorted(pathlib.Path("sample_data/batch").glob("*.tif")):
    img = tifffile.imread(path)
    out = apply_drift_correction(img, shift)
    tifffile.imwrite(path.with_stem(path.stem + "_corrected"), out)
    print(f"Corrected {path.name}")
