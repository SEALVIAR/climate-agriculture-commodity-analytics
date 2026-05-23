"""
Geographic standardization between FAOSTAT and Berkeley Earth country names.

This script compares country names from FAOSTAT with Berkeley Earth country names.
It identifies exact matches, applies manually validated mappings, and generates
fuzzy matching candidates for additional manual review.

Expected input:
    - FAOSTAT CSV file with an "Area" column.

Generated outputs:
    - country_exact_matches.csv
    - country_manual_matches.csv
    - country_fuzzy_candidates.csv
    - berkeley_countries_to_download.csv
"""

from pathlib import Path
import argparse

import pandas as pd
from rapidfuzz import fuzz, process


BERKELEY_COUNTRIES = {
    "Afghanistan", "Albania", "Algeria", "American Samoa", "Andorra", "Angola",
    "Anguilla", "Antarctica", "Antigua and Barbuda", "Argentina", "Armenia",
    "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
    "Baker Island", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize",
    "Benin", "Bhutan", "Bolivia", "Bonaire, Saint Eustatius and Saba",
    "Bosnia And Herzegovina", "Botswana", "Brazil", "British Virgin Islands",
    "Bulgaria", "Burkina Faso", "Burma", "Burundi", "Cambodia", "Cameroon",
    "Canada", "Cape Verde", "Cayman Islands", "Central African Republic",
    "Chad", "Chile", "China", "Christmas Island", "Colombia", "Congo",
    "Congo (Democratic Republic of the)", "Costa Rica", "Croatia", "Cuba",
    "Cyprus", "Czech Republic", "Denmark (Europe)", "Djibouti", "Dominica",
    "Dominican Republic", "Ecuador", "Egypt", "El Salvador",
    "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia",
    "Falkland Islands (Islas Malvinas)", "Faroe Islands",
    "Federated States of Micronesia", "Fiji", "Finland", "France",
    "France (Europe)", "French Guiana", "French Polynesia",
    "French Southern and Antarctic Lands", "Gabon", "Gambia", "Gaza Strip",
    "Georgia", "Germany", "Ghana", "Greece", "Greenland", "Grenada",
    "Guadeloupe", "Guam", "Guatemala", "Guernsey", "Guinea",
    "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "India",
    "Indonesia", "Iran", "Iraq", "Ireland", "Isle of man", "Israel", "Italy",
    "Jamaica", "Japan", "Jersey", "Jordan", "Kazakhstan", "Kenya", "Kuwait",
    "Kyrgyzstan", "Laos", "Lebanon", "Lesotho", "Liberia", "Libya",
    "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia",
    "Madagascar", "Malawi", "Malaysia", "Mali", "Malta", "Mauritania",
    "Mauritius", "Mayotte", "Mexico", "Monaco", "Mongolia", "Montenegro",
    "Morocco", "Mozambique", "Namibia", "Nepal", "Netherlands",
    "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "Norway",
    "Oman", "Pakistan", "Palestina", "Panama", "Paraguay", "Peru",
    "Philippines", "Poland", "Portugal", "Puerto Rico", "Qatar", "Reunion",
    "Romania", "Russia", "Rwanda", "San Marino", "Saudi Arabia", "Senegal",
    "Serbia", "Singapore", "Slovakia", "Slovenia", "Somalia", "South Africa",
    "South Korea", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden",
    "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand",
    "Tunisia", "Turkey", "Uganda", "Ukraine", "United Arab Emirates",
    "United Kingdom (Europe)", "United States", "Uruguay", "Uzbekistan",
    "Venezuela", "Virgin Islands", "Vietnam", "Yemen", "Zambia", "Zimbabwe",
}


MANUAL_COUNTRY_MAPPING = {
    "Bosnia and Herzegovina": "Bosnia And Herzegovina",
    "Bolivia (Plurinational State of)": "Bolivia",
    "Cabo Verde": "Cape Verde",
    "Czechia": "Czech Republic",
    "Denmark": "Denmark (Europe)",
    "Iran (Islamic Republic of)": "Iran",
    "Lao People's Democratic Republic": "Laos",
    "North Macedonia": "Macedonia",
    "Netherlands (Kingdom of the)": "Netherlands",
    "Palestine": "Palestina",
    "Türkiye": "Turkey",
    "Russian Federation": "Russia",
    "Syrian Arab Republic": "Syria",
    "United Republic of Tanzania": "Tanzania",
    "United States of America": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom (Europe)",
    "Viet Nam": "Vietnam",
    "Venezuela (Bolivarian Republic of)": "Venezuela",
    "Micronesia (Federated States of)": "Federated States of Micronesia",
    "Democratic Republic of the Congo": "Congo (Democratic Republic of the)",
    "Réunion": "Reunion",
}


def compare_country_names(source_countries, target_countries, threshold=70):
    """
    Compare country names using fuzzy matching.

    Parameters
    ----------
    source_countries : set
        Country names from FAOSTAT.
    target_countries : set
        Country names from Berkeley Earth.
    threshold : int
        Minimum similarity score required to keep a candidate match.

    Returns
    -------
    pandas.DataFrame
        Candidate matches with confidence scores.
    """
    matches = []

    for source_country in sorted(source_countries):
        best_match = process.extractOne(
            source_country,
            target_countries,
            scorer=fuzz.token_sort_ratio
        )

        if best_match is None:
            continue

        target_country, score, _ = best_match

        if score >= threshold:
            matches.append({
                "faostat_country": source_country,
                "berkeley_country": target_country,
                "confidence_score": score,
                "match_type": "fuzzy_candidate"
            })

    return pd.DataFrame(matches)


def load_faostat_countries(faostat_path):
    """
    Load unique country names from the FAOSTAT Area column.
    """
    data = pd.read_csv(faostat_path)

    if "Area" not in data.columns:
        raise ValueError("The FAOSTAT file must contain an 'Area' column.")

    countries = set(data["Area"].dropna().astype(str).unique())
    return countries


def build_exact_matches(faostat_countries, berkeley_countries):
    """
    Identify countries with the same name in both datasets.
    """
    exact_countries = faostat_countries.intersection(berkeley_countries)

    return pd.DataFrame({
        "faostat_country": sorted(exact_countries),
        "berkeley_country": sorted(exact_countries),
        "confidence_score": 100,
        "match_type": "exact"
    })


def build_manual_matches(faostat_countries, berkeley_countries):
    """
    Apply manually validated country name mappings.
    """
    records = []

    for faostat_country, berkeley_country in MANUAL_COUNTRY_MAPPING.items():
        if faostat_country in faostat_countries and berkeley_country in berkeley_countries:
            records.append({
                "faostat_country": faostat_country,
                "berkeley_country": berkeley_country,
                "confidence_score": 100,
                "match_type": "manual"
            })

    return pd.DataFrame(records)


def main():
    parser = argparse.ArgumentParser(
        description="Standardize country names between FAOSTAT and Berkeley Earth."
    )

    parser.add_argument(
        "--faostat-path",
        required=True,
        help="Path to the FAOSTAT CSV file."
    )

    parser.add_argument(
        "--output-dir",
        default="data/processed",
        help="Directory where output CSV files will be saved."
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=70,
        help="Minimum fuzzy matching score."
    )

    args = parser.parse_args()

    faostat_path = Path(args.faostat_path)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    faostat_countries = load_faostat_countries(faostat_path)
    berkeley_countries = BERKELEY_COUNTRIES

    exact_matches = build_exact_matches(faostat_countries, berkeley_countries)
    manual_matches = build_manual_matches(faostat_countries, berkeley_countries)

    matched_faostat_countries = set(exact_matches["faostat_country"]).union(
        set(manual_matches["faostat_country"])
    )

    matched_berkeley_countries = set(exact_matches["berkeley_country"]).union(
        set(manual_matches["berkeley_country"])
    )

    unmatched_faostat = faostat_countries.difference(matched_faostat_countries)
    unmatched_berkeley = berkeley_countries.difference(matched_berkeley_countries)

    fuzzy_candidates = compare_country_names(
        unmatched_faostat,
        unmatched_berkeley,
        threshold=args.threshold
    )

    exact_matches.to_csv(output_dir / "country_exact_matches.csv", index=False)
    manual_matches.to_csv(output_dir / "country_manual_matches.csv", index=False)
    fuzzy_candidates.to_csv(output_dir / "country_fuzzy_candidates.csv", index=False)

    all_valid_berkeley_countries = pd.concat(
        [
            exact_matches[["berkeley_country"]],
            manual_matches[["berkeley_country"]],
        ],
        ignore_index=True
    ).drop_duplicates()

    all_valid_berkeley_countries = all_valid_berkeley_countries.rename(
        columns={"berkeley_country": "country"}
    )

    all_valid_berkeley_countries.to_csv(
        output_dir / "berkeley_countries_to_download.csv",
        index=False
    )

    print("Geographic standardization completed.")
    print(f"FAOSTAT countries: {len(faostat_countries)}")
    print(f"Berkeley countries: {len(berkeley_countries)}")
    print(f"Exact matches: {len(exact_matches)}")
    print(f"Manual matches: {len(manual_matches)}")
    print(f"Fuzzy candidates for review: {len(fuzzy_candidates)}")
    print(f"Outputs saved in: {output_dir}")


if __name__ == "__main__":
    main()
