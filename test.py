import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np



class point:
    def __init__(self, x, y, z, t=None):
        self.x = x
        self.y = y
        self.z = z
        self.t = str(t)

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y}, z={self.z})"
    

class Cuboid:
    def __init__(self, x, y, z, w, h, d):
        self.x = x  # x-coordinate of the cuboid's corner
        self.y = y  # y-coordinate of the cuboid's corner
        self.z = z  # z-coordinate of the cuboid's corner
        self.w = w  # width of the cuboid
        self.h = h  # height of the cuboid
        self.d = d  # depth of the cuboid

    def contains(self, point):
        """Check if the point lies within this cuboid"""
        return (self.x <= point.x < self.x + self.w and
                self.y <= point.y < self.y + self.h and
                self.z <= point.z < self.z + self.d)
    
    def delete(self, point):
        """Delete a point from this cuboid"""
        return False


class Octree:
    def __init__(self, capacity, cuboid):
        self.capacity = capacity  # max number of points per cunoid
        self.cuboid = cuboid  # the region this octree covers
        self.points = []  # points in this cuboid
        self.divided = False  # flag to see if it's divided or not

    def subdivide(self):
        """Subdivide the cuboid into 8 smaller cuboids"""
        x, y, z, w, h, d = self.cuboid.x, self.cuboid.y, self.cuboid.z, self.cuboid.w, self.cuboid.h, self.cuboid.d

        # create the 8 sub-cuboids
        self.nw_near = Octree(self.capacity, Cuboid(x, y, z, w / 2, h / 2, d / 2))  # Near-top-left
        self.ne_near = Octree(self.capacity, Cuboid(x + w / 2, y, z, w / 2, h / 2, d / 2))  # Near-top-right
        self.sw_near = Octree(self.capacity, Cuboid(x, y + h / 2, z, w / 2, h / 2, d / 2))  # Near-bottom-left
        self.se_near = Octree(self.capacity, Cuboid(x + w / 2, y + h / 2, z, w / 2, h / 2, d / 2))  # Near-bottom-right

        self.nw_far = Octree(self.capacity, Cuboid(x, y, z + d / 2, w / 2, h / 2, d / 2))  # Far-top-left
        self.ne_far = Octree(self.capacity, Cuboid(x + w / 2, y, z + d / 2, w / 2, h / 2, d / 2))  # Far-top-right
        self.sw_far = Octree(self.capacity, Cuboid(x, y + h / 2, z + d / 2, w / 2, h / 2, d / 2))  # Far-bottom-left
        self.se_far = Octree(self.capacity, Cuboid(x + w / 2, y + h / 2, z + d / 2, w / 2, h / 2, d / 2))  # Far-bottom-right

        self.divided = True

        # insert the points into the appropriate child octants
        for point in self.points:
            self.nw_near.insert(point)
            self.ne_near.insert(point)
            self.sw_near.insert(point)
            self.se_near.insert(point)
            self.nw_far.insert(point)
            self.ne_far.insert(point)
            self.sw_far.insert(point)
            self.se_far.insert(point)

            #we do insertion in all sub-cuboid bc if a point isn't supposed to be in a specific space the cuboid will reject it due to an if statement at the start of insert function

        # Clear the points list as they have been moved to the children
        self.points = []

    def insert(self, point):
        """insert a point into this octree"""
        if not self.cuboid.contains(point):
            return False  # point is out of bounds

        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
            return True

        if not self.divided:
            self.subdivide()

        # try inserting the point into one of the 8 child octants
        if self.nw_near.insert(point): return True
        if self.ne_near.insert(point): return True
        if self.sw_near.insert(point): return True
        if self.se_near.insert(point): return True
        if self.nw_far.insert(point): return True
        if self.ne_far.insert(point): return True
        if self.sw_far.insert(point): return True
        if self.se_far.insert(point): return True

        return False
    

    def delete(self, point):
        """Delete a point from this octree"""
        #check if the point is within this cuboid
        if not self.cuboid.contains(point):
            return False

        if point in self.points:
            self.points.remove(point)  #remove the point from the list
            return True

        if self.divided:
            #try deleting the point from one of the 8 child octrees, again we do it for all 8 octrees and if it isn't there it will return false
            if self.nw_near.delete(point): return True
            if self.ne_near.delete(point): return True
            if self.sw_near.delete(point): return True
            if self.se_near.delete(point): return True
            if self.nw_far.delete(point): return True
            if self.ne_far.delete(point): return True
            if self.sw_far.delete(point): return True
            if self.se_far.delete(point): return True

        return False
    
    def query_by_range(self, x_range, y_range, z_range):
        """Query the Octree for points within the given ranges for x, y, and z."""
        results = []

        #check if the current cuboid intersects with the query range on each axis
        if not self._intersects_range(x_range, y_range, z_range):
            return results

        #check all points in the current octree
        for point in self.points:
            if self._is_point_in_range(point, x_range, y_range, z_range):
                results.append(point)

        #if subdivided, search all child octrees
        if self.divided:
            results.extend(self.nw_near.query_by_range(x_range, y_range, z_range))
            results.extend(self.ne_near.query_by_range(x_range, y_range, z_range))
            results.extend(self.sw_near.query_by_range(x_range, y_range, z_range))
            results.extend(self.se_near.query_by_range(x_range, y_range, z_range))
            results.extend(self.nw_far.query_by_range(x_range, y_range, z_range))
            results.extend(self.ne_far.query_by_range(x_range, y_range, z_range))
            results.extend(self.sw_far.query_by_range(x_range, y_range, z_range))
            results.extend(self.se_far.query_by_range(x_range, y_range, z_range))

        return results

    def _intersects_range(self, x_range, y_range, z_range):
        """Check if this Octree's cuboid intersects with the query range."""
        return not (x_range[1] <= self.cuboid.x or
                    x_range[0] >= self.cuboid.x + self.cuboid.w or
                    y_range[1] <= self.cuboid.y or
                    y_range[0] >= self.cuboid.y + self.cuboid.h or
                    z_range[1] <= self.cuboid.z or
                    z_range[0] >= self.cuboid.z + self.cuboid.d)

    def _is_point_in_range(self, point, x_range, y_range, z_range):
        """Check if the point is within the specified ranges."""
        return x_range[0] <= point.x < x_range[1] and \
               y_range[0] <= point.y < y_range[1] and \
               z_range[0] <= point.z < z_range[1]
    

    


import plotly.graph_objects as go

# Function to draw a cuboid
def draw_cuboid(cuboid, color='#0000FF'):
    x, y, z, w, h, d = cuboid.x, cuboid.y, cuboid.z, cuboid.w, cuboid.h, cuboid.d
    # Define the 8 vertices of the cuboid
    vertices = [
        (x, y, z),
        (x + w, y, z),
        (x, y + h, z),
        (x + w, y + h, z),
        (x, y, z + d),
        (x + w, y, z + d),
        (x, y + h, z + d),
        (x + w, y + h, z + d),
    ]

    # Define the edges connecting the vertices
    edges = [
        (0, 1), (1, 3), (3, 2), (2, 0),  # Bottom face
        (4, 5), (5, 7), (7, 6), (6, 4),  # Top face
        (0, 4), (1, 5), (2, 6), (3, 7)   # Vertical edges
    ]

    # Extract x, y, z for each edge
    lines = []
    for edge in edges:
        x_vals = [vertices[edge[0]][0], vertices[edge[1]][0], None]
        y_vals = [vertices[edge[0]][1], vertices[edge[1]][1], None]
        z_vals = [vertices[edge[0]][2], vertices[edge[1]][2], None]
        lines.append((x_vals, y_vals, z_vals))

    return lines


def collect_cuboids(octree, cuboids):
    cuboids.append(octree.cuboid)  # Add current cuboid
    if octree.divided:  # If the octree is divided, collect from children
        collect_cuboids(octree.nw_near, cuboids)
        collect_cuboids(octree.ne_near, cuboids)
        collect_cuboids(octree.sw_near, cuboids)
        collect_cuboids(octree.se_near, cuboids)
        collect_cuboids(octree.nw_far, cuboids)
        collect_cuboids(octree.ne_far, cuboids)
        collect_cuboids(octree.sw_far, cuboids)
        collect_cuboids(octree.se_far, cuboids)






