from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
    enable_async=True
)
env.globals['enumerate'] = enumerate

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        transaction = {'date': timestamp, 'name': name, 'amount': amount, 'type': '入金'}

        if 'transactions' not in session:
            session['transactions'] = []

        session['transactions'].append(transaction)
        flash('入金が成功しました')
        return redirect(url_for('transactions'))

    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        transaction = {'date': timestamp, 'name': name, 'amount': -amount, 'type': '出金'}

        if 'transactions' not in session:
            session['transactions'] = []

        session['transactions'].append(transaction)
        flash('出金が成功しました')
        return redirect(url_for('transactions'))

    return render_template('withdraw.html')

@app.route('/transactions')
def transactions():
    transactions = session.get('transactions', [])
    total = sum(t['amount'] for t in transactions)

    return render_template('transactions.html', transactions=transactions, total=total)

@app.route('/save_transactions')
def save_transactions():
    if 'transactions' in session and 'history' not in session:
        session['history'] = []

    if 'transactions' in session:
        session['history'].append(session['transactions'])
        session.pop('transactions', None)
        flash('取引履歴が保存されました')

    return redirect(url_for('transactions'))

@app.route('/history')
def history():
    history = session.get('history', [])

    return render_template('history.html', history=history)

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    if request.method == 'POST':
        item_name = request.form['item_name']
        amount = float(request.form['amount'])
        timestamp = datetime.now().strftime('%Y-%m-%d')
        expense = {'date': timestamp, 'item_name': item_name, 'amount': amount}

        if 'expenses' not in session:
            session['expenses'] = []

        session['expenses'].append(expense)
        flash('経費が追加されました')
        return redirect(url_for('expenses'))

    expenses = session.get('expenses', [])
    return render_template('expenses.html', expenses=expenses)

if __name__ == '__main__':
    app.run(debug=True)

