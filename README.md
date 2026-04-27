# galvo-drift-correction

**Automatic line-shift correction for laser-scanning microscopy images — no groundtruth required.**

Galvo drift correction is a lightweight Python library for detecting and correcting line-shift artifacts in laser-scanning microscopy images caused by galvo mirror settling delays. At high scan speeds, the galvo mirror fails to fully settle between lines, causing every odd row to be displaced horizontally by a fixed number of pixels relative to the even rows. 


## The problem

At high galvo scan speeds, finite mirror settling time displaces every odd row by a fixed number of pixels relative to the even rows, introducing a characteristic **comb-like shearing** across the image.
<img width="916" height="669" alt="fig1_raw" src="https://github.com/user-attachments/assets/121038ec-9161-4b70-880a-c49508e5f769" />
*Synthetic fluorescence image with a +7 px drift on all odd rows. The staircase pattern is visible on any vertical edge.*

---

## How it works

The image is split into its two interleaved row sets — **even** `[0, 2, 4 …]` and **odd** `[1, 3, 5 …]`. In an undrifted image these two sub-images are highly similar. Galvo drift breaks that similarity by offsetting one set horizontally.
<img width="1966" height="683" alt="fig2_even_odd" src="https://github.com/user-attachments/assets/4dbd154e-07e4-4925-84f9-b7fc82cf8430" />

Zooming into a single horizontal stripe makes the row-by-row offset immediately visible:
<img width="1642" height="417" alt="fig3_interleaved" src="https://github.com/user-attachments/assets/6a30cb9f-b87d-42bf-8203-b16f85af5f0e" />

The algorithm rolls the odd sub-image by every candidate shift `s ∈ [−N, N]` and computes the **normalised cross-correlation (NCC)** with the even sub-image. The shift that maximises NCC is the drift:



```
raw image
    │
    ├── even rows  [0, 2, 4, …]  ──┐
    │                               ├── NCC score for each shift s ∈ [−N, N]
    └── odd rows   [1, 3, 5, …]  ──┘
            │
            └── roll by s, compare → argmax → best_shift
                                                    │
                                        apply −best_shift to odd rows
                                                    │
                                             corrected image
```
The score curve peaks sharply at the true drift. The three inset strips show the interleaved reconstruction at the worst, zero, and best candidate shifts:
<img width="2076" height="1117" alt="fig5_ncc_curve" src="https://github.com/user-attachments/assets/2ce49537-b557-4b9a-80d5-4d5af446c4cc" />

Applying the inverse shift restores full alignment:

<img width="1630" height="600" alt="fig4_shifted" src="https://github.com/user-attachments/assets/013a433b-d084-47db-9e88-7d0b0dc6b174" />


## Installation

```bash
pip install galvo-drift-correction
```

Or install from source:

```bash
git clone https://github.com/nmateosHub/galvo-drift-correction
cd galvo-drift-correction
pip install -e ".[dev]"
```

## Quick start

```python
import tifffile
from galvo_drift_correction import find_drift_shift, apply_drift_correction

raw = tifffile.imread("raw.tif")

# Detect shift — searches ±10 px by default, set plot=True to inspect
shift = find_drift_shift(raw, N=10, plot=True)

# Correct this image
corrected = apply_drift_correction(raw, shift)
tifffile.imwrite("corrected.tif", corrected)

# Reuse the same shift for every subsequent acquisition
for path in batch_paths:
    img = tifffile.imread(path)
    tifffile.imwrite(path.with_stem(path.stem + "_corrected"),
                     apply_drift_correction(img, -shift))
```

## API reference

### `find_drift_shift(rawimg, N=10, plot=False) → int`

Estimate the galvo line-drift shift from a single raw image.

| Parameter | Type | Description |
|-----------|------|-------------|
| `rawimg` | `np.ndarray` | 2-D grayscale image (any dtype) |
| `N` | `int` | Half-width of pixel search range. Tests all integers in `[−N, N]`. |
| `plot` | `bool` | Display NCC score curve and before/after preview. |

Returns the detected shift as a signed integer. Pass it directly to `apply_drift_correction`.

### `apply_drift_correction(img, shift) → np.ndarray`

Correct galvo line-drift by rolling odd rows by `−shift`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `img` | `np.ndarray` | 2-D raw image to correct |
| `shift` | `int` | Value returned by `find_drift_shift` |

Returns a corrected copy of `img` with the same shape and dtype.

## Running the tests

```bash
pytest --cov=galvo_drift_correction
```

## Requirements

- Python ≥ 3.9
- numpy ≥ 1.24
- scikit-image ≥ 0.21
- matplotlib ≥ 3.7
- tifffile ≥ 2023.1
- pytest

## License

MIT

## Citing this work

If you use galvo-drift-correction in your research, please cite it:

```bibtex
@software{galvo_drift_correction,
  author    = {Mateos, Nicolas},
  title     = {galvo-drift-correction},
  year      = {2026},
  version   = {0.1.0},
  publisher = {GitHub},
  url       = {https://github.com/nmateosHub/galvo-drift-correction},
  license   = {MIT}
}
```

See [CITATION.md](CITATION.md) for APA format, a ready-made methods paragraph,
and instructions for obtaining a permanent Zenodo DOI.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use,
modify, and distribute it for any purpose. Attribution through citation is
strongly encouraged — see [CITATION.md](CITATION.md).
