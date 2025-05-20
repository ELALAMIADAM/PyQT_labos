#https://www.geeksforgeeks.org/how-to-make-calculator-using-kivy-python/

import kivy 
from kivy.app import App

kivy.require('1.9.0')

from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '400')

class Calculatrice(GridLayout):
    def compute(self,calcul):
        if calcul:
            try:
                # display result in entry (cf. calculatrice.kv)
                self.display.text = str(eval(calcul))
            except Exception:
                self.display.text = "Error"

class CalculatriceApp(App):  
    def build(self):
        return Calculatrice()
  
if __name__ == "__main__" :
    app = CalculatriceApp()
    app.run()

