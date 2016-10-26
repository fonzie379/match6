import random
import matplotlib.pyplot as plt

def pick_player_numbers():
    """
    Uses the random number generator to pick three plays of six numbers

    Returns a list containing a set of each of those plays, [ {},{},{} ]
    """
    numbers = range(1, 50)
    picked_numbers = [set(random.sample(numbers, 6)) for i in range(3)]

    return picked_numbers

def pick_winning_numbers():
    """
    Generates the six winning numbers for the lottery

    Returns a list of the winning numbers
    """
    numbers = range(1, 50)
    winning_numbers = random.sample(numbers, 6)

    return winning_numbers

def number_checker(player_nums, win_nums):
    """
    Takes the numbers the player has picked and compares with the winning numbers

    Returns a list with the number of numbers matching from each play, e.g., [1,0,6]
    """
    results = []

    for play in player_nums:
        results.append(len(play.intersection(win_nums)))

    return results

def jackpot_calculate(jackpot, jackpot_hit, play_results):
    """
    Checks to see if the jackpot was hit in a play and increments or resets the jackpot.
    Also increases the jackpot_hit variable if the jackpot is hit

    Returns the current jackpot and jackpot_hit
    """
    #Increases the jackpot if there isn't a jackpot win
    if 6 in play_results:
        jackpot = 500000
        jackpot_hit += 1        
    else:
        jackpot += 100000

    return jackpot, jackpot_hit


def calculate_winnings(jackpot, play_results, winnings_total):
    """
    Takes the results from a play and calculates the winnings and accumulates hits

    Returns the amount of dollars won per play
    """
    winnings_key = {6: jackpot, 5: 1000, 4: 20, 3: 2}

    for match in play_results:
        try:
            winnings_total += winnings_key[match]
        except KeyError:
            pass
    
    return winnings_total

def matching_totals(play_results, match_totals):
    """
    Takes the play results and keeps track of how many match hits for each possibility 0 through 6

    Modifies the dictionary with the counts, e.g. { 6: 0, 5: 0, 4: 3, ...}
    """
    
    for number in play_results:
        match_totals[number] += 1      


def num_trials(n):

    jackpot = 500000
    jackpot_hit = 0
    winnings = 0
    graph_winnings = []
    match_totals = {6: 0, 5: 0, 4: 0, 3: 0, 2: 0, 1: 0, 0: 0}

    for k in range(n):
        player_numbers = pick_player_numbers()

        winning_numbers = pick_winning_numbers()

        play_results = number_checker(player_numbers, winning_numbers)

        jackpot, jackpot_hit = jackpot_calculate(jackpot, jackpot_hit, play_results)

        winnings = calculate_winnings(jackpot, play_results, winnings)
        graph_winnings.append(winnings)

        matching_totals(play_results, match_totals)   

    #Graphs
    graph(n, graph_winnings)
    histogram(n, match_totals)
   
   #Probability Per Play
    print("Probability Per Play")
    for i in range(7):
        print("Probability of matching " + str(i) + ": " + str(match_totals[i]/(n*3.0)))
    
    at_least_3 = match_totals[6] + match_totals[5] + match_totals[4] + match_totals[3]
    print("Probability of matching at least 3: " + str(at_least_3/(n*3.0)))    
    
    #Winning Probability Per Game
    print('\n' + "Winning Probability Per Game")
    for i in range(3, 7):
        print("Probability of matching " + str(i) + ": " + str(match_totals[i]/(n)))
    
    at_least_3 = match_totals[6] + match_totals[5] + match_totals[4] + match_totals[3]
    print("Probability of matching at least 3: " + str(at_least_3/(n)))    

def graph(n, winnings):
    """
    Graphs the lottery winnings, ticket costs, and net costs of playing
    """    
    cost = [2*(j+1) for j in range(n)]
    f = plt.figure(1)
    net_costs = [ winnings[i]-cost[i] for i in range(n)]
    plt.plot(winnings, label="Lottery Winnings", linewidth=2.5)
    plt.plot(cost, label="Ticket Costs", linewidth=2.5)
    plt.plot(net_costs, label="Net Costs", linewidth=2.5)
    plt.axhline(y=0, color="black")
    plt.xlabel("Number of Plays")
    plt.ylabel("Money Amount")
    plt.title("The Cost of Playing the Match 6 Lotto")
    plt.legend(loc="lower left")
    f.show()

def histogram(n, match_totals):
    """
    Displays a histogram of the number of 0 through 6 matches
    """    
    #Creates a list of the matches
    values = []
    for num, matches in match_totals.items():
        for k in range(matches):
            values.append(num)
    
    g = plt.figure(2)
    data = [(x-.5) for x in range(7)]
    plt.title("Histogram of the Match 6 Lotto")
    plt.ylabel("Number of matches in " + str(3*n) + " plays")
    plt.xlabel("Number of matched out of 6")
    plt.hist(values, bins= data, color='c')
    plt.xticks(range(7))
    plt.xlim([-1,7])
    g.show()

#Number of Trials desired
n = 500
num_trials(n)