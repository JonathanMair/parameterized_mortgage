"""tests for module: parameterized_mortgage.calcs"""
import parameterized_mortgage.calculate as calcs
from tests.dummy_data import *

import pandas as pd
from pathlib import Path
from decimal import Decimal

def test_monthly_repayment():
    result = calcs.monthly_payment(principal=value, rate=rate, term=term)
    assert round(result) == repayment

def test_repayment_schedule():
    p = Path(__file__).with_name("dummy_schedule.csv")
    with open(p, "r") as f:
        dummy = pd.read_csv(
            f, thousands=".", decimal=",", delimiter=";",
            names=["year", "month", "payment", "interest", "capital repayment", "balance"]
        ).astype(float)
    result = calcs.repayment_schedule(principal=value, rate=rate, term=term).round(2)
    result[["year", "month"]] = result[["year", "month"]].astype(float)
    assert result.equals(dummy)

def test_annual_summary():
    p = Path(__file__).with_name("dummy_schedule.csv")
    with open(p, "r") as f:
        dummy = pd.read_csv(
            f, thousands=".", decimal=",", delimiter=";",
            names=["year", "month", "payment", "interest", "capital repayment", "balance"]
        ).astype(float)
    dummy = dummy.groupby("year")
    dummy_summary = dummy[["payment", "interest", "capital repayment"]].sum()
    dummy_summary["balance"] = dummy["balance"].last()
    result = calcs.annual_summary(
        repayment_schedule=calcs.repayment_schedule(
            principal=value, rate=rate, term=term
        )
    )
    result.index = result.index.astype(float)
    result = result
    print("\n")
    print(dummy_summary)
    print("\n")
    print(result)
    assert result.equals(dummy_summary)



def test_lifetime_summary():
    p = Path(__file__).with_name("dummy_schedule.csv")
    with open(p, "r") as f:
        dummy = pd.read_csv(
            f, thousands=".", decimal=",", delimiter=";",
            names=["year", "month", "payment", "interest", "capital repayment", "balance"]
        ).astype(float)
    dummy = dummy.groupby("year")
    dummy_summary = dummy[["payment", "interest", "capital repayment"]].sum()
    dummy_summary["balance"] = dummy["balance"].last()
    dummy_lifetime = dummy_summary[["payment", "interest", "capital repayment"]].sum()
    result = calcs.annual_summary(
        repayment_schedule=calcs.repayment_schedule(
            principal=value, rate=rate, term=term
        )
    )
    result.index = result.index.astype(float)
    result = calcs.lifetime_summary(annual_summary=result)
    result = result.round(2)
    print("\n")
    print(dummy_lifetime)
    print("\n")
    print(result)
    assert result.equals(dummy_lifetime)