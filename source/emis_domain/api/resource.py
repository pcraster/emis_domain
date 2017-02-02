from werkzeug.exceptions import *
from flask_restful import Resource
from flask import request
from .. import db
from .model import DomainModel
from .schema import DomainSchema


domain_schema = DomainSchema()


class DomainResource(Resource):

    def get(self,
            user_id,
            domain_id):

        # user_id is not needed
        domain = DomainModel.query.get(domain_id)

        if domain is None or domain.user != user_id:
            raise BadRequest("Domain could not be found")


        data, errors = domain_schema.dump(domain)

        if errors:
            raise InternalServerError(errors)


        return data


class DomainsResource(Resource):

    def get(self,
            user_id):

        domains = DomainModel.query.filter_by(user=user_id)
        data, errors = domain_schema.dump(domains, many=True)

        if errors:
            raise InternalServerError(errors)

        assert isinstance(data, dict), data


        return data


class DomainsAllResource(Resource):


    # TODO Only call this from admin interface!
    def get(self):

        domains = DomainModel.query.all()
        data, errors = domain_schema.dump(domains, many=True)

        if errors:
            raise InternalServerError(errors)

        assert isinstance(data, dict), data


        return data


    def post(self):

        json_data = request.get_json()

        if json_data is None:
            raise BadRequest("No input data provided")


        # Validate and deserialize input.
        domain, errors = domain_schema.load(json_data)

        if errors:
            raise UnprocessableEntity(errors)


        # Write domain to database.
        db.session.add(domain)
        db.session.commit()


        # From record in database to dict representing a domain.
        data, errors = domain_schema.dump(DomainModel.query.get(domain.id))
        assert not errors, errors
        assert isinstance(data, dict), data


        return data, 201
