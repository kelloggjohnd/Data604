# -*- coding: utf-8 -*-
"""
Theater Model 
Data 604 Summer 2020
Created on Sun Jul 12 20:29:14 2020
@author: John  Kellogg
"""

import simpy 
import random
import statistics
from modsim import *
import matplotlib.pyplot as plt 

########################Creating the System function########################
def environ_var():
    global alpha
    global beta
    global wait_times
    
    alpha = 3
    beta = 1.5
    wait_times = []
    
def make_system():
    
    num_cashiers = input("Input # of cashiers working: ")
    num_servers = input("Input # of servers working: ")
    num_ushers = input("Input # of ushers working: ")
    num_health = input("Input # of Health screeners working: ")
    #wait_times = []
    mins = []
    secs = []                   
    params = [num_cashiers, num_servers, num_ushers, num_health]
    if all(str(i).isdigit() for i in params):  # Check input is valid
        params = [int(x) for x in params]
    else:
        print(
              "Could not calculate input correctly.  The simulation will use default values"  
              "\nDefault values are 1 Cashier, 1 Server, 1 Usher, 1 Health Screener."  
                )
        params = [1,1,1,1]
    
    return System(num_cashiers = num_cashiers, num_servers = num_servers, num_ushers = num_ushers, 
                  num_health = num_health, mins = mins, secs = secs)


class Theater(object):
     
    def __init__(self, env, num_cashiers, num_servers, num_ushers, num_health):
        self.env = env
        self.cashier = simpy.Resource(env, num_cashiers)
        self.server = simpy.Resource(env, num_servers)
        self.usher = simpy.Resource(env, num_ushers)
        self.health = simpy.Resource(env, num_health)

    # defining the process of tickets and waits of 1 to 3 minutes
    def purchase_ticket(self, moviegoer):
        yield self.env.timeout(random.paretovariate(alpha))

    # defining the Health check and waits 1 to 3 minutes    
    def health_check(self, moviegoer):
        yield self.env.timeout(random.paretovariate(alpha))

    # Add Random if possible
    def check_ticket(self, moviegoer):
        yield self.env.timeout(3 / 60)

    # defining the food options and waits of 1 to 5 minutes
    def sell_food(self, moviegoer):
        yield self.env.timeout(random.paretovariate(beta))

def go_to_movies(env, moviegoer, theater):
    # Moviegoer arrives at the theater
    arrival_time = env.now
    snacks = random.choice([True, False])
    
    # getting a ticket
    with theater.cashier.request() as request:
        yield request
        yield env.process(theater.purchase_ticket(moviegoer))
    
    # getting the health screening    
    with theater.health.request() as request:
        yield request
        yield env.process(theater.health_check(moviegoer))
    
    #getting ticket checked
    with theater.usher.request() as request:
        yield request
        yield env.process(theater.check_ticket(moviegoer))
    
    # random choice to buy snacks or not    
    if snacks == True:
        with theater.server.request() as request:
            yield request
            yield env.process(theater.sell_food(moviegoer))
    
    # substract arrival time from wait times to get total time 
    wait_times.append(env.now - arrival_time)

def run_theater(env, num_cashiers, num_servers, num_ushers, num_health):
    theater = Theater(env, num_cashiers, num_servers, num_ushers, num_health)
    
    lambd = 3
    n = random.randint(1, 10)
    #start sim with people waiting for opening
    #replace with Random number
    for moviegoer in range(n):
        env.process(go_to_movies(env, moviegoer, theater))
    
    # wait time for next person
    while True:
        
        yield env.timeout(random.expovariate(lambd))
        
        # add another movie goer to sim 
        # replace with random number generator of 1-5
        moviegoer += n
        env.process (go_to_movies(env,moviegoer,theater))
        
def get_average_wait_time(wait_times):
    average_wait = statistics.mean(wait_times)
    minutes, frac_minutes = divmod(average_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)

def reset_model():
    global wait_times
    global alpha
    global beta
    wait_times = [] 
    alpha = []
    beta = []

def plot_results(results):
    plt.hist(results, bins = 40)
    plt.show()

def main(system):
# def main(system, num_runs): 
    
  # Setup
    
    environ_var()
    
    #results = TimeSeries()
  
    random.seed(42)
    num_cashiers = int(system.num_cashiers) 
    num_servers = int(system.num_servers) 
    num_ushers = int(system.num_ushers)
    num_health = int(system.num_health)

    # Run the simulation
    env = simpy.Environment()
    env.process(run_theater(env, num_cashiers, num_servers, num_ushers, num_health))
    env.run(until=90)

    # View the results
    mins, secs = get_average_wait_time(wait_times)
    
    plot_results(wait_times)

    """
    for i in range(num_runs):
        results[i] = wait_times
        
    results_full = DataFrame(results)
    results_full = get_average_wait_time(results_full['0'])
    
    return results_full
    """
    print(
            "Running simulation...",
            f"\nThe average wait time is {mins} minutes and {secs} seconds.",
    )
    
    
reset_model()
system = make_system()
main(system)





