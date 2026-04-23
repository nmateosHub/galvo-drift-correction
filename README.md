# galvo-drift-correction
Lightweight Python library for automatic galvo line-drift correction in laser-scanning microscopy. Detects the horizontal pixel shift between interleaved odd/even rows via normalised cross-correlation — no groundtruth needed. Applies the correction to any subsequent acquisition from the same session in a single function call.
