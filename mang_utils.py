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

import logging, re, socket

def prase_ip_range(v_str):
    # Input example: 127.0.0.1-2, 134.56.55.1
    # Output example: [127.0.0.1, 127.0.0.2, 134.56.55.1]
    L = []
    v_str = v_str.strip()
    v_str = v_str.replace(';', ',')
    tmp = v_str.split(',')

    for i, key in enumerate(tmp):
        tmp[i] = key.strip()

    try:
        for key in tmp:         #127.0.0.1-3
            ip = match_ip(key)  #127.0.0.1
            if ip:
                if '-' in key: #This is a range
                    last_oct = ip_last_octet(ip)    #1
                    range_end = ip_range_end(key[len(ip):len(key)]) #3
                    if last_oct and range_end and (last_oct < range_end):
                        while last_oct <= range_end:
                            new_ip = ip_network_part(ip) + '.' + str(last_oct)
                            L.append(new_ip)
                            last_oct += 1
                    else:
                        logging.error("Incorrect IP range - %s", key)
                else:
                    L.append(ip)
    except Exception as e:
        # print type(e).__name__
        return None
    return L


def match_ip(v_str):
    try:
        m = re.search(r'([0-9]{0,3}[.][0-9]{0,3}[.][0-9]{0,3}[.][0-9]{0,3})', v_str)
        if m:
            try:
                socket.inet_aton(m.group(1))
                return m.group(1)
            except Exception as e:
                logging.error("Socket - this is not a correct IP - %s", v_str)
                return None
        else:
            logging.error("No ip found in string - %s", v_str)
            return None
    except Exception as e:
        logging.error("can't match Ip address - %s", v_str)
        print type(e).__name__
        return None

def ip_last_octet(v_str):
    i = v_str.rfind('.')
    try:
        if i >= 0:
            s = v_str[i+1 : len(v_str)]
            return int(s)
        else:
            logging.error("Last octet is not found - %s", v_str)
            return None
    except Exception as e:
        logging.error("This is not a valid integer - %s", v_str)
        return None

def ip_network_part(v_str):
    i = v_str.rfind('.')
    if i >= 0:
        s = v_str[0:i]
        return s
    else:
        logging.error("Network part is not found - %s", v_str)
        return None


def ip_range_end(v_str):
    i = v_str.rfind('-')
    try:
        if i >= 0:
            s = v_str[i+1 : len(v_str)]
            return int(s)
        else:
            logging.error("Last octet is not found - %s", v_str)
            return None
    except Exception as e:
        logging.error("This is not a valid integer - %s", v_str)
        return None

