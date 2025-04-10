from app.udaconnect.models import  Location 
from geoalchemy2.types import Geometry as GeometryType
from marshmallow import Schema, fields
from marshmallow_sqlalchemy.convert import ModelConverter as BaseModelConverter


from marshmallow import Schema, fields
from app.udaconnect.models import Location

class LocationSchema(Schema):
    id = fields.Integer()
    person_id = fields.Integer()
    creation_time = fields.DateTime()
    longitude = fields.String(attribute="longitude")
    latitude = fields.String(attribute="latitude")
    wkt_shape = fields.String(attribute="wkt_shape")  # optional but useful

