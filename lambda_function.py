import os
import pandas as pd
import awswrangler as wr


def lambda_handler(event, context):
    # 1. Figure out which file triggered this run
    record = event["Records"][0]["s3"]
    bucket = record["bucket"]["name"]
    key = record["object"]["key"]
    input_path = f"s3://{bucket}/{key}"

    database = os.environ["GLUE_DATABASE"]
    table = os.environ["GLUE_TABLE"]
    output_path = f"s3://{bucket}/processed/"

    # 2. Read the raw CSV (ISO-8859-1 handles the British pound symbol)
    df = wr.s3.read_csv(input_path, encoding="ISO-8859-1")

    # 3. Standardize column names: lowercase, underscores
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    # now: invoice, stockcode, description, quantity, invoicedate, price, customer_id, country

    rows_before = len(df)

    # 4. Clean the data
    df["invoicedate"] = pd.to_datetime(df["invoicedate"], errors="coerce")
    df = df.dropna(subset=["customer_id"])                                # drop rows with no customer
    df = df[~df["invoice"].astype(str).str.upper().str.startswith("C")]   # drop cancellations
    df = df[(df["quantity"] > 0) & (df["price"] > 0)]                     # keep valid sales only
    df = df.dropna(subset=["invoicedate"])                                # drop unparseable dates
    df = df.drop_duplicates()

    # 5. Add useful columns
    df["revenue"] = df["quantity"] * df["price"]
    df["year_month"] = df["invoicedate"].dt.to_period("M").astype(str)
    df["customer_id"] = df["customer_id"].astype("Int64").astype(str)

    rows_after = len(df)

    # 6. Write clean data to S3 as Parquet AND register the table, in one call
    wr.s3.to_parquet(
        df=df,
        path=output_path,
        dataset=True,
        database=database,
        table=table,
        mode="overwrite",
        partition_cols=["year_month"],
    )

    result = {
        "rows_in": rows_before,
        "rows_out": rows_after,
        "dropped": rows_before - rows_after,
        "message": f"Wrote clean data to {output_path} and registered {database}.{table}",
    }
    print(result)   # this shows up in CloudWatch logs
    return result