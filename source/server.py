import os
from domain import create_app


app = create_app(os.getenv("DOMAIN_CONFIGURATION"))
