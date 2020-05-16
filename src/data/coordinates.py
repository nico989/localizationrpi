import math
import numpy
import socket
import ast
from codecs import decode
from mathOperation import degToRad, truncate

class LLH:
    def __init__(self, lat=0.0, lon=0.0, alt=0.0):
        self._lat =  lat
        self._lon = lon
        self._alt = alt
    
    @property
    def lat(self):
        return self._lat
    
    @lat.setter 
    def lat(self, value):
        self._lat = value

    @property
    def lon(self):
        return self._lon
    
    @lon.setter 
    def lon(self, value):
        self._lon = value

    @property
    def alt(self):
        return self._alt
    
    @alt.setter 
    def alt(self, value):
        self._alt = value
    
    def __str__(self):
        coord = 'latitude: ' + str(self._lat) + ' longitude: ' + str(self._lon) + ' altitude: ' + str(self._alt)
        return coord

class XYZ:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self._x = x
        self._y = y
        self._z = z
    
    @property
    def x(self):
        return self._x
    
    @x.setter 
    def x(self, value):
        self._x = value
    
    @property
    def y(self):
        return self._y
    
    @y.setter 
    def y(self, value):
        self._y = value
    
    @property
    def z(self):
        return self._z
    
    @z.setter 
    def z(self, value):
        self._z = value
    
    def __str__(self):
        coord = 'x: ' + str(self._x) + ' y: ' + str(self._y) + ' z: ' + str(self._z)
        return coord

class Coordinates:
    def __init__(self):
        self._port = 5000
        self._ip = '192.168.1.69'
        self._llh = []
        self._xyz = []
        self._rad = 6378137.0
        self._f = 1.0 / 298.257224
    
    def setIP(self, value):
        self._ip = value
    
    def _geodeticToECEF(self):
        for llh in self._llh:
            cosLat = numpy.cos(degToRad(llh.lat))
            sinLat = numpy.sin(degToRad(llh.lat))
            cosLon = numpy.cos(degToRad(llh.lon))
            sinLon = numpy.sin(degToRad(llh.lon))
            C = 1.0 / math.sqrt(cosLat * cosLat + (1 - self._f) * (1 - self._f) * sinLat * sinLat)
            S = (1.0 - self._f) * (1.0 - self._f) * C
            x = (self._rad * C + llh.alt) * cosLat * cosLon
            y = (self._rad * C + llh.alt) * cosLat * sinLon
            z = (self._rad * S + llh.alt) * sinLat
            xyz = XYZ(x, y, z)
            self._xyz.append(xyz)

    def _ECEFToENU(self):
        positions = []
        for xyz in self._xyz:
            x = -numpy.sin(degToRad(self._llh[0].lon)) * (xyz.x - self._xyz[0].x) + numpy.cos(degToRad(self._llh[0].lon)) * (xyz.y- self._xyz[0].y)
            y = -numpy.sin(degToRad(self._llh[0].lat))*numpy.cos(degToRad(self._llh[0].lon)) * (xyz.x - self._xyz[0].x) - numpy.sin(degToRad(self._llh[0].lat))*numpy.sin(degToRad(self._llh[0].lon)) * (xyz.y - self._xyz[0].y) + numpy.cos(degToRad(self._llh[0].lat)) * (xyz.z - self._xyz[0].z)
            z = numpy.cos(degToRad(self._llh[0].lat))*numpy.cos(degToRad(self._llh[0].lon)) * (xyz.x - self._xyz[0].x) + numpy.cos(degToRad(self._llh[0].lat))*numpy.sin(degToRad(self._llh[0].lon)) * (xyz.y - self._xyz[0].y) + numpy.sin(degToRad(self._llh[0].lat)) * (xyz.z - self._xyz[0].z)
            pos = XYZ(truncate(x, 3), truncate(y, 3), truncate(z, 3))
            positions.append(pos)
        return positions
    
    def getLLH(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((self._ip, self._port))
        data = ast.literal_eval(decode(server.recv(1024), 'utf-8'))
        llh = LLH(data['latitude'], data['longitude'], data['altitude'])
        server.close()
        self._llh.append(llh)

    def positions(self):
        self._geodeticToECEF()
        return self._ECEFToENU()  
