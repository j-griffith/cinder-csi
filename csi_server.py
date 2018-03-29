from concurrent import futures
import json
import time

import grpc

import csi_pb2
import csi_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

AUTH_URL = "http://10.117.36.5:5000/v3"
USERNAME = "jdg"
PASSWORD = "password"
PROJECT_ID = "394337ba489a40678dc6ebf4d4c4af78"
USER_DOMAIN_NAME = "Default"
VERSION = "3"

class CinderServicer(csi_pb2_grpc.ControllerServicer):
    """Implements the ControllerServicer."""
    def __init__self():
        pass


    def _get_client_session(self):
        from keystoneauth1 import loading
        from keystoneauth1 import session
        from cinderclient import client
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(auth_url=AUTH_URL,
                                        username=USERNAME,
                                        password=PASSWORD,
                                        project_id=PROJECT_ID,
                                        user_domain_name=USER_DOMAIN_NAME)
        sess = session.Session(auth=auth)
        return client.Client(VERSION, session=sess)


    def CreateVolume(self, req, context):
        volume_name = req.name
        if len(req.name) < 1:
            volume_name = str(uuid.uuid4())

        # FIXME(jdg):  Figure out sizing, should be able to just
        # use a similar pattern as above with name, but there are
        # some details around using "range" etc and the conversion
        # from bytes to GiB
        volume_size_gig = 1
        volume_type_name = req.parameters.get('type', None)
        volume_az = req.parameters.get('availability', None)

        cc = self._get_client_session()
        vref = cc.volumes.create(volume_size_gig, name=volume_name, volume_type=volume_type_name)

        # FIXME(jdg): This is still wrong, it doesn't serialize correctly for a grpc response, but
        # I haven't figured out what's wrong yet
        csi_create_response = csi_pb2.CreateVolumeResponse()
        csi_create_response.volume.id = vref.id
        csi_create_response.volume.capacity_bytes = 1
        return csi_create_response


    def DeleteVolume(self, req, context):
        pass


    def ControllerPublishVolume(self, req, context):
        pass


    def ControllerUnpublishVolume(self, req, context):
        pass


    def ValidateVolumeCapabilities(self, req, context):
        pass


    def ListVolumes(self, req, context):
        return csi_pb2.ListVolumesResponse


    def GetCapacity(self, req, context):
        pass


    def ControllerGetCapabilities(self, req, context):
        pass


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    csi_pb2_grpc.add_ControllerServicer_to_server(
        CinderServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("now serving...")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
