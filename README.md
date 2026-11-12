# Classroom Spark cluster (Docker)

Local standalone Spark with **1 master, 3 workers, a history server, and JupyterLab**. Students work in the browser; jobs run on the cluster.

## Start (instructor)

Give Docker Desktop at least **8 GB RAM**. First image build downloads Spark (~20 min). Later rebuilds are incremental.

```bash
make build
docker compose build  #windows
make run-d          # detached: master + 3 workers + history + Jupyter
make urls
```

## Give students these URLs

| What | URL |
| --- | --- |
| JupyterLab | http://localhost:8888/lab?token=spark |
| Spark Master | http://localhost:9090 |
| History Server | http://localhost:18080 |
| Current notebook Spark UI | http://localhost:4040 |

Token is `spark` (see `.env.spark`). This is a local classroom stack, not a locked-down multi-user JupyterHub.

## Streaming lesson

Notebook: `notebooks/spark_streaming_flights.ipynb`.

A small script, `notebooks/flight_producer.py`, writes a JSON file of random flights from `data/T_ONTIME_REPORTING.csv` into `notebooks/incoming_flights/` every 2 seconds. The notebook reads that folder as a stream (`spark.readStream.json`) with Spark `local[*]`, and draws live charts.

Start the producer before the notebook: in JupyterLab open **File > New > Terminal** and run `python flight_producer.py`. Stop it with Ctrl+C. Times are UTC.




## Stop

```bash
make down
```

For notebooks, when prompted please connect to the jupyter server http://localhost:8888/ then type in as password spark, you can change this password in .env.spark