import concurrent.futures
from common.process_data import *
import os
from local_job_scrapers.gjirafa import Gjirafa
from local_job_scrapers.kastori import Kastori
from local_job_scrapers.kosova_job import KosovaJob
from local_job_scrapers.portal_pune import PortalPune
from local_job_scrapers.telegrafi import Telegrafi

sources = [
    {'type': 'local_job', 'source': Kastori()},
    {'type': 'local_job', 'source': Telegrafi()},
    {'type': 'local_job', 'source': Gjirafa()},
    {'type': 'local_job', 'source': KosovaJob()},
    {'type': 'local_job', 'source': PortalPune()},
]

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_data, src['type'], src['source']) for src in sources]
    for future in concurrent.futures.as_completed(futures):
        future.result()

script_dir = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(script_dir, "logs")
log_file_path = os.path.join(log_dir, "jobs_logs.txt")
with open(log_file_path, "w") as file:
    for log in logs:
        file.write(f"{log[0]} - Response: {log[1]}\n")
