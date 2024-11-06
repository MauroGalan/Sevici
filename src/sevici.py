from coordenadas import *
from typing import NamedTuple
import csv

Estacion = NamedTuple("Estacion",[
    ("nombre",str),
    ("bornetas",int),
    ("bornetas_vacias",int),
    ("bicis_disponibles",int),
    ("ubicacion",Coordenadas)
])

def lee_estaciones(ruta: str) -> list[Estacion]:
    """
    Recibe una ruta de tipo str, y devuelve una lista de tuplas de tipo Estacion.
    La función lee un ficher csv de la ruta indicada y devuelve la información en la lista.
    """
    with open (ruta,encoding="utf-8") as f:
        res = []
        lector = csv.reader(f)
        next(lector)
        for name,slots,empty_slots,free_bikes,latitude,longitude in lector:
            slots= int(slots)
            empty_slots= int(empty_slots)
            free_bikes= int(free_bikes)
            coordenadas= Coordenadas(float(latitude),float(longitude))
            tupla= Estacion(name,slots,empty_slots,free_bikes,coordenadas)
            res.append(tupla)
        return res
    
def estaciones_bicis_libres(estaciones: list[Estacion], k: int = 5):
    """
    Estaciones que tienen bicicletas libres
    
    ENTRADA: 
      :param estaciones: lista de estaciones disponibles 
      :type estaciones: [Estacion(str, int, int, int, Coordenadas(float, float))]
      :param k: número mínimo requerido de bicicletas
      :type k: int
    SALIDA: 
      :return: lista de estaciones seleccionadas
      :rtype: [(int, str)] 
    
    Toma como entrada una lista de estaciones y un número k.
    Crea una lista formada por tuplas (número de bicicletas libres, nombre)
    de las estaciones que tienen al menos k bicicletas libres. La lista
    estará ordenada por el número de bicicletas libres.
    """
    res = []
    for estacion in estaciones:
        if estacion.bicis_disponibles >= k:
            res.append((estacion.bicis_disponibles,estacion.nombre))
    res.sort(reverse=True)
    return res

def estaciones_bicis_libres_g (estaciones: list[Estacion], k: int=5):
    """Versión usando generador"""
    #Sintaxis del generador
    #Expresion_Generadora for elem in secuencia if condicion
    res = [(estacion.bicis_disponibles,estacion.nombre) for estacion in estaciones if estacion.bicis_disponibles >= k]
    res.sort(reverse=True)
    return res

def total_bicis_estaciones(estaciones: list[Estacion], nombrec: str) -> int:
    """
    Devuelve cuántas bicis hay en total en todas las estaciones cuyo nombre contenga nombre_calle
    
    suma = 0
    for estacion in estaciones:
        if nombrec in estacion.nombre:
            suma += estacion.bicis_disponibles
    """
    suma = sum(estacion.bicis_disponibles for estacion in estaciones if nombrec in estacion.nombre)
    return suma

def estaciones_cercanas (estaciones: list[Estacion], coordenadas: Coordenadas, k=5) -> list[tuple[float,str,int]]:
    """
    Estaciones cercanas a un punto dado
    
    ENTRADA: 
      :param estaciones: lista de estaciones disponibles
      :type estaciones: [Estacion(str, int, int, int, Coordenadas(float, float))]
      :param coordenadas: coordenadas formada por la latitud y la longitud de un punto
      :type coordenadas: Coordenadas(float, float)
      :param k: número de estaciones cercanas a calcular 
      :type k: int
    SALIDA: 
      :return: Una lista de tuplas con la distancia, nombre y bicicletas libres de las estaciones seleccionadas 
      :rtype: [(float, str, int)] 
    
    Toma como entrada una lista de estaciones,  las coordenadas de  un punto y
    un valor k.
    Crea una lista formada por tuplas (distancia, nombre de estación, bicicletas libres)
    con las k estaciones con bicicletas libres más cercanas al punto dado, ordenadas por
    su distancia a las coordenadas dadas como parámetro.
    """
    estacionl = []
    for estacion in estaciones:
        if estacion.bicis_disponibles > 0:
            distancia = calcular_distancia(estacion.ubicacion,coordenadas)
            estacionl.append(distancia,estacion.nombre,estacion.bicis_disponibles)
    estacionl.sort()
    return estacionl[:k]

def estaciones_cercanas_g (estaciones: list[Estacion], coordenadas: Coordenadas, k=5) -> list[tuple[float,str,int]]:
    return sorted([calcular_distancia(estacion.ubicacion,coordenadas),estacion.nombre,estacion.bicis_disponibles] for estacion in estaciones if estacion.bicis_disponibles > 0)[:k]

def estacion_con_mas_bicis(estaciones: list[Estacion], coordenadas: Coordenadas, umbral: float) -> Estacion:
    """
    Devuelve la estación con más bicis disponibles de entre las que están a menos deistancia que "umbral" de "coordenadas
    """
    filtrado = []
    for estacion in estaciones:
        if calcular_distancia(estacion.ubicacion, coordenadas) < umbral:
            filtrado.append(estacion)
    return max(filtrado, key= lambda estacion: estacion.bicis_disponibles)

def estacion_con_mas_bicicletas_g(estaciones: list[Estacion], coordenadas: Coordenadas, umbral: float) -> Estacion:
    return max((estacion for estacion in estaciones if calcular_distancia(estacion.ubicacion,coordenadas) < umbral), key = lambda estacion:estacion.bicis_disponibles)