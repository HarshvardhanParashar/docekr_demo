from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import re
import os

INPUT_FILE = "/opt/airflow/data/customers.csv"
OUTPUT_DIR = "/opt/airflow/data/output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_customers():
    df = pd.read_csv(INPUT_FILE)
    df.to_csv(f"{OUTPUT_DIR}/extracted.csv", index=False)
    print(f"Extracted {len(df)} records")

def validate_customers():
    df = pd.read_csv(f"{OUTPUT_DIR}/extracted.csv")

    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    valid_rows = []
    invalid_rows = []

    for _, row in df.iterrows():

        email_valid = bool(
            re.match(email_pattern, str(row["emails"]))
        )

        phone_valid = (
            len(str(row["phone"])) == 10
        )

        if email_valid and phone_valid:
            valid_rows.append(row)
        else:
            invalid_rows.append(row)

    pd.DataFrame(valid_rows).to_csv(
        f"{OUTPUT_DIR}/valid_customers.csv",
        index=False
    )

    pd.DataFrame(invalid_rows).to_csv(
        f"{OUTPUT_DIR}/invalid_customers.csv",
        index=False
    )

    print("Validation Complete")

def transform_customers():
    df = pd.read_csv(f"{OUTPUT_DIR}/valid_customers.csv")
    df["name"] = df["name"].str.upper()

    df.to_csv(
        f"{OUTPUT_DIR}/transformed_customers.csv",
        index=False
    )

print("Transformation Complete")


def generate_report():
    valid_df = pd.read_csv(
    f"{OUTPUT_DIR}/valid_customers.csv"
    )

    invalid_df = pd.read_csv(
    f"{OUTPUT_DIR}/invalid_customers.csv"
    )

    report = f"""

    ## Customer Pipeline Report

    Valid Records   : {len(valid_df)}
    Invalid Records : {len(invalid_df)}
    Total Records   : {len(valid_df)+len(invalid_df)}
    """


    with open(
        f"{OUTPUT_DIR}/summary_report.txt",
        "w"
    ) as file:
        file.write(report)

    print(report)

with DAG(
    dag_id="customer_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id="extract_customers",
        python_callable=extract_customers
    )

    validate_task = PythonOperator(
        task_id="validate_customers",
        python_callable=validate_customers
    )

    transform_task = PythonOperator(
        task_id="transform_customers",
        python_callable=transform_customers
    )

    report_task = PythonOperator(
        task_id="generate_report",
        python_callable=generate_report
    )

    extract_task >> validate_task >> transform_task >> report_task