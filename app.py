from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__, template_folder="templates")
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://anhuda2:anhuda123@testdb.m5apx3p.mongodb.net/')
db = client.testdb


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


users_collection = db["users"]

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Proses otentikasi pengguna
        user = users_collection.find_one({'email': email, 'password': password})

        if user:
            # login sukses
            return 'Login berhasil'
        else:
            # login gagal
            return 'Email atau password salah'

    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # periksa apakah user sudah terdaftar
        existing_user = users_collection.find_one({'email': email})

        if existing_user:
            # jika sudah terdaftar maka
            return 'Email sudah terdaftar'

        # add user baru
        users_collection.insert_one({'name': name, 'email': email, 'password': password})

        # jika registrasi sukses maka
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route("/reservasi")
def reservasi():
    return render_template("reservasi.html")


if __name__ == "__main__":
    app.run(debug=True, port=8080, use_reloader=False)
