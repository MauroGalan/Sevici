import math

#from collections import namedtuple
#Coordenadas = namedtuple("Coordenadas","latitud,longitud")

#Namedtuple pero con tipos en los campos
from typing import NamedTuple

Coordenadas = NamedTuple("Coordenadas",[("latitud",float),("longitud",float)])

def calcular_distancia(c1: Coordenadas,c2: Coordenadas) -> float:
    return math.sqrt((c1.latitud-c2.latitud)**2-(c1.longitud-c2.longitud)**2)
