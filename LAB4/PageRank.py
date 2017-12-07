#!/usr/bin/python

from collections import namedtuple
import time
import sys

class Edge:
    def __init__ (self, origin=None, dest=None):
        self.origin = origin
        self.dest = dest
        self.weight = 0

    def __repr__(self):
        return "edge: {0} {1} {2}".format(self.origin, self.dest, self.weight)

class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight =    # write appropriate value

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)

edgeList = [] # list of Edge
edgeHash = dict() # hash of edge to ease the match
airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport


## AIRPORT FILE:
## [0]: Id OpenFlights airport. :: 1
## [1]: name of the airport.    :: "Goroka"          ----------SE UTILIZA
## [2]: City of airport         :: "Goroka"
## [3]: Country                 :: "Papua New Guinea"----------SE UTILIZA
## [4]: IATA CODE (3 letters)   :: "GKA"             ----------SE UTILIZA
## [5]: OCAO code (4 letters)   :: "AYGA"

##CLASS AIRPORT
## a.name = [1], [3] = "name airport", "Country"
## a.code = [4] = "IATA code"

def readAirports(fd):
    print "Reading Airport file from {0}".format(fd)
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print "There were {0} Airports with IATA code".format(cont)

## ROUTES FILE:
## [0]: airline code.           :: 2B
## [1]: OpenFlights airline code:: 410
## [2]: Origin IATA o ICAO code :: AER                --------SE UTILIZA
## [3]: Destin IATA o ICAO code :: "Papua New Guinea" --------SE UTILIZA

def readRoutes(fd):
    print "Reading Routes file from {0}".format(fd)
    routesTxt = open(fd, "r");
    cont = 0
    for line in routesTxt.readlines():
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')

            aux = temp[2][1:-1]     #IATA origen
            aux2 = temp[3][1:-1]       #IATA destino
            ## Si no se ha añadido aun aeropuerto destino en origen
            if e.origin == aux && e.dest = aux2 for e in edgeList:
                e.weight += 1
            else:
                e = Edge()
                e.origin = aux
                e.dest = aux2
                e.weight = 1
                pair = (aux,aux2)
                edgeHash[pair] = e
        except Exception as inst:
            pass
        else:
            cont += 1
            airportHash[e.name] = a
            a.routes.append(e)
            a.routeHash[e.dest] = e
    routesTxt.close()

def computePageRanks():
    # write your code

def outputPageRanks():
    # write your code

def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    print "#Iterations:", iterations
    print "Time of computePageRanks():", time2-time1


if __name__ == "__main__":
    sys.exit(main())
