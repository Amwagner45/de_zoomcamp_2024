-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `dezoomcamp2024-412618.zoomcamp.nytaxi_external_green_nytaxi_data`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp2024-412618_mage_demo/nyc_taxi_data/green_tripdata_2022-*.parquet']
);

-- Count how many records in the external table
select count(*) as count
from `dezoomcamp2024-412618.zoomcamp.nytaxi_external_green_nytaxi_data`;

-- Create Materialized table
CREATE OR REPLACE TABLE `dezoomcamp2024-412618.zoomcamp.nytaxi_external_green_nytaxi_data_non_partitioned` AS
SELECT * FROM `dezoomcamp2024-412618.zoomcamp.nytaxi_external_green_nytaxi_data`;

-- Compare how much resources used for External table vs Materialized, non-partitioned table. 
-- 0MB for External table
-- 6.41MB for Materialized table
select distinct PULocationID
from `dezoomcamp2024-412618.zoomcamp.nytaxi_external_green_nytaxi_data`;

select distinct PULocationID
from `dezoomcamp2024-412618.zoomcamp.nytaxi_external_green_nytaxi_data_non_partitioned`;

-- How many records have a fare_amount = 0?
select count(*) as count
from `dezoomcamp2024-412618.zoomcamp.nytaxi_external_green_nytaxi_data`
where fare_amount = 0
limit 10;

-- Create partitioned and clustered table
CREATE OR REPLACE TABLE `dezoomcamp2024-412618.zoomcamp.nytaxi_external_green_nytaxi_data_partitioned_and_clustered`
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PUlocationID AS
SELECT * FROM `dezoomcamp2024-412618.zoomcamp.nytaxi_external_green_nytaxi_data`;

-- Compare performance between Materialized table vs Partitioned and Clustered table
-- Materialized
-- 12.82MB
select distinct PULocationID
from `dezoomcamp2024-412618.zoomcamp.nytaxi_external_green_nytaxi_data_non_partitioned`
where lpep_pickup_datetime between '2022-06-01' and '2022-06-30';

-- Partitioned and Clustered 
-- 1.12MB
select distinct PULocationID
from `dezoomcamp2024-412618.zoomcamp.nytaxi_external_green_nytaxi_data_partitioned_and_clustered`
where lpep_pickup_datetime between '2022-06-01' and '2022-06-30';

-- Bonus: how much resources does a count(*) use on Materialized table?
-- 0MB because this data can be retrieved using metadata stored in BigQuery table. No need to query data in the table and count all rows.
select count(*) as count
from `dezoomcamp2024-412618.zoomcamp.nytaxi_external_green_nytaxi_data_non_partitioned`;
