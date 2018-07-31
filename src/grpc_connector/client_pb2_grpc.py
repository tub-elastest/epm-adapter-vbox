# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import src.grpc_connector.client_pb2 as client__pb2


class OperationHandlerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Create = channel.unary_unary(
        '/OperationHandler/Create',
        request_serializer=client__pb2.FileMessage.SerializeToString,
        response_deserializer=client__pb2.ResourceGroupProto.FromString,
        )
    self.Remove = channel.unary_unary(
        '/OperationHandler/Remove',
        request_serializer=client__pb2.TerminateMessage.SerializeToString,
        response_deserializer=client__pb2.Empty.FromString,
        )
    self.Stop = channel.unary_unary(
        '/OperationHandler/Stop',
        request_serializer=client__pb2.ResourceIdentifier.SerializeToString,
        response_deserializer=client__pb2.Empty.FromString,
        )
    self.CheckIfResourceExists = channel.unary_unary(
        '/OperationHandler/CheckIfResourceExists',
        request_serializer=client__pb2.ResourceIdentifier.SerializeToString,
        response_deserializer=client__pb2.StringResponse.FromString,
        )
    self.CheckIfResourceRunning = channel.unary_unary(
        '/OperationHandler/CheckIfResourceRunning',
        request_serializer=client__pb2.ResourceIdentifier.SerializeToString,
        response_deserializer=client__pb2.StringResponse.FromString,
        )
    self.Start = channel.unary_unary(
        '/OperationHandler/Start',
        request_serializer=client__pb2.ResourceIdentifier.SerializeToString,
        response_deserializer=client__pb2.Empty.FromString,
        )
    self.ExecuteCommand = channel.unary_unary(
        '/OperationHandler/ExecuteCommand',
        request_serializer=client__pb2.RuntimeMessage.SerializeToString,
        response_deserializer=client__pb2.StringResponse.FromString,
        )
    self.DownloadFile = channel.unary_unary(
        '/OperationHandler/DownloadFile',
        request_serializer=client__pb2.RuntimeMessage.SerializeToString,
        response_deserializer=client__pb2.FileMessage.FromString,
        )
    self.UploadFile = channel.unary_unary(
        '/OperationHandler/UploadFile',
        request_serializer=client__pb2.RuntimeMessage.SerializeToString,
        response_deserializer=client__pb2.Empty.FromString,
        )
    self.CheckStatus = channel.unary_unary(
        '/OperationHandler/CheckStatus',
        request_serializer=client__pb2.Empty.SerializeToString,
        response_deserializer=client__pb2.Status.FromString,
        )


class OperationHandlerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Create(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Remove(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Stop(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CheckIfResourceExists(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CheckIfResourceRunning(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Start(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ExecuteCommand(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DownloadFile(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UploadFile(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CheckStatus(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_OperationHandlerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Create': grpc.unary_unary_rpc_method_handler(
          servicer.Create,
          request_deserializer=client__pb2.FileMessage.FromString,
          response_serializer=client__pb2.ResourceGroupProto.SerializeToString,
      ),
      'Remove': grpc.unary_unary_rpc_method_handler(
          servicer.Remove,
          request_deserializer=client__pb2.TerminateMessage.FromString,
          response_serializer=client__pb2.Empty.SerializeToString,
      ),
      'Stop': grpc.unary_unary_rpc_method_handler(
          servicer.Stop,
          request_deserializer=client__pb2.ResourceIdentifier.FromString,
          response_serializer=client__pb2.Empty.SerializeToString,
      ),
      'CheckIfResourceExists': grpc.unary_unary_rpc_method_handler(
          servicer.CheckIfResourceExists,
          request_deserializer=client__pb2.ResourceIdentifier.FromString,
          response_serializer=client__pb2.StringResponse.SerializeToString,
      ),
      'CheckIfResourceRunning': grpc.unary_unary_rpc_method_handler(
          servicer.CheckIfResourceRunning,
          request_deserializer=client__pb2.ResourceIdentifier.FromString,
          response_serializer=client__pb2.StringResponse.SerializeToString,
      ),
      'Start': grpc.unary_unary_rpc_method_handler(
          servicer.Start,
          request_deserializer=client__pb2.ResourceIdentifier.FromString,
          response_serializer=client__pb2.Empty.SerializeToString,
      ),
      'ExecuteCommand': grpc.unary_unary_rpc_method_handler(
          servicer.ExecuteCommand,
          request_deserializer=client__pb2.RuntimeMessage.FromString,
          response_serializer=client__pb2.StringResponse.SerializeToString,
      ),
      'DownloadFile': grpc.unary_unary_rpc_method_handler(
          servicer.DownloadFile,
          request_deserializer=client__pb2.RuntimeMessage.FromString,
          response_serializer=client__pb2.FileMessage.SerializeToString,
      ),
      'UploadFile': grpc.unary_unary_rpc_method_handler(
          servicer.UploadFile,
          request_deserializer=client__pb2.RuntimeMessage.FromString,
          response_serializer=client__pb2.Empty.SerializeToString,
      ),
      'CheckStatus': grpc.unary_unary_rpc_method_handler(
          servicer.CheckStatus,
          request_deserializer=client__pb2.Empty.FromString,
          response_serializer=client__pb2.Status.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'OperationHandler', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class AdapterHandlerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.RegisterAdapter = channel.unary_unary(
        '/AdapterHandler/RegisterAdapter',
        request_serializer=client__pb2.AdapterProto.SerializeToString,
        response_deserializer=client__pb2.ResourceIdentifier.FromString,
        )
    self.DeleteAdapter = channel.unary_unary(
        '/AdapterHandler/DeleteAdapter',
        request_serializer=client__pb2.ResourceIdentifier.SerializeToString,
        response_deserializer=client__pb2.Empty.FromString,
        )


class AdapterHandlerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def RegisterAdapter(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DeleteAdapter(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_AdapterHandlerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'RegisterAdapter': grpc.unary_unary_rpc_method_handler(
          servicer.RegisterAdapter,
          request_deserializer=client__pb2.AdapterProto.FromString,
          response_serializer=client__pb2.ResourceIdentifier.SerializeToString,
      ),
      'DeleteAdapter': grpc.unary_unary_rpc_method_handler(
          servicer.DeleteAdapter,
          request_deserializer=client__pb2.ResourceIdentifier.FromString,
          response_serializer=client__pb2.Empty.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'AdapterHandler', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
