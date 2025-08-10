# Data Dictionary

| Column                  | Type      | Constraints                        | Example         | Description                                 |
|-------------------------|-----------|------------------------------------|-----------------|---------------------------------------------|
| vendor_id               | string    | {"VTS", "CMT"}                     | VTS             | Taxi company code                           |
| tpep_pickup_datetime    | datetime  | not null                           | 2024-01-01 00:01:00 | Trip pickup timestamp                  |
| tpep_dropoff_datetime   | datetime  | not null                           | 2024-01-01 00:12:00 | Trip dropoff timestamp                 |
| passenger_count         | int       | 0 <= x <= 8                        | 1               | Number of passengers                        |
| trip_distance           | float     | 0 <= x <= 200                      | 2.1             | Trip distance in miles                      |
| rate_code_id            | int       | 1–6                                | 1               | Rate code                                   |
| store_and_fwd_flag      | bool      | {"Y", "N"}                         | N               | Store and forward flag                      |
| pu_location_id          | int       | >0                                 | 142             | Pickup location ID                          |
| do_location_id          | int       | >0                                 | 236             | Dropoff location ID                         |
| payment_type            | int       | 1–6                                | 1               | Payment type code                           |
| fare_amount             | float     | >=0                                | 9.5             | Fare amount                                 |
| extra                   | float     | >=0                                | 0.5             | Extra charges                               |
| mta_tax                 | float     | >=0                                | 0.5             | MTA tax                                     |
| tip_amount              | float     | >=0                                | 2.0             | Tip amount                                  |
| tolls_amount            | float     | >=0                                | 0.0             | Tolls amount                                |
| improvement_surcharge   | float     | >=0                                | 0.3             | Improvement surcharge                       |
| total_amount            | float     | >=0, <=1000                        | 12.8            | Total amount                                |
| congestion_surcharge    | float     | >=0                                | 2.5             | Congestion surcharge                        |

## Notes

- All timestamps are in local NYC time.
- `store_and_fwd_flag`: Y = stored and forwarded, N = not.
- `payment_type`: 1=Credit card, 2=Cash, 3=No charge, 4=Dispute, 5=Unknown, 6=Voided trip.
- Data quality checks enforce all constraints above.
