# Climate, Agriculture \& Commodity Analytics

This project was developed as a final Business Analytics project.  
The main goal was to integrate climate, agricultural production and commodity price data to understand how climate variations may relate to agriculture and global market behavior.

The project includes data extraction and cleaning, a Data Warehouse in PostgreSQL, Power BI dashboards, basic machine learning models and a small AI agent for exploring the data using natural language.

## Data Sources

The project uses three public data sources:

* **Berkeley Earth**: historical temperature data by country.
* **FAOSTAT**: agricultural production data by country, crop and year.
* **IMF / Pinky Rose**: international commodity price data.

The analysis focuses on the period **1990–2015**, because it allowed the three sources to be compared within a common time range.

## What We Built

* ETL process using Python and KNIME.
* Clean datasets ready for analysis.
* A PostgreSQL Data Warehouse using a constellation schema.
* SQL scripts to create and validate the database.
* Power BI dashboards to explore climate, agriculture and commodity prices.
* Machine learning models using OLS regression and Random Forest.
* A simple AI agent using LangChain to ask questions about the consolidated data.

## Main Results

Some of the main findings were:

* Agricultural yield was one of the indicators most related to climate conditions.
* Some commodities, such as maize and cocoa, showed higher price volatility during periods of thermal stress.
* The relationship between climate and agricultural production was not the same for all countries.
* Absolute temperature showed stronger predictive value than short-term temperature anomalies in some models.

## Repository Structure



| Folder | Description |

|---|---|

| `data/` | Clean datasets |

| `docs/` | Final report and documentation |

| `images/` | Dashboard screenshots and diagrams |

| `knime/` | KNIME workflow |

| `notebooks/` | Python analysis and machine learning notebooks |

| `powerbi/` | Power BI dashboard file |

| `sql/` | Data Warehouse SQL scripts |

| `src/etl/` | Python ETL scripts |



## Tools Used

* DBeaver
* KNIME
* LangChain
* Pandas
* PostgreSQL
* Power BI
* Python
* Scikit-learn
* SQL

## Authors

* Sergio Alejandro Villada Arias
* Julián David Aranzazu Velásquez

Final project for the Business Analytics course.
Universidad Nacional de Colombia.

