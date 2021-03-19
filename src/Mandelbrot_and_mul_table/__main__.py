from math import pi, sin, cos
from random import random
from OpenGL.GL import *
import glfw

width, height = 920, 920
degree_table = 6
amon = 400
colors = [(random(), random(), random()) for _ in range(amon)]


def float_range(start, stop, step):
    """
    Generator
     Args:
         start: the number at which the sequence starts
         stop: the number to which the sequence continues
         step: step
     Yields:
         present value
    """
    while start <= stop:
        yield start
        start += step


def create_coords_oval(amount_points, radius_x, radius_y):
    """
    Generator of coordinates of points that form an ellipse.
     Args:
         amount_points: number of points
         radius_x: first axis of the ellipse (goes through the focuses of the ellipse)
         radius_y: the second axis of the ellipse (perpendicular to the first axis, passes through its center)
    """
    angle_factor = 360 / amount_points
    radians_factor = pi / 180
    for value in float_range(0, 360, angle_factor):
        yield radius_x * cos(value * radians_factor), radius_y * sin(value * radians_factor), 0


def create_table_values(degree):
    """
    Multiplication table value generator
     Args:
         degree: column number of the multiplication table
    """
    for value in range(10):
        yield value * degree


def create_set_colors(amount):
    for _ in range(amount):
        yield random(), random(), random()


def draw_points(set_coords):
    """
    Draw points
     Args:
         set_coords: set of coordinates
    """
    glPointSize(9)
    # glEnable(GL_POINT_SMOOTH)
    glBegin(GL_POINTS)

    for coords in set_coords:
        glColor3d(1, 1, 0)
        glVertex3d(*coords)
    glEnd()


def draw_oval(set_coords):
    """
    Draw an ellipse
     Args:
         set_coords: set of coordinates
    """
    glLineWidth(4)
    glBegin(GL_LINE_LOOP)

    for coords in set_coords:
        glColor3d(1, 0, 0)
        glVertex3d(*coords)
    glEnd()


def mathematical_calculation(set_coords, degree, amount_points):
    """
    Generator of start and end coordinates of points.
     Args:
         set_coords: set of coordinates of points of the circle
         degree: multiplication table column (by 2, 3, ...)
         amount_points: number of points
    """
    i = 0
    for coord in set_coords:
        # Todo: shitty list binding! Redo!
        yield coord, set_coords[(degree * i) % amount_points]
        i += 1


def draw_lines(set_coords):
    """
    Draw lines
     Args:
         set_coords: set of coordinates
    """

    glLineWidth(2)
    glBegin(GL_LINES)

    for elem, color in zip(set_coords, colors):
        glColor3d(*color)
        glVertex3d(*elem[0])
        glVertex3d(*elem[1])
    glEnd()


def enable_rave_mode():
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT)
    glRotatef(0.4, 0.1, 0.5, 0.5)


def main():
    # Инициализация библиотеки
    if not glfw.init():
        return

    # включение MSAA
    glfw.window_hint(glfw.SAMPLES, 4)

    # Создание окна оконного режима и его контекста OpenGL
    window = glfw.create_window(width, height, "Times Table and Mandelbrot set", None, None)
    if not window:
        glfw.terminate()
        return

    # Делаем контекст окна текущим
    glfw.make_context_current(window)

    # Цикл, пока пользователь не закроет окно
    while not glfw.window_should_close(window):
        global degree_table
        # Выполните рендеринг здесь, например используя pyOpenGL

        # enable_rave_mode()

        draw_oval(create_coords_oval(100, .8, .8))

        amount_points = amon
        coords_points = list(create_coords_oval(amount_points, .8, .8))

        draw_lines(list(mathematical_calculation(coords_points, degree_table, amount_points)))
        draw_points(coords_points)
        # degree_table += 1

        # Поменять местами передний и задний буферы
        glfw.swap_buffers(window)

        # Опрос и обработка событий
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
