import math
import time
import pydirectinput as gui
from mumble_link import get_context
from position import Position
from window import WINDOW_NAME, Window

KeyMap_Forword = 'w'


class Player:
    def get_position(self) -> Position:
        ctx, _ = get_context()
        return Position(ctx.playerX, ctx.playerY)

    def move_to(self, target_position: Position):
        prev_position = self.get_position()
        prev_distance = 0

        gui.keyDown(KeyMap_Forword)
        gui.mouseDown(button=gui.RIGHT)

        try:
            while True:
                current_position = self.get_position()
                distance = current_position.distance(target_position)

                if prev_distance != 0 and distance > prev_distance:
                    break
                
                current_degress = current_position.degress(prev_position)
                target_degress = target_position.degress(current_position)
                degress = target_degress - current_degress

                if degress > 180:
                    degress = degress - 360
                if degress < -180:
                    degress = 360 + degress

                print('distance: ', distance, ', degress: ', degress)

                if abs(degress) >= 12:
                    i = 0
                    times = abs(degress) // 12
                    print('times: ', times)
                    if times > 1:
                        gui.keyUp(KeyMap_Forword)
                        gui.mouseUp(button=gui.RIGHT)
                    while i < times:
                        if degress < 0:
                            gui.press(',')
                        else:
                            gui.press('.')
                        i += 1
                    if times > 1:
                        gui.keyDown(KeyMap_Forword)
                        gui.mouseDown(button=gui.RIGHT)
                else:
                    if degress < 0:
                        gui.move(-20)
                    else:
                        gui.move(20)

                if distance <= 5: 
                    break

                prev_position = current_position
                prev_distance = distance
        finally:
            gui.keyUp(KeyMap_Forword)
            gui.mouseUp(button=gui.RIGHT)
        
        return self


if __name__ == "__main__":
    win = Window(WINDOW_NAME)
    win.focus()
    center = win.get_center_position()
    gui.moveTo(center.x, center.y)

    # # gui.keyDown('w')
    # gui.mouseDown(button=gui.RIGHT)
    # time.sleep(1)
    # # i = 0
    # # while i <= 20:
    # #     gui.move(i * 10)
    # #     i = i + 1
    # gui.move(100)
    # # gui.moveRel(30)
    # time.sleep(2)
    # gui.mouseUp(button=gui.RIGHT)
    # gui.keyUp('w')
    # tx, ty = get_position()
    # print('target:', tx, ty)

    player = Player()
    player.move_to(Position(2084.7, 14091.5)).move_to(Position(2117.8, 14145.4))


    # move(2084.7, 14091.5)
    # time.sleep(3)
    # move(2117.8, 14145.4)
    # time.sleep(3)
    # move(2187.2, 14182.3)
    # time.sleep(3)
    # move(2236.7, 14144.6)
    # time.sleep(3)
    # move(2255.7, 14044.1)
    # time.sleep(3)
    # move(2168.5, 13993.1)
    # time.sleep(3)
    # move(2105.2, 14012.5)
    # time.sleep(3)
    # move(2084.7, 14091.5)
    # 57732.9, 40400.8
    # print('pos', x, y)