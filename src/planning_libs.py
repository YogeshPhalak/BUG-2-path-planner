from setup import *
import numpy as np


class Point:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index


class Trajectory:
    def __init__(self):
        self.fixed = False
        self.points = []
        self.index = 0
        self.fontObj = pg.font.Font('freesansbold.ttf', 8)
        self.textSurfaceObj = None
        self.textRectObj = None
        self.color = RED
        self.sets = None
        self.planned_points = []

    def __del__(self):
        pass

    def add_point(self, x, y):
        if y < SCREENSIZE[1] - 30 and not self.fixed:
            self.points.append(Point(x, y, self.index))
            self.index += 1

    def draw(self):
        if self.fixed:
            self.color = ORANGE
        else:
            self.color = RED

        if len(self.points) > 0:
            pg.draw.circle(DISPSURFACE, self.color, (self.points[0].x, self.points[0].y), 7)

        for i in range(1, len(self.points)):
            pg.draw.line(DISPSURFACE, self.color, (self.points[i - 1].x, self.points[i - 1].y),
                         (self.points[i].x, self.points[i].y), 3)
            pg.draw.circle(DISPSURFACE, self.color, (self.points[i].x, self.points[i].y), 7)

        for i in range(len(self.points)):
            self.textSurfaceObj = self.fontObj.render(str(self.points[i].index), True, BLACK, self.color)
            self.textRectObj = self.textSurfaceObj.get_rect()
            self.textRectObj.center = (self.points[i].x, self.points[i].y)
            DISPSURFACE.blit(self.textSurfaceObj, self.textRectObj)
            DISPSURFACE.blit(self.textSurfaceObj, self.textRectObj)

    def generate_trajectory(self):
        self.fixed = True
        self.planned_points = self.points.copy()

    def get_path(self):
        return self.planned_points

    def add_plan_points(self, sets):
        if sets:
            self.sets = sets
            p0, p1 = self.sets[0], self.sets[-1]
            i0 = min(p0.index[1], p1.index[1])
            i1 = max(p0.index[1], p1.index[1])
            for i in range(i0 + 1, i1 + 1):
                self.planned_points.pop(i0 + 1)

            ''' for optimal results'''
            self.sets.remove(p0)
            self.sets.remove(p1)

            if dist(self.planned_points[i0], p0) > dist(self.planned_points[i0], p1):
                for i in range(len(self.sets)):
                    self.planned_points.insert(i0 + 1, self.sets[i])
            else:
                for i in range(len(self.sets) - 1, -1, -1):
                    self.planned_points.insert(i0 + 1, self.sets[i])

    def plan(self):
        self.points = self.planned_points
        self.correct_indices()

    def correct_indices(self):
        for i in range(len(self.points)):
            self.points[i].index = i


def dist(p0, p1):
    return ((p0.x - p1.x) ** 2 + (p0.y - p1.y) ** 2) ** 0.5


class NFZ:
    def __init__(self):
        self.fixed = False
        self.points = []
        self.outer_points = []
        self.index = 0
        self.color = RED
        self.orn = -1
        self.orn_set = False
        self.generated = False
        self.trajectory = None
        self.intersections = []
        self.nutshell = False

    def add_point(self, x, y):
        if y < SCREENSIZE[1] - 30 and not self.fixed:
            self.points.append(Point(x, y, self.index))
            self.index += 1

        if len(self.points) > 2 and not self.orn_set:
            A = [self.points[1].x - self.points[0].x, self.points[1].y - self.points[0].y]
            B = [self.points[2].x - self.points[1].x, self.points[2].y - self.points[1].y]

            self.orn = -np.sign(A[0] * B[1] - A[1] * B[0])
            self.orn_set = True

    def draw(self):
        if not self.fixed:
            if len(self.points) > 0:
                pg.draw.circle(DISPSURFACE, self.color, (self.points[0].x, self.points[0].y), 5)
            for i in range(1, len(self.points)):
                pg.draw.line(DISPSURFACE, self.color, (self.points[i - 1].x, self.points[i - 1].y),
                             (self.points[i].x, self.points[i].y), 2)
                pg.draw.circle(DISPSURFACE, self.color, (self.points[i].x, self.points[i].y), 5)
        else:
            if len(self.points) > 0:
                s = pg.Surface(SCREENSIZE, pg.SRCALPHA)
                self.color = (255, 0, 0, 75)
                pg.draw.polygon(s, self.color, [(p.x, p.y) for p in self.points])
                self.color = (128, 0, 0, 255)
                pg.draw.polygon(s, self.color, [(p.x, p.y) for p in self.points], 2)
                DISPSURFACE.blit(s, (0, 0))

            if self.nutshell:
                for i in range(len(self.outer_points)):
                    pg.draw.line(DISPSURFACE, BLUE, (self.outer_points[i - 1].x, self.outer_points[i - 1].y),
                                 (self.outer_points[i].x, self.outer_points[i].y), 1)
                    pg.draw.circle(DISPSURFACE, BLUE, (self.outer_points[i].x, self.outer_points[i].y), 3)

                for i in range(len(self.intersections)):
                    pg.draw.circle(DISPSURFACE, WHITE, (self.intersections[i].x, self.intersections[i].y), 5)

                for i in range(0, len(self.intersections), 2):
                    p0, p1 = self.intersections[i], self.intersections[i + 1]

                    for j in range((p1.index[0] - p0.index[0]) % len(self.outer_points)):
                        ind = j + p0.index[0]
                        pg.draw.circle(DISPSURFACE, VIOLET, (
                            self.outer_points[ind % len(self.outer_points)].x,
                            self.outer_points[ind % len(self.outer_points)].y), 5)

                    for j in range((p0.index[0] - p1.index[0]) % len(self.outer_points)):
                        ind = j + p1.index[0]
                        pg.draw.circle(DISPSURFACE, PINK, (
                            self.outer_points[ind % len(self.outer_points)].x,
                            self.outer_points[ind % len(self.outer_points)].y), 5)

    def generate_nfz(self):
        self.fixed = True
        if not self.generated:
            for i in range(len(self.points)):
                A = [self.points[i].x - self.points[i - 1].x, self.points[i].y - self.points[i - 1].y]
                A_p = [-self.orn * NFZ_OFFSET * A[1] / ((A[0] ** 2 + A[1] ** 2) ** 0.5),
                       self.orn * NFZ_OFFSET * A[0] / ((A[0] ** 2 + A[1] ** 2) ** 0.5)]
                B = [self.points[(i + 1) % len(self.points)].x - self.points[i].x,
                     self.points[(i + 1) % len(self.points)].y - self.points[i].y]
                B_p = [-self.orn * NFZ_OFFSET * B[1] / ((B[0] ** 2 + B[1] ** 2) ** 0.5),
                       self.orn * NFZ_OFFSET * B[0] / ((B[0] ** 2 + B[1] ** 2) ** 0.5)]

                a0 = [self.points[i - 1].x + A_p[0], self.points[i - 1].y + A_p[1]]
                b0 = [self.points[i].x + B_p[0], self.points[i].y + B_p[1]]

                X = np.matrix([[A[0], B[0]], [A[1], B[1]]])
                C = np.matrix([[b0[0] - a0[0]], [b0[1] - a0[1]]])
                K = X.getI() * C

                self.outer_points.append(Point(a0[0] + float(K[0]) * A[0], a0[1] + float(K[0]) * A[1], i))
        self.generated = True

    def add_trajectory(self, trajectory):
        self.trajectory = trajectory
        for i in range(len(self.outer_points)):
            for j in range(len(self.trajectory) - 1):
                a0 = [self.outer_points[i - 1].x, self.outer_points[i - 1].y]
                a1 = [self.outer_points[i].x, self.outer_points[i].y]

                A = [a1[0] - a0[0], a1[1] - a0[1]]

                b0 = [self.trajectory[j].x, self.trajectory[j].y]
                b1 = [self.trajectory[j + 1].x, self.trajectory[j + 1].y]

                B = [b1[0] - b0[0], b1[1] - b0[1]]

                X = np.matrix([[A[0], -B[0]], [A[1], -B[1]]])
                C = np.matrix([[b0[0] - a0[0]], [b0[1] - a0[1]]])

                K = X.getI() * C

                if 0 < K[0] < 1 and 0 < K[1] < 1:
                    self.intersections.append(Point(a0[0] + A[0] * float(K[0]), a0[1] + A[1] * float(K[0]), [i, j]))

        for i in range(0, len(self.intersections), 2):
            p0, p1 = self.intersections[i], self.intersections[i + 1]
            set0, set1 = [p0], [p1]
            d0, d1 = 0, 0
            for j in range((p1.index[0] - p0.index[0]) % len(self.outer_points)):
                ind = j + p0.index[0]
                set0.append(self.outer_points[ind % len(self.outer_points)])
                d0 += dist(set0[j], set0[j + 1])
            set0.append(p1)
            d0 += dist(set0[-1], set0[-2])

            for j in range((p0.index[0] - p1.index[0]) % len(self.outer_points)):
                ind = j + p1.index[0]
                set1.append(self.outer_points[ind % len(self.outer_points)])
                d1 += dist(set1[j], set1[j + 1])
            set1.append(p0)
            d1 += dist(set1[-1], set1[-2])

            if d0 > d1:
                return set1[::self.orn]
            else:
                return set0[::-self.orn]
