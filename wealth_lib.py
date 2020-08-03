import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

s_and_p = pd.read_csv('annual_returns.csv')
s_and_p = s_and_p.loc[s_and_p['Year'].astype(float) > 1960, 'EOY_Mult'].values.astype(float)
s_and_p = s_and_p - 1
s_and_p = s_and_p[s_and_p < .3]


class Wealth:
    def __init__(self, contributers=[], current_wealth=10000, investment_return=None, cost_of_living=50000,
                 inflation_rate=.0244):
        if len(contributers) == 0:
            print("oops, need a contributer")
        self.investment_return = investment_return
        self.wealth = current_wealth
        self.cost_of_living = cost_of_living
        self.inflation_rate = inflation_rate
        self.contributers = contributers
        self.list_of_records = []

    def grow_one_year(self):

        self.cost_of_living *= (1 + self.inflation_rate)
        earned_this_year = 0
        for contributer in self.contributers:
            contributer.birthday()
            earned_this_year += contributer.salary

        earned_this_year -= fed_tax(earned_this_year)
        earned_this_year -= ca_tax(earned_this_year)

        earned_this_year -= self.cost_of_living
        self.wealth += earned_this_year
        if self.investment_return is None:
            this_year_investment_return = np.random.choice(s_and_p)
        else:
            this_year_investment_return = self.investment_return

        self.wealth *= (1 + this_year_investment_return)

        self.list_of_records.append(
            [contributer.name, contributer.age, contributer.salary, self.wealth, self.cost_of_living,
             this_year_investment_return])

    def return_records(self):
        return pd.DataFrame(self.list_of_records, columns=["Name", "Age", "Salary", "Wealth", "COL", "Return%"])


class Person:
    def __init__(self, name, salary=60000, age=36, retirement_age=65, salary_growth=.04, pension_rate=0):
        self.salary = salary
        self.age = age
        self.retirement_age = retirement_age
        self.salary_growth = salary_growth
        self.highest_salary = salary
        self.name = name
        self.pension_rate = pension_rate

    def birthday(self):
        # money_earned = self.salary
        self.salary *= (1 + self.salary_growth)
        if self.highest_salary < self.salary:
            self.highest_salary = self.salary

        self.age += 1

        if self.age > self.retirement_age:
            self.salary = self.highest_salary * self.pension_rate


def wealth_simulation_aggregation(list_of_results, age_out=70, filename='data.csv'):
    wealth_data = [d.loc[d['Age'] == age_out, 'Wealth'] for d in list_of_results]
    big_array = np.vstack(wealth_data)

    age_array = big_array[:, 0]
    age_array.sort()

    x = np.arange(0, 1, 1.0 / age_array.shape[0])
    plt.plot(x, age_array)
    plt.plot(age_array, 1 - x)

    df_out = pd.DataFrame({'wealth': age_array, 'probability': (1 - x)})

    df_out.iloc[np.arange(0, 1000, 10), :].to_csv(filename, index=False)


def ca_tax(income):
    if income < 17618:
        return .01 * income
    elif income < 41766:
        return 176.18 + .0200 * (income - 17618)
    elif income < 65920:
        return 659.14 + .0400 * (income - 41766)
    elif income < 91506:
        return 1625.3 + .0600 * (income - 65920)
    elif income < 115648:
        return 3160.46 + .0800 * (income - 91506)
    elif income < 590746:
        return 5091.82 + .093 * (income - 115648)
    elif income < 708890:
        return 49275 + .103 * (income - 590746)
    else:
        return 61444.76 + .1130 * (income - 708890)


def fed_tax(income):
    taxes = 0
    if income < 19400:
        taxes += income * .1
        return taxes
    else:
        taxes += 19400 * .1
    if income < 78950:
        taxes = taxes + (income - 19400) * .12
        return taxes
    else:
        taxes = taxes + (78950 - 19400) * .12
    if income < 168400:
        taxes = taxes + (income - 78950) * .22
        return taxes
    else:
        taxes = taxes + (168400 - 78950) * .22
    if income < 321450:
        taxes = taxes + (income - 168400) * .24
        return taxes
    else:
        taxes = taxes + (321450 - 168400) * .24
    if income < 408200:
        taxes = taxes + (income - 321450) * .32
        return taxes
    else:
        taxes = taxes + (408200 - 321450) * .32
    if income < 612350:
        taxes = taxes + (income - 408200) * .35
        return taxes
    else:
        taxes = taxes + (408200 - 408200) * .35
    taxes = taxes + (income - 408200) * .37
    return taxes
