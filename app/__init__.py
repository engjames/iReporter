from app.view.redflag_view import RedFlagUrls
from flask import Flask

# Initialize application
app = Flask(__name__)

RedFlagUrls.fetch_urls(app)
