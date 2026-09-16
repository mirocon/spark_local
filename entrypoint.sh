#!/bin/bash

set -e

SPARK_WORKLOAD=$1

mkdir -p /opt/spark/spark-events

export PYTHONPATH="${SPARK_HOME}/python:${PYTHONPATH:-}"
py4j_zip=$(ls "${SPARK_HOME}/python/lib"/py4j-*-src.zip 2>/dev/null | head -n1 || true)
if [ -n "$py4j_zip" ]; then
  export PYTHONPATH="${py4j_zip}:${PYTHONPATH}"
fi

echo "SPARK_WORKLOAD: $SPARK_WORKLOAD"

if [ "$SPARK_WORKLOAD" == "master" ]; then
  start-master.sh -p 7077
elif [ "$SPARK_WORKLOAD" == "worker" ]; then
  start-worker.sh spark://spark-master:7077
elif [ "$SPARK_WORKLOAD" == "history" ]; then
  start-history-server.sh
elif [ "$SPARK_WORKLOAD" == "jupyter" ]; then
  exec jupyter lab \
    --ip=0.0.0.0 \
    --port=8888 \
    --no-browser \
    --allow-root \
    --ServerApp.token="${JUPYTER_TOKEN:-spark}" \
    --IdentityProvider.token="${JUPYTER_TOKEN:-spark}" \
    --ServerApp.password='' \
    --ServerApp.root_dir=/opt/spark/notebooks \
    --ServerApp.allow_origin='*'
else
  echo "Unknown SPARK_WORKLOAD: ${SPARK_WORKLOAD}"
  exit 1
fi
