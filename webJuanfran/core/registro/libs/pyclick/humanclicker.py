import pyautogui
from core.registro.libs.pyclick.humancurve import HumanCurve
from random import randint, uniform
from time import sleep

def setup_pyautogui():
    # Any duration less than this is rounded to 0.0 to instantly move the mouse.
    pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
    # Minimal number of seconds to sleep between mouse moves.
    pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
    # The number of seconds to pause after EVERY public function call.
    pyautogui.PAUSE = 0.015  # Default: 0.1

setup_pyautogui()

class HumanClicker():
    def __init__(self):
        pass

    def move(self, toPoint, duration, humanCurve=None):
        fromPoint = pyautogui.position()
        if not humanCurve:
            humanCurve = HumanCurve(fromPoint, toPoint)

        pyautogui.PAUSE = duration / len(humanCurve.points)
        for point in humanCurve.points:
            pyautogui.moveTo(point)

    def click(self):
        pyautogui.click()

    def real_click(self):
        #Para implementar miss-click, != 1
        # Elimino el missclick poniendo un random mayor a 0
        if randint(1, 150) > 0:
            sleep(23 / randint(83,201))
            pyautogui.click()
        else:
            tmp_rand = randint(1, 11)
            if tmp_rand < 10:
                #double click
                print("Misclick dobleClick")
                pyautogui.click()
                sleep(randint(23, 113) / 1000)
                pyautogui.click()
            elif tmp_rand == 10:
                print("Misclick Fold")
                sleep(randint(23, 113) / 1000)
                pyautogui.click(button = 'right',  duration = 0.2)

    def aleatorio(self):
        # realiza un movimiento aleatorio por la pantalla
        if randint(1, 50) == 1:
            x, y = pyautogui.size()
            i = randint(1,10)
            if i <= 3:
                x = randint(1, x)
            else:
                x = randint(1, x) + randint(0, 1980)
            y = randint(y/2, y-100)
            self.move((x, y), uniform(0.025, 0.08))
            sleep(43 / randint(107,201))
            print(f"Movimiento aleatorio a: [{x}, {y}]")
        else:
            sleep(23 / randint(107,201))





