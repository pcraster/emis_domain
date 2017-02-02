import os
from emis_domain import create_app


app = create_app(os.getenv("EMIS_DOMAIN_CONFIGURATION"))
