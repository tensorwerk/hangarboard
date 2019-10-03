import os
from flask import Flask
from flask import send_from_directory
from flask_cors import CORS
from api import api
from api.utils import get_logger


logger = get_logger(__name__)


app = Flask('HangarAPI', static_folder='static', static_url_path='')
app.url_map.strict_slashes = False
CORS(app)

app.add_url_rule('/repository', view_func=api.RepositoryAPI.as_view('repository_api'))
app.add_url_rule('/arrayset', view_func=api.ArraysetAPI.as_view('arrayset_api'))
app.add_url_rule('/sample', view_func=api.SampleAPI.as_view('sample_api'))
# app.add_url_rule('/history', view_func=api.HistoryAPI.as_view('history_api'))
# app.add_url_rule('/diff', view_func=api.DiffAPI.as_view('diff_api'))

# Serve React App
@app.route('/')
@app.route('/home')
@app.route('/dashboard')
@app.route('/dashboard/<path:path>')
def serve(path=None):
    return send_from_directory(app.static_folder, 'index.html')
