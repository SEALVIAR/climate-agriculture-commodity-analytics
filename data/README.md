# Data Folder

This folder contains the datasets used in the project.

## Structure

| Folder | Description |
|---|---|
| `raw/` | Original data samples from Berkeley Earth, FAOSTAT and IMF |
| `interim/` | Auxiliary tables used during cleaning and mapping |
| `processed/` | Clean datasets generated after the ETL process |
| `warehouse/` | Exported dimension and fact tables from the Data Warehouse |

## Notes

The complete raw datasets are not fully included because some sources contain many files or large datasets.  
The project includes representative samples and the cleaned datasets used for the final analysis.

Main data sources:

- Berkeley Earth
- FAOSTAT
- IMF Primary Commodity Prices

Analysis period: 1990–2015.