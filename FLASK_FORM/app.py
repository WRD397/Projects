from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)


### Initialuizing and Creation of Database Model
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Flask_Form.db'
db=SQLAlchemy(app)


### Creating the TABLE of the DATABASE
class forms_table(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(10))
    last_name=db.Column(db.String(10))
    email=db.Column(db.String(20))
    date_created=db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Name %r>' % self.id




### Web Pages
@app.route("/")
def home():
    return render_template('index.html')


@app.route("/form", methods=["POST", "GET"])
def form():
    if request.method == "POST":

        credentials=forms_table(first_name=request.form['first_name'], last_name=request.form['last_name'], email=request.form['email'])

        ### Commiting and pushing to the database table
        try :
            db.session.add(credentials)
            db.session.commit()

            return redirect("/form")
        except : return ("There's an error adding data")

    else :
        form=forms_table.query.order_by(forms_table.date_created)
        return render_template("form.html", form=form)


# @app.route("/signup", methods=["POST"])
# def signup():
#     return render_template("signup.html")




### To run the app (gitbash : "python app.py")
if __name__ == '__main__':
    app.run(debug=True)