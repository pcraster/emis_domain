import datetime
import uuid
from marshmallow import fields, post_dump, post_load, pre_load, ValidationError
from marshmallow.validate import Length
from .. import ma
from .model import DomainModel


class DomainSchema(ma.Schema):

    class Meta:
        # Fields to include in the serialized result.
        fields = ("user", "name", "pathname", "posted_at", "_links")


    id = fields.UUID(dump_only=True)
    user = fields.UUID(required=True)
    name = fields.Str(required=True, validate=Length(min=1))
    pathname = fields.Str(required=True, validate=Length(min=1))
    posted_at = fields.DateTime(dump_only=True,
        missing=datetime.datetime.utcnow().isoformat())
    _links = ma.Hyperlinks({
            "self": ma.URLFor("api.domain", user_id="<user>",
                domain_id="<id>"),
            "collection": ma.URLFor("api.domains", user_id="<user>")
        })


    def key(self,
            many):
        return "domains" if many else "domain"


    @pre_load(
        pass_many=True)
    def unwrap(self,
            data,
            many):
        key = self.key(many)

        if key not in data:
            raise ValidationError("Input data must have a {} key".format(key))

        return data[key]


    @post_dump(
        pass_many=True)
    def wrap(self,
            data, many):
        key = self.key(many)

        return {
            key: data
        }


    @post_load
    def make_object(self,
            data):
        return DomainModel(
            id=uuid.uuid4(),
            user=data["user"],
            name=data["name"],
            pathname=data["pathname"],
            posted_at=datetime.datetime.utcnow()
        )
