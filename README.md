# Serverless Retail Data Pipeline on AWS

An event-driven ETL pipeline that ingests raw retail transaction data,
cleans and transforms it automatically, and makes it queryable for
analytics. Built on AWS using S3, Lambda, Glue, and Athena.

![Architecture](architecture.png)

## What it does
Dropping a CSV into an S3 bucket triggers a Lambda function that cleans
the data with Pandas, writes it back to S3 as partitioned Parquet, and
registers it in the AWS Glue Data Catalog. The cleaned data is then
queried with SQL in Amazon Athena.

## Dataset
[Online Retail II (UCI)](https://archive.ics.uci.edu/dataset/502/online+retail+ii),
~1M transactions from a UK online retailer, 2009 to 2011. Licensed CC BY 4.0.

## Pipeline
1. Ingest: raw CSV lands in S3 (`raw/`).
2. Transform: an S3 event triggers Lambda, which removes cancellations,
   missing customer IDs, and invalid rows, then adds revenue and
   year-month columns. Kept [rows_out] of [rows_in] rows after cleaning.
3. Store: cleaned data written to S3 as partitioned Parquet, cataloged in Glue.
4. Analyze: queried in Athena with SQL.

## Key results
After cleaning, the pipeline retained 779,425 valid transactions from
5,878 unique customers, representing about $17.4M in revenue across
2009 to 2011.

- **Revenue peaked in November 2010** at roughly $1.16M, well above the
  monthly average, likely driven by pre-holiday wholesale ordering.
- **The UK was the home market, but the strongest export markets were
  EIRE (Ireland) and the Netherlands**, each above $550K, followed by
  Germany and France.
- **Top products were giftware and homeware**, led by the Regency
  Cakestand 3 Tier and the White Hanging Heart T-Light Holder, pointing
  to a clear bestseller concentration rather than evenly spread sales.
- Cleaning removed roughly 25% of raw rows (cancellations, missing
  customer IDs, and invalid quantities or prices), which materially
  changed the revenue picture and shows why the transform step matters.

## Tech
AWS S3, AWS Lambda (Python 3.12), AWS Glue Data Catalog, Amazon Athena,
Pandas, AWS SDK for pandas.

## What I learned
[2 to 3 honest sentences: event-driven design, why Parquet and
partitioning lower query cost, the least-privilege IAM tradeoff.]

## Notes
IAM permissions are broad here for learning; in production they would be
scoped to this single bucket and database.
