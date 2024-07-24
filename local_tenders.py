import concurrent.futures
from common.process_data import *
import os
from local_tender_scrapers.caritas import Caritas
from local_tender_scrapers.cdf import Cdf
from local_tender_scrapers.kastori import Kastori
from local_tender_scrapers.osce import Osce
from local_tender_scrapers.undp import Undp
from local_tender_scrapers.world_bank import WorldBank
from local_tender_scrapers.eaas import Eaas
# from local_tender_scrapers.e_prokurorimi import EProkurorimi
from local_tender_scrapers.ada import ADA

sources = [
    {'type': 'tender', 'source': Caritas()},
    {'type': 'tender', 'source': Kastori()},
    {'type': 'tender', 'source': Osce()},
    {'type': 'tender', 'source': WorldBank()},
    {'type': 'tender', 'source': Undp()},
    {'type': 'tender', 'source': Cdf()},
    {'type': 'tender', 'source': ADA()},
    {'type': 'tender', 'source': Eaas()},
]

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_data, src['type'], src['source']) for src in sources]
    for future in concurrent.futures.as_completed(futures):
        future.result()

script_dir = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(script_dir, "logs")
log_file_path = os.path.join(log_dir, "tender_logs.txt")
with open(log_file_path, "w") as file:
    for log in logs:
        file.write(f"{log[0]} - Response: {log[1]}\n")
