# This file is part of ManG.

# ManG is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# ManG is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import socket, time
import ping
from multiprocessing import Process, Lock

class MangIP():
    def __init__(self):
        pass

    is_reachable = 0
    state_changes = 0
    hostname = ''
    ip = '127.0.0.1'
    ping_interval = 5
    p_timeout = 4       # Ping timeout
    #internally used
    p_stop_thread = 0
    p_ping_number = 0
    p_delay = 0
    p_state_kept = 1
    p_failed_count = 0
    p_first_ping = 1
    p_prev_state = 0
    p_recent_change = 0

    mutex = Lock()

    def ping(self):
        try:
            d = ping.do_one(self.ip, self.p_timeout)
            if d is None:
                self.is_reachable = 0
            else:
                self.is_reachable = 1
                self.p_delay = d
            d = None
        except socket.gaierror:
            self.hostname = 'ip_err'
            self.is_reachable = 0

    def check_reachability(self):
        self.ping()
        if not self.is_reachable:
            self.p_failed_count += 1

        if self.p_first_ping:
            self.p_prev_state = self.is_reachable
            self.p_state_kept = 1
            self.p_first_ping = 0
        elif self.p_prev_state != self.is_reachable:
            self.p_state_kept = 0
            self.p_recent_change = 1
        else:
            self.p_state_kept += 1

        if self.p_state_kept > 4 and self.p_recent_change :
            self.p_recent_change = 0
            self.state_changes += 1

        self.p_prev_state = self.is_reachable

    def start_check(self, v_interval):
        logging.debug("Thread start for IP -  %s", str(self.ip))
        self.get_dns()
        while not(self.p_stop_thread):
            with self.mutex: #Ping implementation is not thread safe
                self.check_reachability()
            time.sleep(v_interval)
        logging.debug("Thread stop for IP -  %s", str(self.ip))

    def get_dns(self):
        try:
            self.hostname = socket.getfqdn(self.ip)
        except socket.gaierror:
            self.hostname = 'NA'
        except Exception as e:
            print type(e).__name__
            logging.error("Can't resolve hostname for ", str(self.ip))


    def set_ip(self, v_ip):
        self.ip = v_ip

    def to_str(self):
        k = "OFFLINE"
        if self.is_reachable:
            k = "ONLINE"
        return ",".join([self.ip, self.hostname, str(self.state_changes), k])

