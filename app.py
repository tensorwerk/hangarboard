from flask import Flask
from api import api
from flask_cors import CORS


app = Flask('HangarAPI', static_folder='static', static_url_path='')
CORS(app)

app.add_url_rule('/repository', view_func=api.RepositoryAPI.as_view('repository_api'))
app.add_url_rule('/arrayset', view_func=api.ArraysetAPI.as_view('arrayset_api'))
app.add_url_rule('/sample', view_func=api.SampleAPI.as_view('sample_api'))
# app.add_url_rule('/history', view_func=api.HistoryAPI.as_view('history_api'))
# app.add_url_rule('/diff', view_func=api.DiffAPI.as_view('diff_api'))
