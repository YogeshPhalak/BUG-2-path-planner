import time

from setup import *
import sys
from buttons import *
from planning_libs import *


def setup():
    global okButton, undoButton, planButton, CPtButton, NFZButton, trajectory, resetButton, nfzs, nutshellButton
    okButton = Button(SCREENSIZE[0] - 50, SCREENSIZE[1] - 30, 40, 20, 'Ok', True)
    undoButton = Button(SCREENSIZE[0] - 140, SCREENSIZE[1] - 30, 80, 20, 'Undo', True)
    planButton = Button(SCREENSIZE[0] - 230, SCREENSIZE[1] - 30, 80, 20, 'Plan', True)
    CPtButton = Button(SCREENSIZE[0] - 420, SCREENSIZE[1] - 30, 180, 20, 'CheckPoints')
    NFZButton = Button(SCREENSIZE[0] - 490, SCREENSIZE[1] - 30, 60, 20, 'NFZ')
    resetButton = Button(SCREENSIZE[0] - 600, SCREENSIZE[1] - 30, 100, 20, 'Reset', True)
    nutshellButton = Button(SCREENSIZE[0] - 770, SCREENSIZE[1] - 30, 160, 20, 'Nutshell')

    trajectory = Trajectory()
    nfzs = []


def loop():
    okButton.draw()
    undoButton.draw()
    planButton.draw()
    CPtButton.draw()
    NFZButton.draw()
    resetButton.draw()
    nutshellButton.draw()
    for n in range(len(nfzs)):
        nfzs[n].draw()
    trajectory.draw()


if __name__ == "__main__":
    setup()

    while True:
        CLOCK.tick(FPS)
        background()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if not trajectory.fixed and CPtButton.pressed:
                    trajectory.add_point(pos[0], pos[1])
                for i in range(len(nfzs)):
                    if not nfzs[i].fixed and NFZButton.pressed:
                        nfzs[i].add_point(pos[0], pos[1])

                if pos[1] > SCREENSIZE[1] - 30:
                    okButton.mouse_cb(pos[0], pos[1])
                    undoButton.mouse_cb(pos[0], pos[1])
                    planButton.mouse_cb(pos[0], pos[1])
                    CPtButton.mouse_cb(pos[0], pos[1])
                    NFZButton.mouse_cb(pos[0], pos[1])
                    resetButton.mouse_cb(pos[0], pos[1])
                    nutshellButton.mouse_cb(pos[0], pos[1])

                    if NFZButton.pressed and not okButton.pressed:
                        nfzs.append(NFZ())
                    elif undoButton.pressed:
                        if len(nfzs) > 0:
                            nfzs.remove(nfzs[-1])
                    elif resetButton.pressed:
                        setup()
                    elif planButton.pressed:
                        trajectory.plan()

                    if okButton.pressed:
                        if CPtButton.pressed:
                            trajectory.generate_trajectory()
                            path = trajectory.get_path()
                            for n in range(len(nfzs)):
                                set0 = nfzs[n].add_trajectory(path)
                                trajectory.add_plan_points(set0)
                                # time.sleep(0.5)
                        elif NFZButton.pressed:
                            for n in range(len(nfzs)):
                                nfzs[n].generate_nfz()

                        undoButton.pressed = False
                        planButton.pressed = False
                        CPtButton.pressed = False
                        NFZButton.pressed = False

                    if nutshellButton.pressed:
                        for n in range(len(nfzs)):
                            nfzs[n].nutshell = True
                    else:
                        for n in range(len(nfzs)):
                            nfzs[n].nutshell = False

        loop()
        pg.display.update()
