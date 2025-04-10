from concurrent import futures
import grpc
import location_pb2
import location_pb2_grpc
from app.udaconnect.services import LocationService
from datetime import datetime

class LocationServiceServicer(location_pb2_grpc.LocationServiceServicer):
    def __init__(self, app):
        self.app = app
    
    def GetLocation(self, request, context):
        with self.app.app_context():  
            loc = LocationService.retrieve(request.location_id)
            return location_pb2.LocationResponse(
                id=loc.id,
                person_id=loc.person_id,
                latitude=loc.latitude,
                longitude=loc.longitude,
                creation_time=loc.creation_time.isoformat(),
            )
        
def serve(flask_app):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    location_pb2_grpc.add_LocationServiceServicer_to_server(
        LocationServiceServicer(flask_app), server
    )
    server.add_insecure_port("0.0.0.0:50051")
    print("gRPC server running on 50051")
    server.start()
    server.wait_for_termination()
