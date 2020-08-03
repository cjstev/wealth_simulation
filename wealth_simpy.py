import simpy
import pandas as pd
import numpy as np
from wealth_lib import Wealth, Person, wealth_simulation_aggregation
import matplotlib.pyplot as plt

list_of_results = []


def live_one_lifteime(env):
    p1 = Person("CJ", salary=60000, retirement_age=65)
    p2 = Person("Brie", salary=60000, retirement_age=65, pension_rate=.52, salary_growth=.02)
    wealth = Wealth(contributers=[p1, p2], current_wealth=10000, investment_return=None, cost_of_living=50000)

    while p1.age < 90:
        wealth.grow_one_year()
        yield env.timeout(1)  # elapse one year
    list_of_results.append(wealth.return_records())


# create a second environment for the first to reside inside.  (environments within environments..)
def one_simulation(master_env):
    while True:
        env = simpy.Environment()
        env.process(live_one_lifteime(env))
        env.run()
        yield master_env.timeout(1)


master_env = simpy.Environment()
master_env.process(one_simulation(master_env))
master_env.run(until=1000)

len(list_of_results)

print("Simulation complete")

wealth_simulation_aggregation(list_of_results, age_out=70, filename='data.csv')
