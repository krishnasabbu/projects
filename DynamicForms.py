import streamlit as st
import json
import os

# File to save and load form data
JSON_FILE = "forms_data.json"


# Load forms data from JSON file
def load_forms():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    return []


# Save forms data to JSON file
def save_forms(forms):
    with open(JSON_FILE, "w") as f:
        json.dump(forms, f, indent=4)


# Function to display forms
def display_form(form_data, form_id):
    with st.expander(f"Form {form_id + 1}", expanded=False):
        config_key = st.text_input(f"Config Key {form_id + 1}", value=form_data.get("Config Key", ""))
        config_value = st.text_input(f"Config Value {form_id + 1}", value=form_data.get("Config Value", ""))
        config_code = st.text_area(f"Config Code {form_id + 1}", value=form_data.get("Config Code", ""))

        name = st.checkbox(f"Name {form_id + 1}", value=form_data.get("Name", False))
        address = st.checkbox(f"Address {form_id + 1}", value=form_data.get("Address", False))
        dob = st.checkbox(f"DOB {form_id + 1}", value=form_data.get("DOB", False))

        return {
            "Config Key": config_key,
            "Config Value": config_value,
            "Config Code": config_code,
            "Name": name,
            "Address": address,
            "DOB": dob
        }


# Initialize or load forms
if "forms" not in st.session_state:
    st.session_state.forms = load_forms()

# Add a new form when the button is clicked
if st.button("Add Form"):
    st.session_state.forms.append({
        "Config Key": "",
        "Config Value": "",
        "Config Code": "",
        "Name": False,
        "Address": False,
        "DOB": False
    })

# Display all forms
for i, form_data in enumerate(st.session_state.forms):
    st.session_state.forms[i] = display_form(form_data, i)

# Save the forms data as JSON
if st.button("Save"):
    save_forms(st.session_state.forms)
    st.success("Data saved to forms_data.json")

# Optionally, display the JSON data
if st.checkbox("Show JSON Data"):
    st.write(json.dumps(st.session_state.forms, indent=1))
