from flask import Flask, render_template, redirect, url_for, request, session, flash
# from flask_wtf import FlaskForm
# from wtforms import StringField
# from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = "healthclick"
# db = MongoFlaskAlchemy

#data from db ideally
itemData = {49:'Ibuprofen', 39:'Crocin', 80:'Dolo', 120:'Gelusil', 100:'Accutane', 150:'Aspirin', 400:'Azathioprine', 749:'Citalopram', 1299:'Diazepam', 520:'Albuterol', 310:'Allegra', 60:'Benydryl'}
# itemData = {1:'Iboprofin', 2:'Crocin', 3:'Dolo', 4:'Gelusil', 5:'a', 6:'b', 7:'c', 8:'d', 9:'e', 10:'f', 11:'g', 12:'h'}
mymail = "asdf@gmail.com"
mypwd = "12345678"


#every page extends base.html

#MAIN HOME PAGE
@app.route("/")
def home():
	return render_template("home.html")

#ABOUT US
@app.route("/about")
def about():
	return render_template("about.html")

##SERVICES

#for faqchatbot
@app.route("/faqchatbot")
def symptom():
	return render_template("symptom.html")

#for ordering meds
@app.route("/orderMeds")
def meds():
	return render_template("meds.html", itemData=itemData)

#for monthly subs
@app.route("/monthlySubs")
def monthlySubs():
	return render_template("monthlysubs.html")

#for book appointments
@app.route("/bookappointments")
def bookAppointments():
	return render_template("bookappointments.html")

#for at home tests
@app.route("/athomelab")
def atHomeLab():
	return render_template("athomelab.html")

#for med reminder
@app.route("/medreminder")
def medReminder():
	return render_template("medreminder.html")

## SERVICES END

#INSURANCE
@app.route("/insurance")
def insurance():
	return render_template("insurance.html")

#LOGIN
## Logout and usrsuccess included
@app.route("/login", methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		user = request.form["email"]
		pwd = request.form["password"]

		if user==mymail and pwd==mypwd:
			user=user.split('@')
			session["username"] = user[0]
			session["password"] = pwd
			return redirect(url_for("usersuccess"))
		else:
			error = "Invalid Credentials. Try Again."
			return render_template("login.html", error=error)
	else:
		if "username" in session:
			return redirect(url_for("usersuccess"))

		return render_template("login.html")

@app.route("/user")
def usersuccess():
	if "username" in session:
		usr = session["username"]
		if "password" in session:
			pw = session["password"]
			return render_template("usrsuccess.html", user=usr)
	else:
		error = 'Invalid UserId / Password'
		return redirect(url_for("login", error=error))

@app.route("/logout")
def logout():
	session.pop('username', None)
	session.pop('password', None)
	print(session)
	return redirect(url_for('login'))

#REGISTER
@app.route("/register", methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		fname = request.form["fname"]
		lname = request.form["lname"]
		user = request.form["email"]
		pwd = request.form["password"]
		cpwd = request.form["cpassword"]
		if cpwd == pwd:
			msg = "You have registered succesfully."

			mymail = user
			mypwd = pwd

			# session["username"] = user
			# session["password"] = pwd
			# mymail = session["username"] 
			# mypwd = session["password"]
			# print(session)

			return render_template("register.html", msg=msg)
		else:
			msg = "Passwords do not match."
			return render_template("register.html", msg=msg)
	else:
		return render_template("register.html")

#CART
@app.route("/cart")
def cart():
	return render_template("addtocart.html")


if __name__ == "__main__":
	app.run(debug=True)