import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # in case the file is zipped using gzip, provide the correct file extension
    if url.endswith(".csv.gz"):
        csv_name = "output.csv.gz"
    else:
        csv_name = "output.csv"

    # download csv file using wget, output saved in memory with name 'csv_name'
    os.system(f"wget {url} -O {csv_name}")

    # create engine using sqlalchemy ORM, connects to postgres instance
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    # create chunks of size 100,000 bytes
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    # collects the first chunk with variable name 'df'
    df = next(df_iter)

    # convert columns to datetime datatype
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # collect schema of file. df.head(n=0) returns no rows, only the header and column names
    # chain together .to_sql() to create table in postgres database with this schema
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")

    # adds first chunk of data to postgres database
    df.to_sql(name=table_name, con=engine, if_exists="append")

    while True:
        try:
            t_start = time()

            # collect next chunk to process
            df = next(df_iter)

            # convert columns to datetime datatype
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            # adds next chunk of data to postgres database
            df.to_sql(name=table_name, con=engine, if_exists="append")

            t_end = time()

            print("inserted another chunk, took %.3f second" % (t_end - t_start))

        # when next(df_iter) runs out of chunks to iterate over, then stop the loop
        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break


# when python file is invoked from command line, run the following code below
if __name__ == "__main__":
    # create helper class to add command line arguments with descriptions
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    # add arguments
    parser.add_argument("--user", required=True, help="user name for postgres")
    parser.add_argument("--password", required=True, help="password for postgres")
    parser.add_argument("--host", required=True, help="host for postgres")
    parser.add_argument("--port", required=True, help="port for postgres")
    parser.add_argument("--db", required=True, help="database name for postgres")
    parser.add_argument(
        "--table_name",
        required=True,
        help="name of the table where we will write the results to",
    )
    parser.add_argument("--url", required=True, help="url of the csv file")

    # parse configured arguments
    args = parser.parse_args()

    # pass arguments from cli to the main function
    main(args)
