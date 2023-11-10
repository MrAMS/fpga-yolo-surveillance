from flask import Flask
from flask import render_template, jsonify, request
from utils import *
import models
from pony.flask import Pony



app = Flask(__name__,
            static_url_path='')
Pony(app)


@app.route("/")
def index():
    return render_template('app.html')

@app.route("/query/<sdate>/<stime>/<edate>/<etime>")
def query(sdate, stime, edate, etime):
    s = convert_datetime(sdate, stime)
    e = convert_datetime(edate, etime)
    return render_template('index.html', objects=models.get_object_in_date_range(s, e))

@app.route("/api/query", methods=['POST'])
def api_query():
    print(request.json)
    types = request.json.get('types')
    date = request.json.get('dates')
    data_s = datetime.fromtimestamp(date[0]/1000)
    data_e = datetime.fromtimestamp(date[1]/1000)
    print(data_s, data_e, types)
    ret = []
    res = models.query_object(data_s, data_e, types)
    for obj in res:
        ret.append({'name': obj.name, 'date': [obj.time_appear.timestamp(), obj.time_exit.timestamp()], 'confidence': obj.confidence, 'img': obj.img_path})
    print(ret)
    return jsonify({'success':1, 'return': ret})

@app.route("/debug/add_obj/<int:track_id>/<name>/<sdate>/<stime>")
def debug_add_obj(track_id, name, sdate, stime):
    print(track_id, convert_datetime(sdate, stime))
    models.create_object(tracker_id=track_id, name=name, time_appear=convert_datetime(sdate, stime), img_path='http://lh3.googleusercontent.com/TF82jIDHh1pYFAzcc-nPr96W6an_YTJEtOJbV5ZaYXlE3d4UcelEd8hSt9MJlT9bPc36eJWhiDuUKqbnCgB2rzSD=s150', confidence=0.9)
    return render_template('index.html')
