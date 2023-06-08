import threading
import numpy as np
from queue import Queue
from BetMGM import BetMGMScraper
from DraftKings import DraftKingsScraper
from Dictionaries import mlb_abrev, mlb_cities

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

def match_games(dk, betmgm):
    gamesList = []
    for dk_game in range(len(dk)):
        for dk_team in range(len(dk[dk_game])):
            if isinstance(dk[dk_game][dk_team][0], str) and dk[dk_game][dk_team][0] != None:
                for key in mlb_cities:
                    dk[dk_game][dk_team][0] = dk[dk_game][dk_team][0].replace(key, mlb_cities[key]).strip()
                
    for mgm_game in range(len(betmgm)):
        for mgm_team in range(len(betmgm[mgm_game])):
            if isinstance(betmgm[mgm_game][mgm_team][0], str) and betmgm[mgm_game][mgm_team][0] != None:
                for key in mlb_abrev:
                    betmgm[mgm_game][mgm_team][0] = betmgm[mgm_game][mgm_team][0].replace(key, mlb_abrev[key]).strip()
    
    print(dk)
    print()
    print(betmgm)
    for dk_game in dk:
        for mgm_game in betmgm:
            if dk_game[0][0] == mgm_game[0][0] or mgm_game[0][0] == dk_game[0][0]:
                gamesList.append(dk_game + mgm_game)

    return gamesList

def arbitrage(gamesList):
    odds = []
    for game in gamesList:
        mgmOdds1 = int(game[0][1])
        mgmOdds2 = int(game[1][1])
        dkOdds1 = int(game[2][1])
        dkOdds2 = int(game[3][1])
        
        # Convert moneyline odds to implied probabilities
        mgmDecOdds1 = 100 / abs(mgmOdds1) + 1 if mgmOdds1 < 0 else (mgmOdds1 / 100) + 1
        mgmDecOdds2 = 100 / abs(mgmOdds2) + 1 if mgmOdds2 < 0 else (mgmOdds2 / 100) + 1
        dkDecOdds1 = 100 / abs(dkOdds1) + 1 if dkOdds1 < 0 else (dkOdds1 / 100) + 1
        dkDecOdds2 = 100 / abs(dkOdds2) + 1 if dkOdds2 < 0 else (dkOdds2 / 100) + 1

        print(mgmDecOdds1, mgmDecOdds2, dkDecOdds1, dkDecOdds2)
        
        odds.append(
            [round(1/mgmDecOdds1 * 100 + 1/mgmDecOdds2 * 100, 2),
            round(1/mgmDecOdds1 * 100 + 1/dkDecOdds1 * 100, 2),
            round(1/mgmDecOdds1 * 100 + 1/dkDecOdds2 * 100, 2),
            round(1/mgmDecOdds2 * 100 + 1/dkDecOdds1 * 100, 2),
            round(1/mgmDecOdds2 * 100 + 1/dkDecOdds2 * 100, 2),
            round(1/dkDecOdds1 * 100 + 1/dkDecOdds2 * 100, 2)]
        )
        
    print(odds)
    return min(odds[0])


# Process the results as needed
gameList = match_games(dk_result, mgm_result)
print(gameList)
print()
print(arbitrage(gameList))