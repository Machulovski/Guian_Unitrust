#IRR_CALCULATOR/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, IntegerField, DateTimeField, FloatField, DateField
from wtforms.validators import DataRequired
from datetime import datetime

# CREATE & UPDATE A TRADE FORM
class TradeForm(FlaskForm):
    equip_amount = IntegerField('设备金额', validators=[DataRequired()])
    rent_period = IntegerField('租金期数', validators=[DataRequired()])
    downpayment = IntegerField('首付款', default=0)
    deposit = IntegerField('保证金', default=0)
    fee = IntegerField('费用', default=0)
    flat_rate = FloatField('合同利率', validators=[DataRequired()])
    payment_type = SelectField('还款方式', choices=[('等额本息','等额本息'),('等额本金', '等额本金'),('不定期还款', '不定额还款')], default='等额本息')
    payment_period = SelectField('还款间隙', choices=[('月付','月付'),('季付', '季付'),('不定期还款', '不定期还款')], default='月付')

    submit = SubmitField('确认交易')

# CREATE & UPDATE A CASHFLOW FORM
class CashflowForm(FlaskForm):
    date = DateField('日期', validators=[DataRequired()],default=datetime.utcnow())
    cashflow_nature = SelectField('款项性质', validators=[DataRequired()], choices=[('设备款项','设备款项'),('首付款','首付款'),('保证金','保证金'), ('费用','费用'), ('保险','保险'), ('回购款','回购款'), ('保证金退回','保证金退回'), ('租金','租金'), ('罚息','罚息')])
    cashflow_type = SelectField('流入/流出', choices=[('流入','流入'),('流出','流出')],default='流出')
    cashflow_amount = FloatField('含税金额', validators=[DataRequired()])
    cashflow_tax = FloatField('税额')

    submit = SubmitField('确认现金流')

# UPDATE LEASE_DATE AND PAYMENT TIME
class LeaseDateForm(FlaskForm):
    lease_date = DateField('起租日', validators=[DataRequired()], default=datetime.utcnow())
    period_end_or_beg = SelectField('租金支付时间', validators=[DataRequired()], choices=[('期初','期初'),('期末','期末')], default = '期末')
    basic_rent = FloatField('基本租金')
    submit = SubmitField('重新部署现金流')


