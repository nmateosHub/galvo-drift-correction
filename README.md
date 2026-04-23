# galvo-drift-correction
Galvo drift correction is a lightweight Python library for detecting and correcting line-shift artifacts in laser-scanning microscopy images caused by galvo mirror settling delays. At high scan speeds, the galvo mirror fails to fully settle between lines, causing every odd row to be displaced horizontally by a fixed number of pixels relative to the even rows. 

## Background

Galvo scanners alternate between scanning odd and even lines. At high scan speeds, finite galvo settling time can offset every odd row by a fixed number of pixels relative to the even rows. This library detects that offset automatically from a single raw image and applies the inverse correction.

## How it works

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

The method relies on horizontal continuity between adjacent rows. It is robust on images with lateral features (edges, textures) and may be unreliable on featureless or purely vertically-striped images.

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
