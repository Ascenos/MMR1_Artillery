# könnte auch landscape heißen
import numpy as np
import random, math
from PyQt5.QtGui import QImage

# TODO: Kollisionserkennung anhand des Y-Arrays

class Terrain:
    """Für die Modellierung der Landschft. Speichern und generieren des Arrays, Zeichnen, Kollisionserkennung"""
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def generateByLegendrePolynome(self):  # könnte man aus Deus Version übernehmen
        pass

    def generateByFourierSynthesis(self, amplitude=0.1, averageGroundZero=0.75):
        """Generiert das Y-Array des Terrain per Fourir Synthese (Sinus und so)"""
        self.xArr = np.linspace(0, 1, self.width)
        self.yArr = np.zeros(self.width) + averageGroundZero  # liegt am Ende als Array der Y-Werte der Funktion vor
                                                              # (höchster Punkt des Terrain an dieser Stelle)
        fraktalerExponent = 0.5

        for k in range(1, 5):  # in jeder Iteration wird eine Sinus Funktion mit entsprechenden Zufallsvariablen aufaddiert
            phasenVerschiebung = random.random() * 2*math.pi
            streckFaktor = amplitude * random.random() ** (1/k**fraktalerExponent)
            tempX = k*self.xArr * 2*math.pi + phasenVerschiebung
            addY = streckFaktor * np.sin(tempX)
            self.yArr += addY


    def generateQImage(self):  # TODO: Farbe ersetzen
        """Generiert aus dem Y-Array ein QImage"""
        startC = [10,10,10,255]  # Anfangsfarbe
        endC = [200,130,50,255]  # Endfarbe
        pixmap = np.zeros([self.height, self.width, 4], dtype=np.uint8)
                # erster Index: von oben nach unten, 2. Index: von links nach rechts, 3. Index: RGBA
        for i in range(len(self.yArr)):  # jede Spalte. Lässt sich mit numpy vermutlich eleganter lösen TODO: numpy
            num = max(0, (1-self.yArr[i])*self.height+1)  # Anzahl Pixel
            arr = np.asarray([np.linspace(max,min,num,dtype=np.uint8) for min,max in zip(startC,endC)]).transpose()  # erstellt Farbverlauf
            pixmap[max(0,int(self.height*self.yArr[i])):self.height, i, :] = arr
                # in jeder Spalte werden alle Pixel von unten bis zum Y Wert gefärbt
        self.img = QImage(pixmap, self.width, self.height, QImage.Format_RGBA8888)

    def drawImage(self, qpainter):
        qpainter.drawImage(0, 0, self.img)

    def steigung(self, x):
        x = round(x)
        if (0<x<self.width):
            return self.height*(self.yArr[x+1] - self.yArr[x-1])/2

    def surfaceY(self, x):
        return round(self.height*self.yArr[round(x)])

if __name__ == "__main__":
    pass
