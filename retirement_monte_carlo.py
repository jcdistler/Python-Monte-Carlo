# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 13:50:16 2024

@author: dis76169
"""

import pandas as pd
import numpy as np
import random  
import matplotlib.pyplot as plt  

# starting_age = 30
# retirement_age = 59  
# life_expectancy = 95  
# initial_investment = 287678  # $
# annual_contribution = 48442 # $/year
# coast_fi_age = 45
# social_security = 3000 # $/month
# withdrawal_rate = 100000 # $/year

# Define the variables  
starting_age = int(input("What is your current age?   "))
retirement_age = int(input("When do you plan to retire?   "))
life_expectancy = int(input("Expected lifespan?   "))
initial_investment = int(input("What is your current savings?   "))
annual_contribution = int(input("What is your current annual contribution (USD)?   "))
social_security = int(input("What is your expected social secuirty (USD/month)?   "))
withdrawal_rate = int(input("What is your expected withdrawal rate in retiremenet (USD)?   "))
coast_fi_age = int(input("What age to you expect to stop contributing for 'CoastFI'?   "))
num_simulations = 10000  
  
# Load the historical data only from 1960   
sp500_returns = pd.read_excel('sp500-return.xlsx')
inflation_rates = pd.read_excel('inflation-rate.xlsx') 

# getting mean historical data
sp500_return_mean = sp500_returns.mean()[1]
inflation_rates_mean = inflation_rates.mean()[1]

#getting standard deviation of historical data
sp500_return_std = sp500_returns.std()[1]
inflation_rates_std = inflation_rates.std()[1]
  
# Define the simulation function  
def simulate_retirement():  
    investment_balance = initial_investment
    investment_balance_compiled = []
    returns_compiled = []
    inflation_compiled = []
    for year in range(starting_age, life_expectancy):  
        # Get a random rate of return and inflation rate from the historical data  
        rate_of_return = random.normalvariate(sp500_return_mean, sp500_return_std)  
        inflation_rate = random.normalvariate(inflation_rates_mean, inflation_rates_std)
        #adjust "real" value inputs into "nominal" future dollars based on sum of total inflation
        withdrawal_rate_nominal = withdrawal_rate * (1 + sum(inflation_compiled)/100)
        annual_contribution_nominal = annual_contribution * (1 + sum(inflation_compiled)/100)
        # Calculate the investment balance for the year
        if year < retirement_age and year < coast_fi_age: #checking if contributions are continued
            investment_balance += annual_contribution_nominal + investment_balance * (rate_of_return)
        elif year < retirement_age and year >= coast_fi_age: #checking if contributions are stopped
            investment_balance += investment_balance * (rate_of_return)
        else: #period of retirement age when withdrawals start
            investment_balance += investment_balance * (rate_of_return) - withdrawal_rate_nominal
        investment_balance_compiled.append(investment_balance)
        returns_compiled.append(rate_of_return*100)
        inflation_compiled.append(inflation_rate*100)
        # print(withdrawal_rate_nominal)
    return investment_balance_compiled, returns_compiled, inflation_compiled


simulate_retirement_return_rates = simulate_retirement()[1]
simulate_retirement_inflation_rates = simulate_retirement()[2]

# Run the simulations  
successful_simulations = []  
failed_simulations = []
all_simulations = []
for i in range(num_simulations):  
    all_simulations.append(simulate_retirement()[0])
    investment_balance = all_simulations[-1]
    if investment_balance[-1] >= 0:  
        successful_simulations.append(investment_balance[-1])
    else:
        failed_simulations.append(investment_balance[-1])

#analyze the varying percentiles
fifth_percentile_simulations = []
thirtieth_percentile_simulations = []
mean_simulations = []
seventieth_percentile_simulations = []
ninetyfifth_percentile_simulations = []

for year in range(0, (life_expectancy - starting_age)):
    all_simulations_year = [] #creating a list of all simulations for each year to assess percentiles
    for simulation in range(num_simulations):
        all_simulations_year.append(all_simulations[simulation][year])
    fifth_percentile_simulations.append(np.percentile(all_simulations_year, 5))
    thirtieth_percentile_simulations.append(np.percentile(all_simulations_year, 30))
    mean_simulations.append(np.percentile(all_simulations_year, 50))
    seventieth_percentile_simulations.append(np.percentile(all_simulations_year, 70))
    ninetyfifth_percentile_simulations.append(np.percentile(all_simulations_year, 95))
    
#plot percentile graphs
plt.plot(range(starting_age, life_expectancy), thirtieth_percentile_simulations, label = "30th percentile")    
plt.plot(range(starting_age, life_expectancy), mean_simulations, label = "50th percentile") 
plt.plot(range(starting_age, life_expectancy), seventieth_percentile_simulations, label = "70th percentile")

plt.ylabel('Nominal Dollars (USD)', )
plt.xlabel('Age (years)')
plt.legend()

# Analyze the results  
success_rate = (len(successful_simulations) / num_simulations)*100  
average_balance = mean_simulations[-1]  
  
# Print the results  

print(f"Success rate: {success_rate:.2f}%")  
print(f"Expected investment balance: ${average_balance:,.0f}")  
print(f"Range of investment balances: $", '{:,.0f}'.format(thirtieth_percentile_simulations[-1]), "to $", '{:,.0f}'.format(seventieth_percentile_simulations[-1]))  