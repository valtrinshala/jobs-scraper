import concurrent.futures
from common.process_data import *
import os

from local_grant_scrapers.kastori import Kastori

sources = [
    {'type': 'grant', 'source': Kastori()},
]

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_data, src['type'], src['source']) for src in sources]
    for future in concurrent.futures.as_completed(futures):
        future.result()

script_dir = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(script_dir, "logs")
log_file_path = os.path.join(log_dir, "grants_logs.txt")
with open(log_file_path, "w") as file:
    for log in logs:
        file.write(f"{log[0]} - Response: {log[1]}\n")
