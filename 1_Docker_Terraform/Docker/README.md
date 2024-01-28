# After setup
First run PostgreSQL database and PGAdmin using:
```bash
docker compose up -d
```

Once the database and client have been composed, now it is time to insert data into the database
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -it \
  --network=1_docker_terraform_default \
  dezoomcamp2024_learn_docker \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```

> [!NOTE]
> network used in the 'dezoomcamp2024_learn_docker' docker container has the name '1_docker_terraform_default'
> that is because by default a docker compose file will create a network with name 'folder_name_default'


testing