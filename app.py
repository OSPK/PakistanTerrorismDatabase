from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    country = db.Column(db.String(80))
    city = db.Column(db.String(80))
    province = db.Column(db.String(80))
    perpetrator_group = db.Column(db.String(380))
    fatalities = db.Column(db.Integer)
    injured = db.Column(db.Integer)
    target_type = db.Column(db.String(380))
    attack_type = db.Column(db.String(380))
    weapon_type = db.Column(db.String(380))
    incident_summary = db.Column(db.String(1080))
    sources = db.Column(db.String(580))
    suicide_attack = db.Column(db.String(80))
    target = db.Column(db.String(80))

    def __repr__(self):
        return self.incident_summary

# db.create_all()
incidents = Incident.query.all()

def clean_list(list_to_clean, column_name):
    cleaned_items = [str(inc.__getattribute__(column_name)).strip().\
              replace(' (suspected)', '') for inc in list_to_clean]

    cleaned_items = set(str(set(cleaned_items)).\
             strip().replace("/",",").replace("'", "").\
             replace('"', '').replace("{", "").replace("}", "").split(","))

    cleaned_items = set([gr.strip() for gr in cleaned_items])

    if column_name == 'weapon_type':
        str_ = "i.e."
        str2_ = " (not to include vehicle-borne explosives"
        str3_ = "car or truck bombs)"
        cleaned_items = [it.replace(str_, "").replace(str2_, "").replace(str3_, "") for it in cleaned_items if it!='']

    return list(cleaned_items)

def find_things(thing_, col_, str_):
    things = [inc for inc in thing_ if str_ in inc.__getattribute__(col_)]

    return things

@app.route("/")
def hello_world():
    provinces = set([inc.province for inc in incidents])

    cities = set([str(inc.city).title().strip() for inc in incidents])

    groups = clean_list(incidents, 'perpetrator_group')

    targets = clean_list(incidents, 'target_type')

    attacks = clean_list(incidents, 'attack_type')

    weapons = clean_list(incidents, "weapon_type")

    things = find_things(incidents, "weapon_type", "Biological")

    return render_template("index.html", cities=cities,\
        provinces=provinces, groups=groups,\
        targets=targets, attacks=attacks, weapons=weapons,\
        things=things
        )