# Citing galvo-drift-correction

If you use this software in your research, please cite it. This helps sustain
open-source scientific software and gives proper credit.

## Recommended citation

> [Your Name] (2025). *galvo-drift-correction* (version 0.1.0).
> GitHub. https://github.com/your-username/galvo-drift-correction

### BibTeX

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

### APA

Nicolas Mateos. (2026). *galvo-drift-correction* (Version 0.1.0) [Software].
GitHub. https://github.com/nmateosHub/galvo-drift-correction

## Methods paragraph

If you need to describe the correction in a paper's methods section, you can
adapt the following:

> Line-shift artifacts caused by galvo mirror settling delays were corrected
> using galvo-drift-correction (v0.1.0; [Your Name], 2025). The pixel
> displacement of odd rows relative to even rows was estimated by maximising
> the normalised cross-correlation (NCC) between the two interleaved row
> sub-images across a search range of ±N pixels. The integer shift
> corresponding to the NCC peak was applied as a horizontal roll to all odd
> rows in each acquired frame.

## Zenodo DOI

Once this repository is archived on Zenodo, a permanent DOI will be listed here.
Zenodo records are automatically generated from GitHub releases — see
https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content.
