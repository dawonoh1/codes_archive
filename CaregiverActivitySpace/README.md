# CaregiverActivitySpace (R)

- NHTS 2017 + restricted block-group files (data not included)
- question: parents with a child 0–9 vs. adults with no dependents → daily activity space
- activity space = convex hull of home + destinations (Hasanzadeh et al. 2017)
- `AS_centroid_nobuffer_sizelimit*.rmd`: block-group centroids, home 500 m / destination 140 m buffers, only block groups ≤ 1 km² → latest `_3` (Oct 12)
- `data_processing*.rmd` (up to `_10`): polygon + 100 m buffer version → latest `_9` (Jul 23)
- OLS on log(area); weekend; child × gender
- result: with a child, about 9% smaller after controls, mostly for women
- `data/` = NHTS dictionaries + citation
