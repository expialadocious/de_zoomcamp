# **Week 3 Homework Notes and Queries**
# NOTE: Italicized words are generic naming used in place of actual private BigQuery variables

##1 Begin by using modified Kestra Flow to backfill load NY Taxi data in parquet format into GCP Bucket
  CRON Trigger dates for yellow taxi data orchestration is set for the first of every month at 10am
  Backfill load 2023-12-31 10:00:00 to 2024-06-02 10:00:00 to capture January 2024 to June 2024 parquet files.
  See Kestra Yaml Flow file "09_gcp_taxi_scheduled"

##2 Login to GCP Console and create Dataset in BigQuery
    '''SQL
    CREATE SCHEMA *dataset*
OPTIONS(
  location= "us-west1"
);
'''

##3 Create External table in BigQuery
  Use all parquet files extracted by Kestra Flow and uploaded into GCP Bucket
  '''SQL
    
CREATE OR REPLACE EXTERNAL TABLE *dataset.ny_taxi_ext*
OPTIONs (
format = 'PARQUET',
uris = ['gs://*bucketname*/*.parquet']
);
'''

##4 See Schema of external table and use in Regular Table creation in BigQuery
  '''SQL
SELECT
  column_name,
  data_type,
  is_nullable
FROM *dataset*.INFORMATION_SCHEMA.COLUMNS
WHERE table_name = 'ny_taxi_ext'
ORDER BY ordinal_position;
'''
Extracted schema used when creating regular table 

##5 Create Regular Table in BigQuery (uses BigQuery storage)

Create Empty Table:

''''SQL
CREATE OR REPLACE TABLE *dataset*.ny_taxi
(
  VendorID	INT64,	
  tpep_pickup_datetime	TIMESTAMP,	
	tpep_dropoff_datetime	TIMESTAMP,	
	passenger_count	INT64,	
	trip_distance	FLOAT64,	
	RatecodeID	INT64,	
	store_and_fwd_flag	STRING,	
	PULocationID	INT64,	
	DOLocationID	INT64,	
	payment_type	INT64,	
	fare_amount	FLOAT64,	
	extra	FLOAT64,	
	mta_tax	FLOAT64,	
	tip_amount	FLOAT64,	
	tolls_amount	FLOAT64,	
	improvement_surcharge	FLOAT64,	
	total_amount	FLOAT64,	
	congestion_surcharge	FLOAT64,	
	Airport_fee	FLOAT64 
)
'''

Load Values from External Table into Regular Table:

'''SQL
CREATE OR REPLACE TABLE *dataset*.ny_taxi AS
SELECT * FROM datasethmwk3.ny_taxi_ext;
'''

##6 See how estimated Bytes that will be processed to run a SELECT COUNT(*) Query in External Table and Regular Table

Both Queries will process 0 Bytes since BigQuery can derive the amount usign the metadata on each table (no Scans throughout the tables are necessary)

'''SQL
SELECT COUNT(*)
FROM *dataset*.ny_taxi;

##7 See Columnar Storage Effects on Bytes used when returning queries with 1 entire column and then with 2 entire columns
    Bytes processed doubled since BigQuery will process the query in columnar fashion and will scan both columns

'''SQL
SELECT PULocationID, DOLocationID
 FROM *dataset*.ny_taxi;

 ##8 Query count of rows where fare = $0

 '''SQL
 SELECT COUNT(*)
FROM *dataset*.ny_taxi
WHERE fare_amount = 0;
'''
##8 Compare Bytes Usage when using filter predicate on datetime column between partitioned and non-partitioned tables

Create new table with a partition on datetime. Table will contain all rows and columns of regular non-partitioned table:
'''SQL
CREATE OR REPLACE TABLE *dataset*.ny_taxi_partition
PARTITION BY DATE(tpep_dropoff_datetime)
AS
SELECT * FROM *dataset*.ny_taxi;
'''
Query using partition on a specific datetime range and note how many bytes were used:
'''SQL
SELECT DISTINCT(VendorID)
FROM *dataset*.ny_taxi_partition
WHERE tpep_dropoff_datetime >= '2024-03-01'
AND tpep_dropoff_datetime < '2024-03-16';
'''

Query non-partitioned table on same specific datetime range and note how many bytes were used:
'''SQL
SELECT DISTINCT VendorID
FROM *dataset*.ny_taxi
WHERE tpep_dropoff_datetime >= '2024-03-01' 
AND tpep_dropoff_datetime < '2024-03-16';
'''
NOTE: the partitioned table used significantly less bytes









