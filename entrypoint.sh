if [ "$DEBUG" = "true" ]; then
  export FLASK_ENV=development
  python3 setup_dummy.py
  flask run -h 0.0.0.0 -p 8000 --reload
else
  gunicorn --bind 0.0.0.0:8000 app:app
fi
