# galvo-drift-correction
Galvo drift correction is a lightweight Python library for detecting and correcting line-shift artifacts in laser-scanning microscopy images caused by galvo mirror settling delays. At high scan speeds, the galvo mirror fails to fully settle between lines, causing every odd row to be displaced horizontally by a fixed number of pixels relative to the even rows. 

The library estimates this displacement automatically from a single raw image (no groundtruth or calibration target required) by maximising the normalised cross-correlation between the interleaved even and odd row sub-images across a user-defined pixel search range. Once the shift is known it can be applied as a one-pixel-precision correction to any number of subsequent acquisitions from the same microscope session.

For specific situations when the images taken lack structure, there is fast diffusion, small objects,... Then a calibration target is required to calculate the shift to be applied in the experimental acquisitions.
