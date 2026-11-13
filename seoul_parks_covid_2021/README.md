# seoul_parks_covid_2021 (R)

- 2021 Aug–Oct, ACSP
- `kshape/`, `rsave/`: cluster parks by 2020 data (DTW clustering, hierarchical, k-means)
- `mlogit/`: multinomial logit, park cluster ~ park attributes
- panel folders: Y = LUM, FE vs RE (plm), Hausman / F / LM tests; folder name = date (210827 = Aug 27)
- `ols/`, `rsave/cross.R`: crossed random effects (district + park), first version of the park_accessibility model
- code is mostly `.Rhistory` = console history of each session
