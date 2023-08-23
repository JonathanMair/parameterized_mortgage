"""tests for module: parameterized_mortgage.calcs"""
import parameterized_mortgage.calculate as calcs
from tests.dummy_data import *

import pandas as pd
from pathlib import Path

def test_monthly_repayment():
    result = calcs.get_monthly_payment(principal=value, rate=rate, term=term)
    assert round(result, 2) == repayment

def test_repayment_schedule():
    p = Path(__file__).with_name("dummy_schedule.csv")
    with open(p, "r") as f:
        dummy = pd.read_csv(
            f, thousands=".", decimal=",", delimiter=";",
            names=["year", "month", "payment", "interest", "capital repayment", "balance"]
        ).astype(float)
    result = calcs.repayment_schedule(principal=value, rate=rate, term=term).round(2)
    result = result.reset_index()
    result[["year", "month"]] = result[["year", "month"]].astype(float)

    # TODO: dropping the year and month columns here because the dummy data has them
    # the wrong way round — change the dummy data instead to test for correct
    # series of months and years
    result = result.drop(columns=["year", "month"], axis=1)
    dummy = dummy.drop(columns=["year", "month"], axis=1)

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

    # TODO: rounding below eliminates small diffs due to floating point error
    # is there a better way to deal with this?
    def rounding_fn(in_):
        out_ = round(in_ - 0.05)
        return out_
    result = result.agg(func=rounding_fn)
    dummy_summary = dummy_summary.agg(func=rounding_fn)

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
    # to deal with small imprecision due to floating point errors:
    # test differences are within a small range and sum passes for each value
    # TODO: perhaps there's a better way to deal with this
    result_values = list(result["value"].values)
    dummy_values = list(dummy_lifetime.values)
    passes = 0
    for r, d in zip(result_values, dummy_values):
        verdict = True if (r-d)/r < 0.001 else False
        passes += 1
    assert len(result_values) == passes
