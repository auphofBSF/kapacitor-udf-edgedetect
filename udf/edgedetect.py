import sys
import json
from kapacitor.udf.agent import Agent, Handler, Server
from kapacitor.udf import udf_pb2
import signal

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger()


# EdgeDetect pass only points that have changed back to Kapacitor
class EdgeDetectHandler(Handler):
    
    def __init__(self, agent):
        self._agent = agent


    def info(self):
        response = udf_pb2.Response()
        response.info.wants = udf_pb2.STREAM
        response.info.provides = udf_pb2.STREAM
        response.info.options['field'].valueTypes.append(udf_pb2.STRING)
        response.info.options['as'].valueTypes.append(udf_pb2.STRING)

        return response

    def init(self, init_req):
        success = True
        msg = ''
        for opt in init_req.options:
            if opt.name == 'field':
                self._field = opt.values[0].stringValue
            elif opt.name == 'as':
                self._as = opt.values[0].stringValue

        if self._field is None:
            success = False
            msg += ' must supply field name'
        if self._as == '':
            success = False
            msg += ' invalid as name'

        response = udf_pb2.Response()
        response.init.success = success
        response.init.error = msg[1:]
        self.lastPoint=None
        return response

    # From movingavg
    # def snapshot(self):
    #     return {
    #             'state' : self._state,
    #     }

    # def restore(self, data):
    #     self._state = data['state']

    def snapshot(self):
        response = udf_pb2.Response()
        response.snapshot.snapshot = ''
        return response

    def restore(self, restore_req):
        response = udf_pb2.Response()
        response.restore.success = False
        response.restore.error = 'not implemented'
        return response

    def begin_batch(self, begin_req):
        raise Exception("not supported")

    def point(self, point):
        response = udf_pb2.Response()
        response.point.CopyFrom(point)
        logger.debug("EdgeDetect:point:%s Fields Strings %s Fields Doubles: %s", point.fieldsString[self._field], point.fieldsString, point.fieldsDouble) #['fieldsString']['value'])

#WIP from moving _avg Example
        #value = point.fieldsDouble[self._field]


        if self.lastPoint:
            if self.lastPoint.fieldsString[self._field]!= point.fieldsString[self._field]:
                    logger.debug("EdgeDetect:CHANGE FOUND") 
                    response.point.fieldsString[self._as] = point.fieldsString[self._field]
                    self._agent.write_response(response, True)
        self.lastPoint = point            
        # self._agent.write_response(response, True)

    def end_batch(self, end_req):
        raise Exception("not supported")

class accepter(object):
    _count = 0
    def accept(self, conn, addr):
        self._count += 1
        a = Agent(conn, conn)
        h = EdgeDetectHandler(a)
        a.handler = h

        logger.info("EdgeDetect:Starting Agent for connection %d", self._count)
        a.start()
        a.wait()
        logger.info("EdgeDetect:Agent finished connection %d",self._count)

if __name__ == '__main__':
    path = "/tmp/edgedetect.sock"
    if len(sys.argv) == 2:
        path = sys.argv[1]
    server = Server(path, accepter())
    logger.info("Started EdgeDetect server 0.2apha")
    server.serve()
