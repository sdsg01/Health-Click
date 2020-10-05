from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = "healthclick"
app.config["MONGO_URI"] = "mongodb://localhost:27017/Health"
mongo = PyMongo(app)

#collections in db:Health
login_collection = mongo.db.users
cart_collection = mongo.db.cart
itemData = {49:'Ibuprofen', 39:'Crocin', 80:'Dolo', 120:'Gelusil', 100:'Accutane', 150:'Aspirin', 400:'Azathioprine', 749:'Citalopram', 1299:'Diazepam', 520:'Albuterol', 310:'Allegra', 60:'Benydryl'}


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
    items = []
    for i, data in itemData.items():
        cart1 = cart_collection.find_one({'item': data})
        items.append(cart1)
        # print(items)
    return render_template("meds.html", items=items)

#CART
cart_list = []

@app.route("/cart")
@app.route("/cart/<id>")
def cart(id):
    global cart_list

    # items = []
    totalprice = 0
    ind = int(id.split('.')[0])
    cart1 = cart_collection.find_one({'i': ind})
    if cart1 != None:
        totalprice += int(cart1["price"])
        cart_list.append(cart1)
    else:
        totalprice = 0

    return render_template("addtocart.html", items=cart_list, totalprice=totalprice, id=ind)

#clear cart
@app.route("/clear")
def clear():
    cart_list = []
    # print(cart_list)
    return redirect(url_for('meds'))

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
## Logout and usersuccess included
@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form["email"]
        pwd = request.form["password"]
        user1 = login_collection.find_one({'user': user})

        if user1["user"]==user and user1["password"]==pwd:
            user=user.split('@')
            session["username"] = user[0]
            session["password"] = pwd
            return redirect(url_for("usersuccess"))
        else:
            msg = "Invalid Credentials. Try Again."
            return render_template("login.html", msg=msg)
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
            print(pw)
            return render_template("usrsuccess.html", user=usr)
    else:
        msg = 'Invalid UserId / Password'
        return redirect(url_for("login", msg=msg))

@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('password', None)
    # print(session)
    msg = "Logout Successful."
    return redirect(url_for('login', msg=msg))

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

            login_collection.insert({'user' : user, 'password' : pwd})

            msg = "Successful Register."
            return redirect(url_for("login", msg=msg))
        else:
            msg = "Passwords do not match."
            return render_template("register.html", msg=msg)
    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)