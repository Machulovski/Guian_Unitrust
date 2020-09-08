#IRR_CALCULATOR/views.py
from flask import render_template,url_for,flash,redirect,request,Blueprint,session
from flask_login import current_user, login_required
from CompanyWebApp import db
from CompanyWebApp.models import Trade, CashFlow
from CompanyWebApp.irr_calculators.forms import TradeForm, CashflowForm, LeaseDateForm
from datetime import datetime, date
from CompanyWebApp.irr_calculators.cashflow_generate import add_cashflows, xirr, eirr

irr_calculators = Blueprint('irr_calculators', __name__)

#TRADE LIST
@irr_calculators.route('/trade_list', methods = ['GET','POST'])
@login_required
def trade_list():

    trans = Trade.query.order_by(Trade.id.desc())

    return render_template('irr_trade_list.html', trans = trans)

#CREATE A TRADE
@irr_calculators.route('/trade_create', methods=['GET', 'POST'])
@login_required
def trade_create():

    form = TradeForm()

    if form.validate_on_submit():

        new_trade = Trade(equip_amount=form.equip_amount.data, rent_period=form.rent_period.data, downpayment=form.downpayment.data, deposit=form.deposit.data,fee=form.fee.data, flat_rate=form.flat_rate.data,payment_type=form.payment_type.data,payment_period=form.payment_period.data,irr_nor=0,irr_exp=0)
        db.session.add(new_trade)
        db.session.commit()

        flash('您已经成功添加一项交易！')
        
        return redirect(url_for('irr_calculators.trade_list'))
    return render_template('irr_trade_create.html', form=form)

#UPDATE A TRADE
@irr_calculators.route('/<int:trade_id>/trade_update', methods = ['GET','POST'])
@login_required
def trade_update(trade_id):
    
    trade = Trade.query.get_or_404(trade_id)
    
    form = TradeForm()

    if form.validate_on_submit():
        trade.equip_amount = form.equip_amount.data
        trade.rent_period = form.rent_period.data
        trade.downpayment = form.downpayment.data
        trade.deposit = form.deposit.data
        trade.fee = form.fee.data
        trade.flat_rate= form.flat_rate.data
        trade.payment_type = form.payment_type.data
        trade.payment_period = form.payment_period.data
        db.session.commit()
        
        # cashflows = CashFlow.query.filter_by(tra_id=trade.id)
        # # update default cashflows to the cashflow database
        # # equip_amount_payment
        # cashflow_equip_payment = CashFlow(trade.id,datetime.utcnow(),"设备款项", "流入",trade.equip_amount, trade.equip_amount/1.13*0.13)
        # # down_payment
        # cashflow_down_payment = CashFlow(trade.id,datetime.utcnow(),"首付款", "流出",-trade.downpayment, -trade.downpayment/1.13*0.13)
        # # deposit
        # cashflow_deposit = CashFlow(trade.id,datetime.utcnow(),"保证金", "流出",-trade.deposit, -trade.deposit/1.13*0.13)
        # # fee
        # cashflow_fee = CashFlow(trade.id,datetime.utcnow(),"费用", "流出",-trade.fee, -trade.fee/1.13*0.13)
        # db.session.add_all([cashflow_equip_payment,cashflow_down_payment,cashflow_deposit,cashflow_fee])
        # db.session.commit()  
        
        flash(f'更新了{trade.id}号交易！')

        return redirect(url_for('irr_calculators.trade_list'))
    
    elif request.method == 'GET':
        form.equip_amount.data = trade.equip_amount
        form.rent_period.data = trade.rent_period
        form.downpayment.data = trade.downpayment 
        form.deposit.data = trade.deposit
        form.fee.data = trade.fee 
        form.flat_rate.data = trade.flat_rate 
        form.payment_type.data = trade.payment_type 
        form.payment_period.data = trade.payment_period

    return render_template('irr_trade_create.html', form=form, trade=trade)

#DELETE A TRADE
@irr_calculators.route('/<int:trade_id>/trade_delete', methods = ['GET','POST'])
@login_required
def trade_delete(trade_id):
    trade = Trade.query.get_or_404(trade_id)

    db.session.delete(trade)
    db.session.commit()
    flash(f'删除了{trade.id}号交易')
    return redirect(url_for('irr_calculators.trade_list'))

#Cashflows and IRR
@irr_calculators.route('/<trade_id>/irr_cashflows', methods = ['GET','POST'])
@login_required
def irr_cashflows(trade_id):
    trade = Trade.query.filter_by(id=trade_id).first()
    XIRR = trade.irr_nor
    EIRR = trade.irr_exp
    equip_amount = trade.equip_amount
    rent_period = trade.rent_period
    downpayment = trade.downpayment
    deposit = trade.deposit
    fee = trade.fee
    payment_period = trade.payment_period
    cashflows = CashFlow.query.filter_by(tra_id=trade_id).order_by(CashFlow.date.asc())
    form = LeaseDateForm()
    count = 0
    if form.validate_on_submit():
        lease_date = form.lease_date.data
        period_end_or_beg = form.period_end_or_beg.data
        basic_rent = form.basic_rent.data

        for cashflow in cashflows:
            db.session.delete(cashflow)
        add_cashflows(trade_id, equip_amount, rent_period,downpayment, deposit, fee,payment_period,lease_date,period_end_or_beg, basic_rent)
        return redirect(url_for('irr_calculators.irr_cashflows', trade_id=trade_id))

    return render_template('irr_cashflows.html', trade_id=trade_id, cashflows = cashflows, trade=trade, form=form, count=count, XIRR=XIRR, EIRR=EIRR)

#CREATE A CASHFLOW
@irr_calculators.route('/<trade_id>/cashflow_create', methods=['GET', 'POST'])
@login_required
def cashflow_create(trade_id):

    form = CashflowForm()

    if form.validate_on_submit():

        new_cashflow = CashFlow(tra_id=trade_id, date=form.date.data, cashflow_nature=form.cashflow_nature.data, cashflow_type=form.cashflow_type.data,cashflow_amount=form.cashflow_amount.data, cashflow_tax=form.cashflow_tax.data)
        db.session.add(new_cashflow)
        db.session.commit()
        flash('您已经成功添加一条现金流！')
        return redirect(url_for('irr_calculators.irr_cashflows', trade_id=trade_id))
    return render_template('irr_cashflow_create.html', form=form, trade_id=trade_id)

#DELETE A CASHFLOW
@irr_calculators.route('/<int:cashflow_id>/cashflow_delete', methods = ['GET','POST'])
@login_required
def cashflow_delete(cashflow_id):
    cashflow = CashFlow.query.get_or_404(cashflow_id)
    trade_id = cashflow.tra_id
    db.session.delete(cashflow)
    db.session.commit()
    flash('删除了一条现金流')
    return redirect(url_for('irr_calculators.irr_cashflows', trade_id=trade_id))

#UPDATE A CASHFLOW
@irr_calculators.route('/<int:cashflow_id>/cashflow_update', methods = ['GET','POST'])
@login_required
def cashflow_update(cashflow_id):
    
    cashflow = CashFlow.query.get_or_404(cashflow_id)
    trade_id = cashflow.tra_id
    form = CashflowForm()

    if form.validate_on_submit():
        cashflow.date = form.date.data
        cashflow.cashflow_nature = form.cashflow_nature.data
        cashflow.cashflow_type = form.cashflow_type.data
        cashflow.cashflow_amount = form.cashflow_amount.data
        cashflow.cashflow_tax = form.cashflow_tax.data
        db.session.commit()
        
        flash(f'更新了一条现金流！')

        return redirect(url_for('irr_calculators.irr_cashflows', trade_id=trade_id))
    
    elif request.method == 'GET':
        form.date.data = cashflow.date 
        form.cashflow_nature.data = cashflow.cashflow_nature 
        form.cashflow_type.data = cashflow.cashflow_type 
        form.cashflow_amount.data = cashflow.cashflow_amount  
        form.cashflow_tax.data = cashflow.cashflow_tax 

    return render_template('irr_cashflow_create.html', form= form)

#calculate xirr and eirr
@irr_calculators.route('/<int:trade_id>/calculate_irr', methods = ['GET','POST'])
@login_required
def calculate_irr(trade_id):
    cashflows=CashFlow.query.filter_by(tra_id=trade_id).order_by(CashFlow.date.asc())
    cashflow_data=[]
    for cashflow in cashflows:
        time = cashflow.date
        amount = cashflow.cashflow_amount
        cashflow_data.append((time,amount))
    XIRR = xirr(cashflow_data)
    EIRR = eirr(cashflow_data)
    trade = Trade.query.filter_by(id=trade_id).first()

    try:
        trade.irr_nor = round(float(XIRR*100),4)
        trade.irr_exp = round(float(EIRR*100),4)
    except:
        trade.irr_nor = 0
        trade.irr_exp = 0
    db.session.commit()
    flash(f'IRR已经重新计算！XIRR:{trade.irr_nor}%/年, 连续复利IRR{trade.irr_exp}%/年')
    return redirect(url_for('irr_calculators.irr_cashflows', trade_id=trade_id))
    
