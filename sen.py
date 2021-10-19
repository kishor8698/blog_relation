from enum import unique
from os import stat_result
from flask import Flask, render_template, redirect, request, session,make_response
#from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.sqlite3'
app.config["SESSION_PERMANENT"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "thisisddsecret"
#Session(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin=Admin(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #posts = db.relationship('Post', lazy='dynamic',back_populates='author')
    posts=db.relationship('Post',backref='owner')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #author = db.relationship('User')

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
    
# data=User(username="rkishorRr",email="rkishorrR869819@gmail.com")
# db.session.add(data)


# pdata=Post(body="pqr boffdy",author=data)
# db.session.add(pdata)
 
# db.session.commit()  
'''
db.drop_all()
db.create_all()

# Susan will be both created and added to the session
u1 = User(username='susan', email='susan@example.com')
db.session.add(u1)

# John will be created, but not added
u2 = User(username='john', email='john@example.com')

# Create a post by Susan
p1 = Post(body='this is my post!', author=u1)

# Add susan's post to the session
db.session.add(p1)

# Create a post by john, since john does not yet exist as a user, he is created automatically
p2 = Post(body='this is my post!', author=u2)

# Add john's post to the session
db.session.add(p2)

# After the session has everything defined, commit it to the database
db.session.commit()
'''

'''
class emp(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    address= db.Column(db.String(100))
    state= db.Column(db.String(100))
    pin_code= db.Column(db.String(100))
    
'''
class Customer(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(25))
    customer_email = db.Column(db.String(100), nullable=True)
    order_id = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return f'<Customer: {self.id} {self.customer_name}>'

'''
data=Customer(customer_name='xyz',customer_email='xyz@gmail.com')
db.session.add(data)
db.session.commit()
'''

class Order(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.now)
    order_number = db.Column(db.Integer, default=datetime.now().strftime("%f"))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    
    def __repr__(self):
        return f'<Order: {self.id}>'
'''   
data=Order(customer_id=1)
db.session.add(data)
db.session.commit()
    
'''

    
# result = emp.query.filter_by(name='kishor').first()
# db.session.delete(result)
# db.session.commit()
# result=emp(name='kishor',city='parola',address='maharashtra')
# db.session.add(result)
# db.session.commit()


@app.route("/")
def index():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")

    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
      # if form is submited
      
    if request.method == "POST":
        # record the user name
        session["name"] = request.form.get("name")
        
        # redirect to the main page
        return redirect("/")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
    

