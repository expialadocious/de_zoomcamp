import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import pandas as pd

    return duckdb, mo


@app.cell
def _(duckdb):
    con = duckdb.connect(r"path to duckdb database")

    # Query the taxi_rides dataset
    df = con.execute("SELECT * FROM taxi_rides.rides LIMIT 100").df()
    df
    return con, df


@app.cell
def _(con):
    # Question 1: What is the start date and end date of the dataset?

    con.execute(
        '''SELECT trip_pickup_date_time, trip_dropoff_date_time
            FROM taxi_rides.rides
            ORDER BY trip_pickup_date_time ASC, trip_dropoff_date_time DESC
            LIMIT 3;
        '''
    ).df()
    return


@app.cell
def _(con):
    con.execute(
        '''SELECT trip_pickup_date_time, trip_dropoff_date_time
            FROM taxi_rides.rides
            ORDER BY trip_dropoff_date_time DESC
            LIMIT 3;
        '''
    ).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Question 2: What proportion of trips are paid with credit card?
    """)
    return


@app.cell
def _(df):
    ## Question 2: What proportion of trips are paid with credit card?
    ## need 'payment_type' column

    df.head()
    return


@app.cell
def _(con):
    ### Claude Code syntax provided 

    con.execute("""
      SELECT payment_type,
             COUNT(*) AS count,
             ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct
      FROM taxi_rides.rides
      GROUP BY payment_type
      ORDER BY count DESC
    """).df()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Question 3: What is the total amount of money generated in tips?
    """)
    return


@app.cell
def _(df):
    df.head()

    ## need 'tip_amt' column
    return


@app.cell
def _(con):
    con.execute("""
      SELECT SUM(tip_amt) as total_tip,
      FROM taxi_rides.rides
    """).df()
    return


if __name__ == "__main__":
    app.run()
