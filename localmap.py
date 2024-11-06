import math

# setting range of map for testing purposes
MIN = 100 # for both x and y
MAX = -100
STEP = 20 # intervals that cones snap to
num_of_cones = 100
radius = 30

map = {}
in_range = []
checking = [] # for graph plotting
car = (0, 0)

print(f"radius: {radius}")
print(f"step: {STEP}")

'''
^
map of cones, key is (x, y) of interval cones snap to, value is list of cones in that interval
e.g 
(40, 20) : [(43.2, 29.1), (40.1, 20.5)]

---

to find the interval of a cone, you round down to the nearest multiple of STEP, 
e.g -43.2 -> -50, 29.1 -> 20
'''

# functions
def round_down(x, interval=1):
    return int((x // interval) * interval)
    
def find_a_pythagoras(b, c): # find a in pythagoras theorem a^2 + b^2 = c^2
    '''
    use this function to find what range of x values are in range of a given y value 
    (for a circle, as y moves futher from origin of cirle, the x interval/width of circle decreases)
    '''
    if c**2 < b**2: # if c is smaller than b (delta y), then the max val a (delta x) can be is c (radius)
        return 0
    return (c**2 - b**2) ** (1/2)

def unzip_tuples(pairs):
    return [x[0] for x in pairs], [x[1] for x in pairs]

def get_distance_between_coords(point1, point2):
    delta_y = point1[1] - point2[1]
    delta_x = point1[0] - point2[0]
    return (delta_x**2 + delta_y**2)**(1/2)

def coords_within_range(a, b, range):
    return range >= get_distance_between_coords(a, b)

##### setup #####

# generate test data
import random

cones = []

for _ in range(num_of_cones):
    cones.append((random.uniform(MIN, MAX), random.uniform(MIN, MAX)))

# add cones to map
for cone in cones:
    x, y = cone[0], cone[1]
    map.setdefault((round_down(x, STEP), round_down(y, STEP)), []).append(cone)

# show all cones in map
# for key, val in map.items():
#     print(f"{key}: {val}")

# generate random car coordinates
car = (random.uniform(MIN, MAX), random.uniform(MIN, MAX))
print(f"Car is at: {car}")

##### main loop #####

min_y_snap = round_down(car[1] - radius, STEP)
max_y_snap = round_down(car[1] + radius, STEP)

for y_snap in range(min_y_snap, max_y_snap + STEP, STEP):
    y_reach = abs(y_snap - car[1])
    x_maxreach = find_a_pythagoras(y_reach, radius)

    # search along y level for x values in range
    min_x_snap = round_down(car[0] - x_maxreach, STEP)
    max_x_snap = round_down(car[0] + x_maxreach, STEP)
    for x_snap in range(min_x_snap, max_x_snap + STEP, STEP):
        checking.append((x_snap, y_snap))
        # check cones individually if edge snap-point
        if (x_snap, y_snap) in map.keys() and (y_snap in {min_y_snap, max_y_snap} 
                                                or x_snap in {min_x_snap, max_x_snap}):
            for cone in map[(x_snap, y_snap)]:
                if coords_within_range(car, cone, radius):
                    in_range.append(cone)
        # otherwise guarenteed in range, so add all cones in interval
        elif (x_snap, y_snap) in map.keys():
            in_range = in_range + map[(x_snap, y_snap)]

# plot points
import matplotlib.pyplot as plt

cones_xs, cones_ys = unzip_tuples(cones)
cones_inRange_xs, cones_inRange_ys = unzip_tuples(in_range)
check_snapPoints_xs, check_snapPoints_ys = unzip_tuples(checking)

plt.scatter(cones_xs, cones_ys)
plt.scatter(cones_inRange_xs, cones_inRange_ys, c="red")
plt.scatter(check_snapPoints_xs, check_snapPoints_ys, c="yellow", alpha=0.5)
plt.scatter([car[0]], [car[1]], c="black")

circle = plt.Circle((car[0], car[1]), radius, color='blue', fill=False, linewidth=2)
plt.gca().add_artist(circle)

plt.show()
