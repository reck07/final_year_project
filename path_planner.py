import numpy as np
# import matplotlib.pyplot as plt # Removed matplotlib
# import io # Removed io
# import base64 # Removed base64
import networkx as nx
from scipy.spatial import KDTree
from scipy.interpolate import splprep, splev

class PathPlanner:
    def __init__(self, field_size=(100, 100)):
        """Initialize the path planner with field dimensions."""
        self.field_width, self.field_height = field_size
        self.obstacles = []
        self.graph = None
        self.spraying_patterns = {
            'zigzag': self._zigzag_pattern,
            'spiral': self._spiral_pattern,
            'custom': self._custom_pattern
        }

    def add_obstacle(self, x, y, radius):
        """Add an obstacle to the field."""
        self.obstacles.append({
            'x': x,
            'y': y,
            'radius': radius
        })

    def is_valid_point(self, x, y):
        """Check if a point is within the field and not in an obstacle."""
        # Check field boundaries with a small margin
        margin = 1.0
        if not (margin <= x <= self.field_width - margin and margin <= y <= self.field_height - margin):
            return False
        
        # Check obstacles
        for obstacle in self.obstacles:
            distance = np.sqrt((x - obstacle['x'])**2 + (y - obstacle['y'])**2)
            if distance < obstacle['radius']:
                return False
        
        return True

    def _zigzag_pattern(self, start_point, coverage_radius):
        """Generate a zigzag pattern for spraying."""
        x, y = start_point
        row_spacing = coverage_radius * 1.2
        num_rows = int(self.field_height / row_spacing) + 1
        path = []
        
        for row in range(num_rows):
            y = row * row_spacing
            if row % 2 == 0:
                x_points = np.arange(0, self.field_width + coverage_radius/2, coverage_radius/2)
            else:
                x_points = np.arange(self.field_width, -coverage_radius/2, -coverage_radius/2)
            
            row_points = [(x, y) for x in x_points if self.is_valid_point(x, y)]
            path.extend(row_points if row % 2 == 0 else reversed(row_points))
        
        return path

    def _spiral_pattern(self, start_point, coverage_radius):
        """Generate a spiral pattern for spraying."""
        x, y = start_point
        path = []
        angle = 0
        radius = coverage_radius
        max_radius = max(self.field_width, self.field_height)
        
        while radius < max_radius:
            x_new = x + radius * np.cos(angle)
            y_new = y + radius * np.sin(angle)
            
            if self.is_valid_point(x_new, y_new):
                path.append((x_new, y_new))
            
            angle += 0.1
            radius += coverage_radius / (2 * np.pi)
        
        return path

    def _custom_pattern(self, start_point, coverage_radius):
        """Generate a custom pattern based on field characteristics."""
        # Create a grid of potential points
        x_points = np.arange(0, self.field_width, coverage_radius/2)
        y_points = np.arange(0, self.field_height, coverage_radius/2)
        points = [(x, y) for x in x_points for y in y_points if self.is_valid_point(x, y)]
        
        # Use KDTree for efficient nearest neighbor search
        tree = KDTree(points)
        
        # Start from the given point
        current_point = start_point
        path = [current_point]
        remaining_points = set(points)
        
        while remaining_points:
            # Find nearest valid point
            distances, indices = tree.query([current_point], k=1)
            next_point = points[indices[0]]
            
            if next_point in remaining_points:
                path.append(next_point)
                remaining_points.remove(next_point)
                current_point = next_point
            else:
                break
        
        return path

    def optimize_spraying_pattern(self, start_point=(0, 0), coverage_radius=10, pattern='zigzag', 
                                spraying_rate=None, smooth_path=True):
        """Generate an optimized spraying pattern with the specified parameters."""
        try:
            if coverage_radius <= 0:
                raise ValueError("Coverage radius must be positive")
            
            x, y = start_point
            if not self.is_valid_point(x, y):
                raise ValueError("Start point is not valid (outside field or in obstacle)")
            
            # Generate base path using selected pattern
            if pattern not in self.spraying_patterns:
                raise ValueError(f"Invalid pattern. Choose from: {list(self.spraying_patterns.keys())}")
            
            path = self.spraying_patterns[pattern](start_point, coverage_radius)
            
            if len(path) < 2:
                raise ValueError("Could not generate valid path with given parameters")
            
            # Apply path smoothing if requested
            if smooth_path:
                path = self._smooth_path(path)
            
            # Convert path points to list of dictionaries with spraying rate
            path_points = []
            for x, y in path:
                point = {
                    'x': float(x),
                    'y': float(y),
                    'spraying_rate': spraying_rate if spraying_rate is not None else 1.0
                }
                path_points.append(point)
            
            return path_points
            
        except Exception as e:
            print(f"Error in optimize_spraying_pattern: {e}")
            raise

    def _smooth_path(self, path, smoothing_factor=0.5):
        """Smooth the path using spline interpolation."""
        if len(path) < 3:
            return path
        
        # Convert path to numpy arrays
        x = np.array([p[0] for p in path])
        y = np.array([p[1] for p in path])
        
        # Fit spline
        tck, u = splprep([x, y], s=smoothing_factor)
        
        # Generate smooth path
        u_new = np.linspace(0, 1, len(path) * 2)
        x_new, y_new = splev(u_new, tck)
        
        # Convert back to list of tuples and filter invalid points
        smooth_path = [(x, y) for x, y in zip(x_new, y_new) if self.is_valid_point(x, y)]
        
        return smooth_path

    def visualize_path(self, path, coverage_radius):
        """Create a simple text-based visualization of the path."""
        try:
            if not path:
                return "No path to visualize."

            # Create a simple grid representation
            grid_width = int(self.field_width) + 1
            grid_height = int(self.field_height) + 1
            grid = [['.' for _ in range(grid_width)] for _ in range(grid_height)]

            # Mark path points on the grid
            for point in path:
                x, y = int(point['x']), int(point['y'])
                if 0 <= x < grid_width and 0 <= y < grid_height:
                    grid[y][x] = 'X'

            # Mark start and end points
            start_x, start_y = int(path[0]['x']), int(path[0]['y'])
            end_x, end_y = int(path[-1]['x']), int(path[-1]['y'])
            if 0 <= start_x < grid_width and 0 <= start_y < grid_height:
                grid[start_y][start_x] = 'S'
            if 0 <= end_x < grid_width and 0 <= end_y < grid_height:
                grid[end_y][end_x] = 'E'

            # Convert grid to a string representation
            visualization_str = "\n".join([" ".join(row) for row in reversed(grid)])

            # Add basic information
            visualization_str = f"Field Size: {self.field_width}x{self.field_height} | Coverage Radius: {coverage_radius}\n" + visualization_str

            return visualization_str

        except Exception as e:
            print(f"Error in visualize_path: {e}")
            return f"Error generating visualization: {e}"

    def plan_path(self, start, end):
        """Plan path using A* algorithm."""
        try:
            path = nx.astar_path(self.graph, start, end)
            return path
        except nx.NetworkXNoPath:
            return None

    def grid_to_graph(self):
        """Convert the field grid to a graph for path planning."""
        self.graph = nx.grid_2d_graph(self.field_width, self.field_height)
        
        # Remove nodes that are in obstacles
        for obstacle in self.obstacles:
            for x in range(max(0, int(obstacle['x'] - obstacle['radius'])), 
                         min(self.field_width, int(obstacle['x'] + obstacle['radius'] + 1))):
                for y in range(max(0, int(obstacle['y'] - obstacle['radius'])), 
                             min(self.field_height, int(obstacle['y'] + obstacle['radius'] + 1))):
                    if (x - obstacle['x'])**2 + (y - obstacle['y'])**2 <= obstacle['radius']**2:
                        if (x, y) in self.graph:
                            self.graph.remove_node((x, y))

    def plan_path_with_graph(self, start, end):
        """Plan path using graph-based approach."""
        self.grid_to_graph()
        return self.plan_path(start, end) 