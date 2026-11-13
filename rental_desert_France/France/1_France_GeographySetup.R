#Rental Deserts Working Paper 041824
#first script:0_GeographySetUp
#This code creates the geographic crosswalk for the rental deserts dataset
#The resulting file gives the tract, the cbsa it is in, and the urban/suburban classification: tracts_cbsas_suburbs_2022.csv

#LOAD LIBRARIES------
install.packages(c("sf", "dplyr"))
install.packages("tidyverse")
library(tidyverse)
library(sf)
library(dplyr)

#UPDATE SETTINGS AND FILE PATH------
#file path 
filepath_data <- "/Users/ohdaw/OneDrive/Documents/R_Projects/rental_desert/France/France_IRIS/" 

# Load the shapefile (adjust the path if necessary)
france_tracts_shp <- st_read("C:/Users/ohdaw/OneDrive/Documents/R_Projects/rental_desert/France/France_maps/com_uu2020_2024/com_uu2020_2024.shp")

# Load the CSV file containing additional data
france_tracts <- read.csv("C:/Users/ohdaw/OneDrive/Documents/R_Projects/rental_desert/France/France_maps/France_MunicipalComposition.csv")



# Join the shapefile data with the CSV data on the common 'codegeo' column
# Assuming 'codegeo' is named the same in both datasets; if not, adjust accordingly
france_tracts <- france_tracts_shp %>%
  left_join(france_tracts, by = c("codgeo" = "codgeo"))

# Drop the redundant columns and keep only the unique ones
france_tracts <- france_tracts %>%
  select(-ends_with(".x")) %>%
  # Optionally, rename columns to remove the .x suffix if needed
  rename_with(~ gsub("\\.y$", "", .))

# Categorize places as city or suburban based on the columns 'UU2020' and 'statut_com_uu'
france_tracts <- france_tracts %>%
  mutate(
    # Define municipality status based on statut_com_uu
    municipality_status = case_when(
      statut_com_uu == "H" ~ "Outside urban unit",
      statut_com_uu == "C" ~ "Central city",
      statut_com_uu == "B" ~ "Suburb",
      statut_com_uu == "I" ~ "Isolated city",
      TRUE ~ "Unknown"
    ),
    # Determine if place is city or suburb based on status
    city = if_else(municipality_status == "Central city", 1, 0),
    suburb = if_else(municipality_status == "Suburb", 1, 0)
  )

# Select relevant columns
france_tracts <- france_tracts %>%
  select(codgeo, libgeo, dep, reg, municipality_status, city, suburb, geometry)

# CATEGORIZE TRACTS AS URBAN/RURAL ----
# Since France does not use CBSAs, we’ll use urban/rural status at the commune level.
# Assume communes outside urban units are rural.

france_tracts <- france_tracts %>%
  mutate(
    rural = if_else(municipality_status == "Outside urban unit", 1, 0)
  )

# Summary of classification
summary(france_tracts)

# Save the processed data (if needed)
# st_write(france_tracts, "C:/path/to/save/processed_france_places.shp")



#########



# Load the shapefile for French urban units
france_cbsa_shp <- st_read("C:/Users/ohdaw/OneDrive/Documents/R_Projects/rental_desert/France/France_maps/uu2020_2024/uu2020_2024.shp")

# Load the CSV for French population data
france_cbsa <- read.csv("C:/Users/ohdaw/OneDrive/Documents/R_Projects/rental_desert/France/France_maps/France_UrbanUnit.csv")

# Join the shapefile and population data on the common 'UU2020' column
france_cbsa <- france_cbsa %>%
  left_join(france_cbsa_shp, by = "uu2020")
# Drop the redundant columns and keep only the unique ones
france_cbsa <- france_cbsa %>%
  select(-ends_with(".y")) %>%
  # Optionally, rename columns to remove the .x suffix if needed
  rename_with(~ gsub("\\.x$", "", .))

# Join the shapefile data with the CSV data on the common 'uu2020' column
# Assuming 'uu2020' is named the same in both datasets; if not, adjust accordingly
france_units <- france_tracts %>%
  left_join(france_cbsa, by = c("uu2020" = "uu2020"))
# Drop the redundant columns and keep only the unique ones
france_units <- france_units %>%
  select(-ends_with(".y")) %>%
  # Optionally, rename columns to remove the .x suffix if needed
  rename_with(~ gsub("\\.x$", "", .))


# Define city and suburb status based on population range (e.g., 100,000 or more for cities)
france_units <- france_units %>%
  mutate(
    # Define city status based on population size range
    popcity = if_else(TUU2017 == 7 | TUU2017 == 8, 1, 0),  # Urban unit with 100,000+ inhabitants or Paris
    city = if_else(popcity == 1, 1, 0),  # Mark as city
    suburb = if_else(city == 1, 0, 1)  # Mark as suburb if not a city
  )

# Assuming you want to assign city/suburb status to tracts
# Create centroid layer for tracts 
france_units$centroid <- st_centroid(france_units$geometry)  


# Rank urban units based on their population sizes and filter the top categories
france_units_pop <- france_units %>%
  mutate(
    # Classify urban units by population size categories
    pop_category = case_when(
      TDUU2017 == 71 ~ "200,000 to 299,999",
      TDUU2017 == 72 ~ "300,000 to 499,999",
      TDUU2017 == 73 ~ "500,000 to 1,999,999",
      TDUU2017 == 80 ~ "Paris",
      TRUE ~ "Other"
    )
  ) %>%
  # Rank urban units by population size category
  mutate(
    pop_rank = case_when(
      pop_category == "200,000 to 299,999" ~ 1,
      pop_category == "300,000 to 499,999" ~ 2,
      pop_category == "500,000 to 1,999,999" ~ 3,
      pop_category == "Paris" ~ 4,
      TRUE ~ NA_real_  # For other cases, assign NA
    ),
    # Add a flag for top population categories (500,000 to 1,999,999 and Paris)
    pop_top = if_else(pop_category %in% c("500,000 to 1,999,999", "Paris"), 1, 0)
  )##There are 154 500,000 to 1,999,999 and 1 Paris
