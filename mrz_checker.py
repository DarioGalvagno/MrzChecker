
import os
import streamlit as st
from mrz.generator.td3 import TD3CodeGenerator
from datetime import datetime

# Path to the logo image (use raw string notation)

# Set up the logo path
logo_path = os.path.expanduser(r"C:\Users\dario\OneDrive\Desktop\png-transparent-bass-player-icon-illustration-t-shirt-bass-guitar-bassist-fender-precision-bass-bass-guitar-text-logo-double-bass.png")

# Display the logo at the top of the page, centered
st.image(logo_path, width=150)



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
st.markdown("**Note:** Enter `N/A` if you do not have a middle name.")
first_name = st.text_input("First Name", "Enter the first name")
passport_number = st.text_input("Passport Number", "Enter the passport number")
nationality = st.selectbox("Nationality", COUNTRY_OPTIONS)

# Input fields for dates in DD/MM/YY format
birthdate_input = st.text_input("Date of Birth (DD/MM/YY)", "Enter a date")
expiration_date_input = st.text_input("Expiration Date (DD/MM/YY)", "Enter a date")

# Initialize variables
birthdate = None
expiration_date = None

# Convert dates to YYMMDD format for MRZ generation
try:
    if birthdate_input:
        birthdate = datetime.strptime(birthdate_input, "%d/%m/%y").strftime("%y%m%d")
    if expiration_date_input:
        expiration_date = datetime.strptime(expiration_date_input, "%d/%m/%y").strftime("%y%m%d")
except ValueError:
    st.error("Please enter the dates in the correct format (DD/MM/YY).")

gender = st.selectbox("Gender", GENDER_OPTIONS)

# Generate MRZ code when button is pressed
if st.button("Generate MRZ Code"):
    if issuing_country == "Select the country of issue" or nationality == "Select the nationality" or gender == "Select the gender":
        st.error("Please select a valid option for issuing country, nationality, and gender.")
    elif not birthdate or not expiration_date:
        st.error("Please enter valid dates for birthdate and expiration date.")
    else:
        try:
            # Create MRZ code
            code = TD3CodeGenerator(
                doc_type, issuing_country, surname, first_name + ' ' + middle_names, passport_number,
                nationality, birthdate, gender, expiration_date
            )
            # Display the MRZ code
            st.text("Generated MRZ Code:")
            st.code(str(code))
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.markdown("---")  # Adds a horizontal line
st.markdown('Created by [Dario Galvagno](https://www.your-link-here.com)')
