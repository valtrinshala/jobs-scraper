import concurrent.futures

from common.process_data import *
import os
from external_job_scrapers.arbeits_agentur import ArbeitsAgentur
from external_job_scrapers.xing import Xing

sources = [
    # {'type': 'job', 'source': RemoteCo()},
    # {'type': 'job', 'source': StepStone()},
    {'type': 'external_job', 'source': ArbeitsAgentur()},
    {'type': 'external_job', 'source': Xing()},
    # {'type': 'job', 'source': Indeed()}
]

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_data, src['type'], src['source']) for src in sources]
    for future in concurrent.futures.as_completed(futures):
        future.result()

script_dir = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(script_dir, "logs")
log_file_path = os.path.join(log_dir, "external_jobs_logs.txt")
with open(log_file_path, "w") as file:
    for log in logs:
        file.write(f"{log[0]} - Response: {log[1]}\n")
