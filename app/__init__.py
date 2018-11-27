from flask import Flask

# Initialize application
app = Flask(__name__)

from app.view.redflag_view import RedFlagUrls
RedFlagUrls.fetch_urls(app)

