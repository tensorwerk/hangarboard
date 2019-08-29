if [ "$DEBUG" = "true" ]; then
  export FLASK_ENV=development
  flask run -h 0.0.0.0 -p 5000 --reload
else
  gunicorn --bind 0.0.0.0:8000 app:app
fi
