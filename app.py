from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import numpy as np
import os

app = Flask(__name__)
app.secret_key = "secretkey"

# 🔥 BASE PATH (IMPORTANT FOR DEPLOY)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model and scaler
model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), "rb"))
scaler = pickle.load(open(os.path.join(BASE_DIR, "scaler.pkl"), "rb"))

# Accuracy
accuracy = 87.5


# LOGIN PAGE
@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":

            session['user'] = username
            return redirect(url_for('dashboard'))

        else:

            return render_template(
                "login.html",
                error="Invalid Username or Password"
            )

    return render_template("login.html")


# DASHBOARD
@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template(
        "dashboard.html",
        accuracy=accuracy
    )


# PREDICTION
@app.route('/predict', methods=['POST'])
def predict():

    if 'user' not in session:
        return redirect(url_for('login'))

    gender = request.form['gender']

    # Female = 0, Male = 1
    if gender == "Male":
        gender = 1
    else:
        gender = 0

    age = int(request.form['age'])
    salary = int(request.form['salary'])

    data = np.array([[gender, age, salary]])

    scaled_data = scaler.transform(data)

    prediction = model.predict(scaled_data)

    # Prediction Result
    if prediction[0] == 1:
        result = "Purchased"
    else:
        result = "Not Purchased"

    return render_template(
        "dashboard.html",
        prediction=result,
        accuracy=accuracy
    )


# GRAPH PAGE (NO MATPLOTLIB NEEDED)
@app.route('/graph/<result>')
def graph(result):

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template(
        "graph.html",
        result=result
    )


# LOGOUT
@app.route('/logout')
def logout():

    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)