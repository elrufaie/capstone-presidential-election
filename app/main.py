# imports

import json
import sys

from bokeh.embed import components

import twtanalysis as twt
import electmapslider_2 as mslider
import stateaggregates as aggs
import issues as issues

# starting Flask app
from flask import Flask, render_template, jsonify, request
import time, random

app = Flask(__name__)
map_plot = mslider.get_electmap_with_controls()
aggs.init()   


@app.route("/")
def chart():
    print("calling / endpoint")

    start = time.time()
    script, div = components(map_plot)
    end = time.time()
    print("components time={}".format(str(end-start)))

    start = time.time()
    twtplot_ey = twt.get_candidate_election_yearmonth_sent_plot()
    twtscript_ey, twtdiv_ey = components(twtplot_ey)

    twtplot_p = twt.get_candidate_party_plot()
    twtscript_p, twtdiv_p = components(twtplot_p)
    twtplot_ec = twt.get_candidate_economy_plot()
    twtscript_ec, twtdiv_ec = components(twtplot_ec)
    twtplot_en = twt.get_candidate_env_plot()
    twtscript_en, twtdiv_en = components(twtplot_en)

    twtplot_h = twt.get_candidate_health_plot()
    twtscript_h, twtdiv_h = components(twtplot_h)
    twtplot_i = twt.get_candidate_imm_plot()
    twtscript_i, twtdiv_i = components(twtplot_i)
    twtplot_j = twt.get_candidate_job_plot()
    twtscript_j, twtdiv_j = components(twtplot_j)
    end = time.time()
    print("twitter plots time={}".format(str(end-start)))

    return render_template("index.html",
        map_div=div, map_script=script,
        twtdiv_ey=twtdiv_ey, twtscript_ey=twtscript_ey,
        twtdiv_p=twtdiv_p, twtscript_p=twtscript_p,
        twtdiv_ec=twtdiv_ec, twtscript_ec=twtscript_ec,
        twtdiv_en=twtdiv_en, twtscript_en=twtscript_en,
        twtdiv_h=twtdiv_h, twtscript_h=twtscript_h,
        twtdiv_i=twtdiv_i, twtscript_i=twtscript_i,
        twtdiv_j=twtdiv_j, twtscript_j=twtscript_j)

@app.route('/details/<state_fips>')
def details(state_fips):
    year = request.args.get('year')
    print("calling /details; state_fips={}; year={}".format(state_fips, year))
    state_details = aggs.get_details_for_state(int(state_fips), int(year))

    details = {
        'details_state_text': state_details.name,
        'details_top_issue': state_details.top_topic,
        'details_votes': state_details.votes,
        'details_win_margin': state_details.win_margin,
        'details_party': state_details.prev_winner
    }

    return jsonify(details)

@app.route('/issues/<state_fips>')
def issues_by_candidate(state_fips):
    year = request.args.get('year')
    issues_by_candidate = issues.get_issues_by_candidates(int(state_fips), int(year))

    return jsonify(issues_by_candidate)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    print("loading app...")
    app.run(host="0.0.0.0", port=8080, debug=True)
    # app.run(host='127.0.0.1', port=8080, debug=True)
