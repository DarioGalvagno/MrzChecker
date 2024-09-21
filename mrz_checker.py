import streamlit as st
from mrz.generator.td3 import TD3CodeGenerator
from datetime import datetime

# Streamlit app title
st.title("MRZ Code Generator")

# Define dropdown options with placeholders for issuing country, nationality, and gender
COUNTRY_OPTIONS = [
    "Select the country of issue", "AFG", "ALB", "DZA", "ASM", "AND", "AGO", "AIA", "ATA", "ATG", "ARG", "ARM", "ABW",
    "AUS", "AUT", "AZE", "BHS", "BHR", "BGD", "BRB", "BLR", "BEL", "BLZ", "BEN", "BMU", "BTN", "BOL", "BES", "BIH",
    "BWA", "BVT", "BRA", "IOT", "BRN", "BGR", "BFA", "BDI", "CPV", "KHM", "CMR", "CAN", "CYM", "CAF", "TCD", "CHL",
    "CHN", "CXR", "CCK", "COL", "COM", "COD", "COG", "COK", "CRI", "HRV", "CUB", "CUW", "CYM", "CZE", "CIV", "DNK",
    "DJI", "DMA", "DOM", "ECU", "EGY", "SLV", "GNQ", "ERI", "EST", "SWZ", "ETH", "FLK", "FRO", "FJI", "FIN", "FRA",
    "GUF", "PYF", "ATF", "GAB", "GMB", "GEO", "DEU", "GHA", "GIB", "GRC", "GRL", "GRD", "GLP", "GUM", "GTM", "GGY",
    "GIN", "GNB", "GUY", "HTI", "HMD", "VAT", "HND", "HKG", "HUN", "ISL", "IND", "IDN", "IRN", "IRQ", "IRL", "IMN",
    "ISR", "ITA", "JAM", "JPN", "JEY", "JOR", "KAZ", "KEN", "KIR", "PRK", "KOR", "KWT", "KGZ", "LAO", "LVA", "LBN",
    "LSO", "LBR", "LBY", "LIE", "LTU", "LUX", "MAC", "MDG", "MWI", "MYS", "MDV", "MLI", "MLT", "MHL", "MTQ", "MRT",
    "MUS", "MYT", "MEX", "FSM", "MDA", "MCO", "MNG", "MNE", "MSR", "MAR", "MOZ", "MMR", "NAM", "NRU", "NPL", "NLD",
    "NCL", "NZL", "NIC", "NER", "NGA", "NIU", "NFK", "MNP", "NOR", "OMN", "PAK", "PLW", "PSE", "PAN", "PNG", "PRY",
    "PER", "PHL", "PCN", "POL", "PRT", "PRI", "QAT", "MKD", "ROU", "RUS", "RWA", "REU", "BLM", "SHN", "KNA", "LCA",
    "MAF", "SPM", "VCT", "WSM", "SMR", "STP", "SAU", "SEN", "SRB", "SYC", "SLE", "SGP", "SXM", "SVK", "SVN", "SLB",
    "SOM", "ZAF", "SGS", "SSD", "ESP", "LKA", "SDN", "SUR", "SJM", "SWE", "CHE", "SYR", "TWN", "TJK", "TZA", "THA",
    "TLS", "TGO", "TKL", "TON", "TTO", "TUN", "TUR", "TKM", "TCA", "TUV", "UGA", "UKR", "ARE", "GBR", "UMI", "USA",
    "URY", "UZB", "VUT", "VEN", "VNM", "VGB", "VIR", "WLF", "ESH", "YEM", "ZMB", "ZWE", "ALA"
]

GENDER_OPTIONS = [
    "Select the gender", "M", "F", "X", "U"  # M for Male, F for Female, X for Non-binary/Other, U for Unknown
]

# Input fields for MRZ data
doc_type = st.text_input("Document Type", "P")
issuing_country = st.selectbox("Issuing Country", COUNTRY_OPTIONS)
surname = st.text_input("Last Name", "Enter the last name")
middle_names = st.text_input("Middle Name", "Enter the middle name")
st.markdown("<div style='background-color: lightyellow; color: red; padding: 10px;'><strong>Note:</strong> "
            "Leave the field blank if you do not have a middle name.</div>", unsafe_allow_html=True)
first_name = st.text_input("First Name", "Enter the first name")
passport_number = st.text_input("Passport Number", "Enter the passport number")
nationality = st.selectbox("Nationality", COUNTRY_OPTIONS)

# Use date_input for date of birth with range (1930-2020)
birthdate_input = st.date_input(
    "Date of Birth",
    value=datetime(1990, 1, 1),
    min_value=datetime(1930, 1, 1),
    max_value=datetime(2020, 12, 31)
)

# Use date_input for expiration date with range (2020-2150)
expiration_date_input = st.date_input(
    "Expiration Date",
    value=datetime(2030, 1, 1),
    min_value=datetime(2020, 1, 1),
    max_value=datetime(2150, 12, 31)
)

# Convert dates to YYMMDD format for MRZ generation
birthdate = birthdate_input.strftime("%y%m%d")
expiration_date = expiration_date_input.strftime("%y%m%d")

gender = st.selectbox("Gender", GENDER_OPTIONS)

# Generate MRZ code when button is pressed
if st.button("Generate MRZ Code"):
    if issuing_country == "Select the country of issue" or nationality == "Select the nationality" or gender == "Select the gender":
        st.error("Please select a valid option for issuing country, nationality, and gender.")
    else:
        try:
            # Create MRZ code
            code = TD3CodeGenerator(
                doc_type, issuing_country, surname, first_name + ' ' + middle_names, passport_number,
                nationality, birthdate, gender, expiration_date
            )
            # Highlight MRZ code up to expiration date
            code_str = str(code)
            expiration_idx = code_str.find(expiration_date)
            highlighted_code = (
                f"<span style='background-color: yellow;'>{code_str[:expiration_idx + len(expiration_date)]}</span>"
                f"{code_str[expiration_idx + len(expiration_date):]}"
            )

            # Display the MRZ code with highlighted portion
            st.text("Generated MRZ Code:")
            st.markdown(highlighted_code, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")

        # Horizontal line
        st.markdown("---")

        # Display your name properly
        st.write("Created by **Dario Galvagno**")