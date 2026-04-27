"""
galvo_drift_correction
======================
Detect and correct galvo line-drift in laser-scanning microscopy images.

Public API
----------
.. autofunction:: galvo_drift_correction.find_drift_shift
.. autofunction:: galvo_drift_correction.apply_drift_correction
"""

from galvo_drift_correction.correction import find_drift_shift, apply_drift_correction

__all__ = ["find_drift_shift", "apply_drift_correction"]
__version__ = "0.1.0"
