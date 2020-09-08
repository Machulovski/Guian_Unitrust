from CompanyWebApp.models import CashFlow
from CompanyWebApp import db
from numpy import pmt, irr,ipmt,ppmt
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from scipy import optimize
from math import e

# def cashflows_on_equalprincipal(trade_id, equipment_amount, rent_period, downpayment, deposit, fee, flat_rate, payment_period):
#     count = 0
#     total_principal = equipment_amount-downpayment
#     period_principal = total_principal/rent_period
#     cashflow_equip_payment = CashFlow(trade_id,datetime.utcnow(),"设备款项", "流入",equipment_amount, round(equipment_amount/1.13*0.13,2))
#     cashflow_down_payment = CashFlow(trade_id,datetime.utcnow(),"首付款", "流出",downpayment, round(downpayment/1.13*0.13,2))
#     cashflow_deposit = CashFlow(trade_id,datetime.utcnow(),"保证金", "流出",deposit,0)
#     cashflow_fee = CashFlow(trade_id,datetime.utcnow(),"费用", "流出",fee,round(fee/1.06*0.06,2))
#     db.session.add_all([cashflow_equip_payment,cashflow_down_payment,cashflow_deposit,cashflow_fee])
#     db.session.commit()  

#     if payment_period == "月付" or "不定期还款":
#         period_rate = flat_rate/12
#         cashflow_date = date.today()
#         while count < rent_period:
#             rent_payment = round(period_principal + total_principal*period_rate, 2)
#             total_principal -= period_principal
#             cashflow_date = cashflow_date +relativedelta(months=+1)
#             cashflow_rent = CashFlow(trade_id,cashflow_date,"租金", "流出",rent_payment,round(rent_payment/1.13*0.13,2))
#             db.session.add(cashflow_rent)
#             db.session.commit()
#             count += 1
#     else:
#         period_rate = flat_rate/4
#         cashflow_date = date.today()
#         while count < rent_period:
#             rent_payment = round(period_principal + total_principal*period_rate, 2)
#             total_principal -= period_principal
#             cashflow_date = cashflow_date +relativedelta(months=+3)
#             cashflow_rent = CashFlow(trade_id,cashflow_date,"租金", "流出",rent_payment,round(rent_payment/1.13*0.13,2))
#             db.session.add(cashflow_rent)
#             db.session.commit()
#             count += 1
#     return print('cashflows added')
    
def add_cashflows(trade_id,equipment_amount, rent_period, downpayment, deposit, fee,payment_period, lease_date, period_end_or_beg, basic_rent):
    count = 0
    cashflow_equip_payment = CashFlow(trade_id,lease_date,"设备款项", "流入",equipment_amount, round(equipment_amount/1.13*0.13,2))
    cashflow_down_payment = CashFlow(trade_id,lease_date,"首付款", "流出",-downpayment, -round(downpayment/1.13*0.13,2))
    cashflow_deposit = CashFlow(trade_id,lease_date,"保证金", "流出",-deposit,0)
    cashflow_fee = CashFlow(trade_id,lease_date,"费用", "流出",-fee,-round(fee/1.06*0.06,2))
    db.session.add_all([cashflow_equip_payment,cashflow_down_payment,cashflow_deposit,cashflow_fee])
    db.session.commit() 

    if period_end_or_beg == '期末' and payment_period == "月付" :
        while count < rent_period:
            lease_date = lease_date +relativedelta(months=+1)
            cashflow_rent = CashFlow(trade_id,lease_date,"租金", "流出",-round(basic_rent,2),-round(basic_rent/1.13*0.13,2))
            db.session.add(cashflow_rent)
            db.session.commit()
            count += 1

    elif period_end_or_beg == '期初' and payment_period == "月付" :
        while count < rent_period:
            cashflow_rent = CashFlow(trade_id,lease_date,"租金", "流出",-round(basic_rent,2),-round(basic_rent/1.13*0.13,2))
            db.session.add(cashflow_rent)
            db.session.commit()
            lease_date = lease_date +relativedelta(months=+1)
            count += 1

    elif period_end_or_beg == '期初' and payment_period == "季付":
        while count < rent_period:

            cashflow_rent = CashFlow(trade_id,lease_date,"租金", "流出",-round(basic_rent,2),-round(basic_rent/1.13*0.13,2))
            db.session.add(cashflow_rent)
            db.session.commit()
            lease_date = lease_date +relativedelta(months=+3)
            
            count += 1
    elif period_end_or_beg == '期末' and payment_period == "季付":
        while count < rent_period:

            lease_date = lease_date +relativedelta(months=+3)
            cashflow_rent = CashFlow(trade_id,lease_date,"租金", "流出",-round(basic_rent,2),-round(basic_rent/1.13*0.13,2))
            db.session.add(cashflow_rent)
            db.session.commit()
            count += 1
    
    elif period_end_or_beg == '期初' and payment_period == "不定期还款" :
        while count < rent_period:

            cashflow_rent = CashFlow(trade_id,lease_date,"租金", "流出",-round(basic_rent,2),-round(basic_rent/1.13*0.13,2))
            db.session.add(cashflow_rent)
            db.session.commit()
            lease_date = lease_date +relativedelta(months=+1)
            count += 1

    else:
        while count < rent_period:

            cashflow_rent = CashFlow(trade_id,lease_date,"租金", "流出",-round(basic_rent,2),-round(basic_rent/1.13*0.13,2))
            db.session.add(cashflow_rent)
            db.session.commit()
            lease_date = lease_date +relativedelta(months=+1)
            count += 1

    return print(f"{count}笔租金已添加")

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






    
