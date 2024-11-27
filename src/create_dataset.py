import pandas as pd
import json
import os

def create_datasets_from_json(json_file):
    """
    Extract data from JSON and create datasets as Pandas DataFrames.
    """
    with open(json_file, "r") as file:
        data = json.load(file)

    guest_checks = pd.json_normalize(data["guestChecks"])
    detail_lines = pd.json_normalize(
        data["guestChecks"],
        record_path=["detailLines"],
        meta=["guestCheckId"],
        errors="ignore"
    )

    return guest_checks, detail_lines
