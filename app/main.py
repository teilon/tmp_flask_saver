from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

from config import SQLALCHEMY_DATABASE_URI
from calc import receive_data

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)

class Sino_trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(50), nullable=False)
    station = db.Column(db.String(50), nullable=False)
    article = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(50), nullable=False)
    sale = db.Column(db.Integer, default=0)
    rest = db.Column(db.Integer, default=0)
    month = db.Column(db.String(50), nullable=False)
    aroma_type = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/api/save-data/', methods=['GET', 'POST'])
def add_data_handler():

    if request.form.get('secret') == '123':
        month = request.form.get('month')
        data = request.files.get('data')

        data = receive_data(data, month)
        for index, row in data.iterrows():
            try:
                trade = Sino_trade(region=row['region'],
                                   station=row['station'],
                                   article=row['article'],
                                   number=row['number'],
                                   sale=row['sale'],
                                   rest=row['rest'],
                                   month=row['month'],
                                   aroma_type=row['aroma_type']
                                   )
                db.session.add(trade)
                db.session.commit()
            except Exception as e:
                print("FAILURE TO APPEND: {}".format(e))
        return jsonify(dict(success=1))

    return jsonify(dict(success=0))

if __name__ == '__main__':
    app.run(port=5001)

