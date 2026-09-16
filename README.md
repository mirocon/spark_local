# Classroom Spark cluster (Docker)

Local standalone Spark with **1 master, 3 workers, a history server, and JupyterLab**. Students work in the browser; jobs run on the cluster.

## Start (instructor)

Give Docker Desktop at least **8 GB RAM**. First image build downloads Spark (~20 min). Later rebuilds are incremental.

```bash
make build
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




## Stop

```bash
make down
```

For notebooks, when prompted please connect to the jupyter server http://localhost:8888/ then type in as password spark, you can change this password in .env.spark