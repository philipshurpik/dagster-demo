import os
import streamlit as st

from dagster_demo.utils import write_json

DATA_DIR = 'data/clients_meta'


def send_data(company_name: str, competitors: list):
    data = {
        "company_name": company_name,
        "competitors": competitors
    }
    write_json(f"{DATA_DIR}/{company_name}.json", data)


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
