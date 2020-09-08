from datetime import date
from dateutil.relativedelta import relativedelta
from numpy import npv
from math import exp,e
import datetime
from scipy import optimize
print(date.today())
print(date.today() + relativedelta(years=+1))
print(date.today() + relativedelta(months=-3))

def irr(cashflows,iterations=100):
    """The IRR or Internal Rate of Return is the annualized effective 
       compounded return rate which can be earned on the invested 
       capital,i.e.,the yield on the investment.
       >>> irr([-100.0,60.0,60.0])
       0.36309653947517645
    """
    rate = 1.0
    investment = cashflows[0]
    for i in range(1,iterations+1):
        rate *= (1 - npv(rate,cashflows) / investment)
    return rate

print(irr([-100,10,10,110]))


# 函数
def xnpv(rate, cashflows):
    return sum([cf/(1+rate)**((t-cashflows[0][0]).days/365.0) for (t,cf) in cashflows])
 
def xirr(cashflows, guess=0.1):
    try:
        return optimize.newton(lambda r: xnpv(r,cashflows),guess)
    except:
        print('Calc Wrong')

def enpv(rate, cashflows):
    return sum([cf/e**(rate*(t-cashflows[0][0]).days/365.0) for (t,cf) in cashflows])
 
def eirr(cashflows, guess=0.1):
    try:
        return optimize.newton(lambda r: enpv(r,cashflows),guess)
    except:
        print('Calc Wrong')

# # 函数
# def xirr(cashflows):
#     years = [(ta[0] - cashflows[0][0]).days / 365. for ta in cashflows]
#     residual = 1.0
#     step = 0.05
#     guess = 0.05
#     epsilon = 0.0001
#     limit = 10000
#     while abs(residual) > epsilon and limit > 0:
#         limit -= 1
#         residual = 0.0
#         for i, trans in enumerate(cashflows):
#             residual += trans[1] / pow(guess, years[i])
#         if abs(residual) > epsilon:
#             if residual > 0:
#                 guess += step
#             else:
#                 guess -= step
#                 step /= 2.0
#     return guess - 1

data = [(datetime.date(2006, 1, 24), -39967), (datetime.date(2008, 2, 6), -19866), (datetime.date(2010, 10, 18), 245706), (datetime.date(2013, 9, 14), 52142)]
print(xirr(data))
print(eirr(data))
 


    