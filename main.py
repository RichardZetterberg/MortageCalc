from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(30), nullable=False)
    interest_rate = db.Column(db.Integer, nullable=False)
    max_loan = db.Column(db.Integer, nullable=False)
    min_down_pay = db.Column(db.Integer, nullable=False)
    loan_term = db.Column(db.Integer, nullable=False)
    branch_code = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), nullable=True)
    FIC = db.Column(db.String(20), nullable=True)
    GIIN = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Bank %r>' % self.id


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/mortage')
def moratge_calc():
    bank_mortgage = Bank.query.order_by(Bank.date.desc()).all()
    return render_template("mortage_calc.html", bank_mortgage=bank_mortgage)


@app.route('/loan')
def loan():
    return render_template("loan.html")


@app.route('/print_result', methods=['POST'])
def print_res():
    banks = Bank.query.order_by(Bank.date.desc()).all()
    initial_loan = float(request.form['init_loan'])
    down_payment = float(request.form['down_pay'])
    name = request.form['bank']
    ind = 0
    result = -1

    for i in banks:
        if i.bank_name == name:
            ind = i.id

    bank = Bank.query.get(ind)

    if bank is None:
        result = "There isn't such bank in our DataBase"
    else:
        interest_rate = bank.interest_rate
        max_loan = bank.max_loan
        min_down_pay = bank.min_down_pay
        loan_term = bank.loan_term

        if down_payment >= min_down_pay and initial_loan <= max_loan:
            result = (initial_loan*(interest_rate/12)*((1+interest_rate/12)**loan_term))/(((1+interest_rate/12)**loan_term)-1)
        elif down_payment < min_down_pay:
            result = "Down payment less than minimum down payment"
        elif initial_loan > max_loan:
            result = "Maximum loan less than initial loan"
        else:
            result = "Down payment less than minimum down payment and maximum loan less than initial loan"

    return render_template("mortage_calc_res.html", value=result)


@app.route('/history')
def history():
    banks = Bank.query.order_by(Bank.date.desc()).all()
    return render_template("history.html", banks=banks)


@app.route('/history/<int:id>')
def hist_details(id):
    bank = Bank.query.get(id)
    return render_template("hist_details.html", bank=bank)


@app.route('/history/<int:id>/delete')
def hist_delete(id):
    bank = Bank.query.get_or_404(id)
    try:
        db.session.delete(bank)
        db.session.commit()
        return redirect('/history')
    except:
        return "Some troubles have arisen"


@app.route('/history/<int:id>/update', methods=['POST', 'GET'])
def update_bank(id):
    bank = Bank.query.get(id)

    if request.method == 'POST':
        bank.bank_name = request.form['bank_name']
        bank.interest_rate = request.form['interest_rate']
        bank.max_loan = request.form['max_loan']
        bank.min_down_pay = request.form['min_down_pay']
        bank.loan_term = request.form['loan_term']
        bank.branch_code = request.form['branch_code']
        bank.currency = request.form['currency']
        bank.FIC = request.form['FIC']
        bank.GIIN = request.form['GIIN']

        try:
            db.session.commit()
            return redirect('/history')
        except:
            return "Some troubles have arisen"
    else:
        return render_template("hist_details_update.html", bank=bank)


@app.route('/create-bank', methods=['POST', 'GET'])
def create_bank():
    if request.method == 'POST':
        bank_name = request.form['bank_name']
        interest_rate = request.form['interest_rate']
        max_loan = request.form['max_loan']
        min_down_pay = request.form['min_down_pay']
        loan_term = request.form['loan_term']
        branch_code = request.form['branch_code']
        currency = request.form['currency']
        FIC = request.form['FIC']
        GIIN = request.form['GIIN']

        bank = Bank(
            bank_name=bank_name,
            interest_rate=interest_rate,
            max_loan=max_loan,
            min_down_pay=min_down_pay,
            loan_term=loan_term,
            branch_code=branch_code,
            currency=currency,
            FIC=FIC,
            GIIN=GIIN
        )

        try:
            db.session.add(bank)
            db.session.commit()
            return redirect('/history')
        except:
            return "Some troubles have arisen"
    else:
        return render_template("create-bank.html")


if __name__ == "__main__":
    app.run(debug=True)