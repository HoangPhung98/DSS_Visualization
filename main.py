import numpy as np
from tkinter import *
from graphics import *
def drawGraph(matrix, n):
    jams_color = np.full((5, 5), 255)

    for x in node_info:
        c = Circle(Point(x[2],x[3]), 30)
        c.setFill("blue")
        c.draw(window)
        node_name = Text(Point(x[2],x[3]), x[0])
        node_name.setSize(30)
        node_name.draw(window)


        # draw edge, distance cost
        i = x[1]
        for j in range(n):
            if i != j and matrix[i][j]<1000:
                line = Line(Point(node_info[i][2], node_info[i][3]), Point(node_info[j][2], node_info[j][3]))

                #jam detect
                if jams[i][j][0]!=-1:
                    jams_color[i][j] = max(jams_color[i][j] - 255 * jams[i][j][1],0)
                    line.setWidth(5)
                    line.setOutline(color_rgb(255,np.int32(jams_color[i][j]),0))

                line.draw(window)
                text_point = Point(np.abs(node_info[i][2] + node_info[j][2]) / 2, np.abs(node_info[i][3] + node_info[j][3]) / 2)
                text = Text(text_point, matrix[i][j])
                text.setSize(20)
                text.draw(window)
def drawDirectionPanel(panel_width):

    panel_area = Rectangle(Point(w-panel_width, 0), Point(w,h))
    panel_area.setFill(color_rgb(110, 119, 240))
    panel_area.setOutline("white")
    panel_area.draw(window)

    source_ibbox.setSize(20)
    source_ibbox.setFill("white")
    source_ibbox.draw(window)

    dest_ibbox.setSize(20)
    dest_ibbox.setFill("white")
    dest_ibbox.draw(window)

    bt_rect_find = Rectangle(Point(w - panel_width +30, 150 + panel_padding * 2), Point(w - 30, 150 + panel_padding * 2 + 35))
    bt_rect_find.setFill(color_rgb(75, 86, 235))
    bt_rect_find.draw(window)
    text_bt_find = Text(bt_rect_find.getCenter(), "Find path")
    text_bt_find.draw(window)


def find_min(result_matrix, unvisited, n):
    min = 1000
    index_min = unvisited[0]
    for i in unvisited:
        if(i!=-1):
            if result_matrix[i][0]<min:
                min = result_matrix[i][0]
                index_min = i

    return index_min

def find_path(matrix, n, source, dest):
    visited = np.zeros(n)
    unvisited = np.arange(0,n)
    result_matrix = np.full((5,2), 1000)
    for i in range(n):
        result_matrix[i][1]=i
    result_matrix[source][0] = 0
    print(result_matrix)

    for i in range(n):
        current_city = find_min(result_matrix, unvisited, n)
        unvisited[current_city]=-1
        visited[current_city]=1
        for j in unvisited:
            if j!=-1:
                if matrix[current_city][j]>0 and matrix[current_city][j]<1000:
                    if result_matrix[current_city][0]+matrix[current_city][j]<result_matrix[j][0]:
                        result_matrix[j][0] = result_matrix[current_city][0]+matrix[current_city][j] #update shortest path
                        result_matrix[j][1] = current_city #update prev city
    print(result_matrix)

    return result_matrix


def drawResultPath(result_matrix, source, dest):
    current_city = dest
    prev_city = result_matrix[dest][1]
    while prev_city != source:
        line = Line(Point(node_info[current_city][2],node_info[current_city][3]), Point(node_info[prev_city][2], node_info[prev_city][3]))
        line.setFill(color_rgb(52, 235, 140))
        line.setWidth(5)
        line.draw(window)

        current_city = prev_city
        prev_city = result_matrix[current_city][1]

    line = Line(Point(node_info[current_city][2], node_info[current_city][3]), Point(node_info[prev_city][2], node_info[prev_city][3]))
    line.setFill(color_rgb(52, 235, 140))
    line.setWidth(5)
    line.draw(window)

def dijkstra(matrix, n):
    drawGraph(matrix, n)
    drawDirectionPanel(panel_width)

    while True:
        mouse = window.getMouse()
        if mouse.getX() > w-panel_width+30 and mouse.getX() < w -30 and mouse.getY() > 150 and mouse.getY() < 185:
            window.update()
            drawGraph(matrix, n)

            source = ord(source_ibbox.getText().upper())-65
            dest= ord(dest_ibbox.getText().upper())-65
            result_matrix = find_path(matrix, n, source, dest)

            drawResultPath(result_matrix, source, dest)

        else:
            mouse = window.getMouse()


# data
matrix = [[0, 6, 1000, 1, 1000],
          [6, 0, 5, 2, 2],
          [1000, 5, 0, 1000, 5],
          [1, 2, 1000, 0, 1],
          [1000, 2, 5, 1, 0]]
    # [jam area, muy, v]
jams = [[(-1, 0.4, 0.5),(1, 0.1, 0.6),(2, 0.8,0.15),(1, 0.7,0.12),(0, 0.5, 0.3)],
        [(1, 0.1, 0.6),(-1, 0, 0),(-1, 0.8,0.15),(1, 0.7,0.12),(-1, 0.5, 0.3)],
        [(2, 0.8,0.15),(-1, 0.8,0.15),(-1, 0,0),(-1, 0.7,0.12),(-0, 0.5, 0.3)],
        [(1, 0.7,0.12),(1, 0.7,0.12),(-1, 0.7,0.12),(-1, 0, 0),(-1, 0.5, 0.3)],
        [(0, 0.5, 0.3),(-1, 0.5, 0.3),(-0, 0.5, 0.3),(-1, 0.5, 0.3),(-1, 0, 0)],
       ]
jams_color = np.full((5,5), 255)
node_info = [('A', 0,50,50), ('B', 1,200,50), ('C', 2,400, 200), ('D', 3,50, 400), ('E', 4,200, 400)]

#var
w = 800
h = 600
panel_width = 200
panel_padding = 2
source_ibbox = Entry(Point(w - panel_width // 2 - panel_padding, 30 + panel_padding * 2), 12)
dest_ibbox = Entry(Point(w - panel_width // 2 - panel_padding, 100 + panel_padding * 2), 12)
window = GraphWin("graph", w, h)


dijkstra(matrix, 5)
