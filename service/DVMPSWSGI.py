import DVMPSService
import threading
import json

class DVMPSWSGI:
    def __init__(self, database=None):
        self.dvmps = DVMPSService.DVMPSService(database=database)
        self.sync_lock = threading.Lock()

    def dvmps_app(self, environ, start_response):
        command = environ['PATH_INFO']

        status = '200 OK'
        headers = [('Content-type', 'text/plain')]

        start_response(status, headers)

        res = None
        request_params = None

        if self.dvmps is not None and environ['REQUEST_METHOD'] == 'POST' and environ.has_key('CONTENT_LENGTH'):
            data_size = int(environ['CONTENT_LENGTH'])
            data = environ['wsgi.input'].read(data_size)
            request_params = json.loads(data)

            if command == '/allocate':
                base_image = None
                expires = None
                comment = None
                priority = 50
                if request_params.has_key('base_image'):
                    base_image = request_params['base_image']
                if request_params.has_key('expires'):
                    expires = request_params['expires']
                if request_params.has_key('comment'):
                    comment = request_params['comment']
                if request_params.has_key('priority'):
                    priority = request_params['priority']
                if base_image is not None and expires is not None:
                    self.sync_lock.acquire()
                    try:
                        res = self.dvmps.allocate_image(base_image, expires, priority, comment)
                    except:
                        self.sync_lock.release()
                        raise
                    self.sync_lock.release()
            elif command == '/deallocate':
                image_id = None
                if request_params.has_key('image_id'):
                    image_id = request_params['image_id']
                if image_id is not None:
                    self.sync_lock.acquire()
                    try:
                        res = self.dvmps.deallocate_image(image_id)
                    except:
                        self.sync_lock.release()
                        raise
                    self.sync_lock.release()
            elif command == '/revert':
                image_id = None
                if request_params.has_key('image_id'):
                    image_id = request_params['image_id']
                if image_id is not None:
                    self.sync_lock.acquire()
                    try:
                        res = self.dvmps.revert_image(image_id)
                    except:
                        self.sync_lock.release()
                        raise
                    self.sync_lock.release()
            elif command == '/poweroff':
                image_id = None
                if request_params.has_key('image_id'):
                    image_id = request_params['image_id']
                if image_id is not None:
                    self.sync_lock.acquire()
                    try:
                        res = self.dvmps.poweroff_image(image_id)
                    except:
                        self.sync_lock.release()
                        raise
                    self.sync_lock.release()
            elif command == '/poweron':
                image_id = None
                if request_params.has_key('image_id'):
                    image_id = request_params['image_id']
                if image_id is not None:
                    self.sync_lock.acquire()
                    try:
                        res = self.dvmps.poweron_image(image_id)
                    except:
                        self.sync_lock.release()
                        raise
                    self.sync_lock.release()
            elif command == '/status':
                image_id = None
                if request_params.has_key('image_id'):
                    image_id = request_params['image_id']
                if image_id is not None:
                    self.sync_lock.acquire()
                    try:
                        res = self.dvmps.image_status(image_id)
                    except:
                        self.sync_lock.release()
                        raise
                    self.sync_lock.release()
            elif command == '/systemstatus':
                self.sync_lock.acquire()
                try:
                    res = self.dvmps.status()
                except:
                    self.sync_lock.release()
                    raise
                self.sync_lock.release()
            elif command == '/running_images':
                self.sync_lock.acquire()
                try:
                    res = self.dvmps.running_images()
                except:
                    self.sync_lock.release()
                    raise
                self.sync_lock.release()
            elif command == '/base_images':
                self.sync_lock.acquire()
                try:
                    res = self.dvmps.base_images()
                except:
                    self.sync_lock.release()
                    raise
                self.sync_lock.release()

        return [json.dumps(res)]
