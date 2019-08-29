from flask import Flask
from hangarapi import api

app = Flask('HangarAPI')

app.add_url_rule('/repository', view_func=api.RepositoryAPI.as_view('repository_api'))
app.add_url_rule('/arrayset', view_func=api.ArraysetAPI.as_view('arrayset_api'))
app.add_url_rule('/sample', view_func=api.SampleAPI.as_view('sample_api'))
