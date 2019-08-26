import socket
from datetime import datetime


class ClientDetail(object):

    def __init__(self, request=None):
        self.request = request

    def get_elaspsed_time(self):
        if self.request.started_at:
            dt = datetime.now() - self.request.started_at
            dt_ms = dt.total_seconds() * 1000  # milliseconds
            return "%.2f ms" % dt_ms
        else:
            return None

    def get_client_details(self):
        return {
            "hostname": socket.gethostname(),
            "ip_address": socket.gethostbyname(socket.gethostname()),
            "browser_type": self.request.browser_type,
            "elasped_time_ms": self.get_elaspsed_time()
        }
