import threading
import numpy as np
from queue import Queue
from BetMGM import BetMGMScraper
from DraftKings import DraftKingsScraper

def run_dk_scraper(output_queue):
    DKScraper = DraftKingsScraper()
    result = DKScraper.run()
    output_queue.put(result)  # Put the result in the output queue

def run_mgm_scraper(output_queue):
    MGMScraper = BetMGMScraper()
    result = MGMScraper.run()
    output_queue.put(result)  # Put the result in the output queue

# Create the output queue
output_queue = Queue()

# Create the thread objects
dk_thread = threading.Thread(target=run_dk_scraper, args=(output_queue,))
mgm_thread = threading.Thread(target=run_mgm_scraper, args=(output_queue,))

# Start the threads
dk_thread.start()
mgm_thread.start()

# Wait for the threads to finish
dk_thread.join()
mgm_thread.join()

# Retrieve the results from the output queue
dk_result = output_queue.get()
mgm_result = output_queue.get()

# Process the results as needed
print("DraftKings Result:", dk_result)
print("BetMGM Result:", mgm_result)
