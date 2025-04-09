import json
import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db, Response
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")


class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """
        locations = []
        persons = []
        try:
            response = requests.get("http://location-api:5000/locations", timeout=5)
            response.raise_for_status()
            jls = response.json()  
            for jl in jls:
                location = Location(
                id=jl["id"],
                person_id=jl["person_id"],
                creation_time=datetime.strptime(jl["creation_time"], "%Y-%m-%dT%H:%M:%S"),
                )
                location.set_wkt_with_coords(jl["latitude"], jl["longitude"])
                locations.append(location)
        except requests.RequestException as e:
            return "Failed to retrieve locations", 503

        try:
            response = requests.get("http://person-api:5000/persons", timeout=5)
            response.raise_for_status()
            jps = response.json()  
            for jp in jps:
                person = Person(
                    id=jp["id"],
                    first_name=jp["first_name"],
                    last_name=jp["last_name"],
                    company_name=jp["company_name"],
                    )
                persons.append(person)
        except requests.RequestException as e:
            return "Failed to retrieve persons", 503

        
        locations: List = locations.filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date).filter(
            Location.creation_time >= start_date
        ).all()

        # Cache all users in memory for quick lookup
        person_map: Dict[str, Person] = {person.id: person for person in persons}

        # Prepare arguments for queries
        data = []
        for location in locations:
            data.append(
                {
                    "person_id": person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": meters,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
                }
            )

        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )
        result: List[Connection] = []
        for line in tuple(data):
            for (
                exposed_person_id,
                location_id,
                exposed_lat,
                exposed_long,
                exposed_time,
            ) in db.engine.execute(query, **line):
                location = Location(
                    id=location_id,
                    person_id=exposed_person_id,
                    creation_time=exposed_time,
                )
                location.set_wkt_with_coords(exposed_lat, exposed_long)

                result.append(
                    Connection(
                        person=person_map[exposed_person_id], location=location,
                    )
                )

        return result

