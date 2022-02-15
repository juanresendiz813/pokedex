from dataclasses import dataclass
from importlib.resources import contents
from itertools import count
from pickle import TRUE
from shutil import move
from unicodedata import name
from urllib.parse import uses_fragment
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import json
from urllib.request import Request, urlopen

from sqlalchemy import JSON

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = TRUE
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY']='SuperSecretKey'
db = SQLAlchemy(app)



# class pokemon(db.Model):
#     _id = db.Column("id", db.Integer, primary_key=True)
#     name = db.Column(db.String(150))
#     url = db.Column(db.String(150))

#     def __init__(self, name, url):
#         self.name = name
#         self.url = url


# def insert_data():
#     url =  f"https://pokeapi.co/api/v2/pokemon/?limit=151".format(JSON)
#     req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
#     webpage = urlopen(req).read()
#     homeData = json.loads(webpage)
#     session["homeData"] = homeData
#     print(homeData)
    # db.session.add(dict)
    # db.session.commit()
# insert_data()

#Get's the users input for the pokemon they are searching for
@app.route("/", methods=['POST', 'GET'])
def index():
    if "homeData" in session:
        user = session["homeData"]
    else:
        url =  f"https://pokeapi.co/api/v2/pokemon/?limit=151".format(JSON)
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        homeData = json.loads(webpage)
        fullList = homeData["results"]
        session["fullList"] = fullList
        count = []
        for i in range(1, 152):
            count.append(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png")
    if request.method == "POST":
        user = request.form.get("nm")
        session["user"] = user
        try:
            url =  f"https://pokeapi.co/api/v2/pokemon/{user}".format(JSON)
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            urlopen(req).read()
            return redirect(url_for("findPokemon"))
        except:
            flash("You have entered a invalid Pokemone name.Please try again.")
            return render_template("index.html", fullList=fullList, count=count)
    else:
        return render_template("index.html", fullList=fullList, count=count)


#Calls API and parses the result
@app.route("/pokemon", methods=['POST', 'GET'])
def findPokemon():
    if "user" in session:
        user = session["user"]
        url =  f"https://pokeapi.co/api/v2/pokemon/{user}".format(JSON)
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        data = json.loads(webpage)
        session["data"] = data
        #parses name out 
        names = data["name"]
        names.capitalize()
        #parses id out 
        id = data["id"]
        #parses fighting moves
        moves = data["moves"]
        hitNames = []
        finalHitName = []
        urlsHit= []
        c = 0
        for fight in moves:
            for k, v in fight.items():
                if k == "move":
                    hitNames.append(v)
                else:
                    c = c+1
        for moveHit in hitNames:
            for k, v in moveHit.items():
                if k == "name":
                    finalHitName.append(v)
                else:
                    urlsHit.append(v)
                    c = c+1
        #parses abilitie names
        dict_list = data["abilities"]
        abilitiesNames = []
        finalName = []
        urls= []
        e = 0
        for dic in dict_list:
            for k, v in dic.items():
                if k == "ability":
                    abilitiesNames.append(v)
                else:
                    e = e+1
        for moveName in abilitiesNames:
            print(moveName)
            for k, v in moveName.items():
                if k == "name":
                    finalName.append(v)
                else:
                    urls.append(v)
                    e = e+1
        return render_template("pokemon.html",  dict=dict, names=names, id=id, finalHitName=finalHitName, finalName=finalName)


if __name__ == "__main__":
    app.run(debug=True)
