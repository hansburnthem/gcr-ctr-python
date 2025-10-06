import os
import sys

from fastapi import FastAPI
import datadog
import logging

datadog.initialize(
    statsd_host="127.0.0.1",
    statsd_port=8125,
)
app = FastAPI()

LOG_FILE = os.environ.get(
    "DD_SERVERLESS_LOG_PATH", "/shared-volume/logs/*.log"
).replace("*.log", "app.log")
print('LOG_FILE: ', LOG_FILE)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')

logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
logger.level = logging.INFO


@app.get("/")
def read_root():
    logger.info("Hello world! ahgahah")
    return {"Hello": "World"}
