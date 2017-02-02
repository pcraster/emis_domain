from . import api_restful
from .resource import *


# All domains.
# - Get all domains
# - Post domain by user-id
api_restful.add_resource(DomainsAllResource,
    "/domains",
    endpoint="domains_all")

# Domain by user-id and domain-id.
# - Get domain by user-id and domain-id
# - Delete domain by user-id and domain-id
api_restful.add_resource(DomainResource,
    "/domains/<uuid:user_id>/<uuid:domain_id>",
    endpoint="domain")

# Domains by user-id.
# - Get domains by user-id
api_restful.add_resource(DomainsResource,
    "/domains/<uuid:user_id>",
    endpoint="domains")
