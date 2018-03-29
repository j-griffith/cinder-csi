from concurrent import futures
import time

import grpc

import csi_pb2
import csi_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class CinderServicer(csi_pb2_grpc.ControllerServicer):
    """Implements the ControllerServicer."""
    def __init__self():
        pass


    def CreateVolume(self, req, context):
        volume_name = req.name
        if len(req.name) < 1:
            volume_name = str(uuid.uuid4())

        # FIXME(jdg):  Figure out sizing, should be able to just
        # use a similar pattern as above with name, but there are
        # some details around using "range" etc and the conversion
        # from bytes to GiB
        volume_size_gig = 1
        volume_type = req.parameters.get('type', None)
        volume_az = req.parameters.get('availability', None)

        vref = csi_pb2.Volume
        create_response = csi_pb2.CreateVolumeResponse

        vref.id = cvol.volume_id
        create_response.volume = vref
        import pdb; pdb.set_trace()
        return create_response, nil


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
