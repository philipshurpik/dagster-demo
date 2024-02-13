import os
import json
import streamlit as st


DATA_DIR = 'data/clients_meta'


def send_data(company_name: str, competitors: list):
    data = {
        "company_name": company_name,
        "competitors": competitors
    }
    with open(f"{DATA_DIR}/{company_name}.json", "w") as file:
        json.dump(data, file)


if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    st.title("Demo")
    input_company = st.text_input("Company Name")
    input_competitors = st.text_input("Competitors")
    submit_button = st.button("Submit")
    if submit_button:
        competitors = [x.strip() for x in input_competitors.split(',')]
        send_data(input_company, competitors)
        st.success(f"Processing started: {input_company}  | {competitors}")
