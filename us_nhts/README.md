# us_nhts (R + Python inside Rmd)

- NHTS 2017, tours of adults in households with a child under 10
- outcome: child on all trips / some trips / no trips of the tour (43,954 tours)
- order: `us_data_processing_1` → `us_var_setting_1` → `us_variable_breakdown` → models
- models (Biogeme): mixed logit (`us_mixed_chisq_sim_1`), by purpose (`_bypurp`), interaction logit (`us_interaction_chisq_sim_1`, latest Jul 20)
- `.html` = Biogeme reports (`Interaction_US~36` = last run)
- files without `_1` = older versions
