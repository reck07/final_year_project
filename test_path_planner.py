from path_planner import PathPlanner
import json

def test_path_planning():
    # Test case 1: Basic path planning with realistic dimensions
    planner = PathPlanner(field_size=(100, 100))
    try:
        path = planner.optimize_spraying_pattern(
            start_point=(0, 0),
            coverage_radius=10
        )
        print("Test 1 - Basic path planning:")
        print(f"Number of points: {len(path)}")
        print(f"First point: {path[0]}")
        print(f"Last point: {path[-1]}")
        print("Test 1 passed!\n")
    except Exception as e:
        print(f"Test 1 failed: {e}\n")

    # Test case 2: Path planning with smaller field
    planner = PathPlanner(field_size=(25, 20))
    try:
        path = planner.optimize_spraying_pattern(
            start_point=(0, 0),
            coverage_radius=5
        )
        print("Test 2 - Path planning with smaller field:")
        print(f"Number of points: {len(path)}")
        print(f"First point: {path[0]}")
        print(f"Last point: {path[-1]}")
        print("Test 2 passed!\n")
    except Exception as e:
        print(f"Test 2 failed: {e}\n")

    # Test case 3: Path planning with obstacles
    planner = PathPlanner(field_size=(100, 100))
    planner.add_obstacle(50, 50, 10)  # Add obstacle in the middle
    try:
        path = planner.optimize_spraying_pattern(
            start_point=(0, 0),
            coverage_radius=10
        )
        print("Test 3 - Path planning with obstacles:")
        print(f"Number of points: {len(path)}")
        print(f"First point: {path[0]}")
        print(f"Last point: {path[-1]}")
        print("Test 3 passed!\n")
    except Exception as e:
        print(f"Test 3 failed: {e}\n")

    # Test case 4: Invalid start point
    planner = PathPlanner(field_size=(100, 100))
    try:
        path = planner.optimize_spraying_pattern(
            start_point=(150, 150),  # Outside field
            coverage_radius=10
        )
        print("Test 4 failed: Should have raised an error for invalid start point\n")
    except ValueError as e:
        print("Test 4 - Invalid start point:")
        print(f"Expected error: {e}")
        print("Test 4 passed!\n")

    # Test case 5: Invalid coverage radius
    planner = PathPlanner(field_size=(100, 100))
    try:
        path = planner.optimize_spraying_pattern(
            start_point=(0, 0),
            coverage_radius=-10  # Negative radius
        )
        print("Test 5 failed: Should have raised an error for negative coverage radius\n")
    except ValueError as e:
        print("Test 5 - Invalid coverage radius:")
        print(f"Expected error: {e}")
        print("Test 5 passed!\n")

if __name__ == "__main__":
    test_path_planning() 