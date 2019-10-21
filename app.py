"""
TODO 
add a home button for every page
if the database is empty, show sorry no food available! in the receive page

"""

from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

file_name = 'FoodDonation.db'
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{file_name}"
db = SQLAlchemy(app)

class FoodDonation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    food_type = db.Column(db.String)
    quantity = db.Column(db.Integer)
    age = db.Column(db.Integer)
    expiry = db.Column(db.Integer)
    city = db.Column(db.String)
    phone_no = db.Column(db.String)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/food_donation', methods=['GET','POST'])
def food_donation():
    if request.method == 'GET':
        food_types = ['Veg', 'Non-veg']
        return render_template('donate.html', food_types=food_types)
    else:
        data_fields = ['name','food_type','quantity','age','expiry','city','phone_no']
    
    data_dict = {}
   
    for field in data_fields:
        data_dict[field] = request.form.get(field).lower()

    food_donation = FoodDonation(**data_dict)
    db.session.add(food_donation)
    db.session.commit()

    return redirect(url_for('home'))
    
@app.route('/food_receive', methods=['GET','POST'])
def food_receive():
    if request.method == 'GET':
        food_types = ['Veg', 'Non-veg']
        return render_template('find_food.html', food_types=food_types)
    else:
        food_type = request.form.get('food_type').lower()
        city = request.form.get('city').lower()
        result = FoodDonation.query.\
            filter_by(food_type = food_type).\
            filter_by(city = city).\
                all()

    print(result)
    return render_template('results.html', food_donations=result)

@app.route('/delete_food')
def delete_food():
    food_donation_id = request.args.get('id')
    result = FoodDonation.query.get(food_donation_id)
    print(result)
    db.session.delete(result)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)