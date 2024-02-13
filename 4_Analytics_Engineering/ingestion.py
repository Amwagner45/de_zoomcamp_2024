import duckdb


def collect_urls(year: str, color: str):
    for month in range(1, 13):
        if month < 10:
            month = "0" + str(month)
        else:
            month

        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-{month}.parquet"

        print(url)


def create_table(conn, color, year):
    conn.execute(
        f""" create or replace table {color}_tripdata_{year} as 
            SELECT * FROM read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-01.parquet')
            union all
            SELECT * FROM read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-02.parquet')
            union all
            SELECT * FROM read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-03.parquet')
            union all
            SELECT * FROM read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-04.parquet')
            union all
            SELECT * FROM read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-05.parquet')
            union all
            SELECT * FROM read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-06.parquet')
            union all
            SELECT * FROM read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-07.parquet')
            union all
            SELECT * FROM read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-08.parquet')
            union all
            SELECT * FROM read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-09.parquet')
            union all
            SELECT * FROM read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-10.parquet')
            union all
            SELECT * FROM read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-11.parquet')
            union all
            SELECT * FROM read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-12.parquet')
            ;
        """
    )


conn = duckdb.connect(database="ny_taxi.db", read_only=False)
create_table(conn, "fhv", "2019")

conn.execute("show tables;")
print(conn.fetchall())

conn.execute("select * from fhv_tripdata_2019 limit 10;")
print(conn.fetchone())
