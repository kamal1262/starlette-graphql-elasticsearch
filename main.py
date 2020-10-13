import os
from app import create_app

env = os.environ.get("FLASK_ENV", "development")
app = create_app("config.%sConfig" % env.capitalize())
