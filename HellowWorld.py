import random
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pymysql.cursors
import math

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


size = 10

pressure = [([random.uniform(-1.0, 1.0) for x in range(size)]) for y in range(size)]

center = int(size / 2)


def gradient(p):
    """Compute gradient

    It tries to compute gradient.
    """
    connection_flow = pymysql.connect(host='localhost',
                                      user='root',
                                      password='root',
                                      db='python_test_db',
                                      charset='utf8mb4',
                                      cursorclass=pymysql.cursors.DictCursor)
    size_y = len(p)
    size_x = len(p[0])

    try:
        with connection_flow.cursor() as cursor_flow:
            sql_flow = "DELETE FROM `flow` WHERE `idflow`>%s"
            cursor_flow.execute(sql_flow, 0)
            connection_flow.commit()
            for x in range(1, size_x - 1):  # avoid boundaries
                for y in range(1, size_y - 1):
                    # Create a new record
                    v_x = (p[x + 1][y] - p[x - 1][y]) / 2
                    v_y = (p[x][y + 1] - p[x][y - 1]) / 2
                    sql_flow = "INSERT INTO `flow` (`i`, `j`, `vx`, `vy`) VALUES (%s, %s, %s, %s)"
                    cursor_flow.execute(sql_flow, (x, y, v_x, v_y))
            connection_flow.commit()

        # connection is not autocommit by default. So you must commit to save
        # your changes.

    except:
        print('Error on writing the database.')
    finally:
        connection_flow.close()


# gradient(pressure, 2)
# Quiver plot
# import matplotlib.pyplot as plt
# import numpy as np
# X = np.arange(-10, 10, 1)
# Y = np.arange(-10, 10, 1)
# U, V = np.meshgrid(X, Y)
# x, y position, flow_x matrix, flow_y matrix
# q = ax.quiver(X, Y, U, V)
# ax.quiverkey(q, X=0.3, Y=1.1, U=10,
#              label='Quiver key, length = 10', labelpos='E')


def get_vx(size_x, size_y):
    connection_flow = pymysql.connect(host='localhost',
                                      user='root',
                                      password='root',
                                      db='python_test_db',
                                      charset='utf8mb4',
                                      cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection_flow.cursor() as cursor_flow:
            sql_flow = "SELECT `vx` FROM `flow`"
            cursor_flow.execute(sql_flow)
            result_flow = cursor_flow.fetchall()
            return [[result_flow[i]["vx"] for i in range(size_y)] for j in range(size_x)]
    except:
        print('An error occurred in function get_vx')
    finally:
        connection_flow.close()


def get_vy(size_x, size_y):
    connection_flow = pymysql.connect(host='localhost',
                                      user='root', password='root', db='python_test_db', charset='utf8mb4',
                                      cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection_flow.cursor() as cursor_flow:
            sql_flow = "SELECT `vy` FROM `flow`"
            cursor_flow.execute(sql_flow)
            result_flow = cursor_flow.fetchall()
            return [[result_flow[i]["vy"] for i in range(size_y)] for j in range(size_x)]
    except:
        print('An error occurred in function get_vy')
    finally:
        connection_flow.close()


figure(num=None, figsize=(20, 5), dpi=80, facecolor='w', edgecolor='k')
# # FIGURE 1
# for x in range(len(pressure[0])):
#     for y in range(len(pressure)):
#         pressure[x][y] = -((x-center)**2 + (y-center)**2)**0.5
#
# gradient(pressure)
# vx = get_vx(len(pressure)-2, len(pressure[0])-2)
# vy = get_vy(len(pressure)-2, len(pressure[0])-2)
#
# ax = plt.subplot(1, 4, 1)
# q = ax.quiver(list(range(1, size-1)), list(range(1, size-1)), vx, vy)
#
# # # FIGURE 2
# for x in range(size):
#     for y in range(size):
#         pressure[x][y] = -((x-center)**2 + (y-center)**2)
#
# gradient(pressure)
# vx = get_vx(len(pressure)-2, len(pressure[0])-2)
# vy = get_vy(len(pressure)-2, len(pressure[0])-2)
# ax = plt.subplot(1, 4, 2)
# q = ax.quiver(list(range(1, size-1)), list(range(1, size-1)), vx, vy)
#
# # FIGURE 3
# for x in range(size):
#     for y in range(size):
#         if center == x and center == y:
#             pressure[x][y] = 0
#         else:
#             pressure[x][y] = -1/(((x-center)**2 + (y-center)**2)**0.5)
#
# gradient(pressure)
# vx = get_vx(len(pressure)-2, len(pressure[0])-2)
# vy = get_vy(len(pressure)-2, len(pressure[0])-2)
# ax = plt.subplot(1, 4, 3)
# q = ax.quiver(list(range(1, size-1)), list(range(1, size-1)), vx, vy)

# # FIGURE 4
print("Center:", center)
for x in range(size):
    for y in range(size):
        if x == 0 & y == 0:
            pressure[x][y] = 0
        else:
            pressure[x][y] = float(1/math.sqrt(y*y+x*x))

gradient(pressure)
vx = get_vx(len(pressure)-2, len(pressure[0])-2)
vy = get_vy(len(pressure)-2, len(pressure[0])-2)
ax = plt.subplot(1, 4, 4)
q = ax.quiver(list(range(1, size-1)), list(range(1, size-1)), vx, vy)

# Show figures
plt.show()

file_object = open("filename.txt", "w+")
file_object.write("I created an non empty file. Please note that THIS sentence makes THIS sentence true.")
file_object.close()

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='python_test_db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
except:
    print('An error occurred.')
finally:
    connection.close()


