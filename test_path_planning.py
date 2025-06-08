import requests
import json

def test_path_planning():
    # Test parameters
    data = {
        "fieldWidth": 25,
        "fieldHeight": 20,
        "coverageRadius": 5,
        "startX": 0,
        "startY": 0
    }
    
    # Make request to the path planning endpoint
    response = requests.post('http://localhost:5000/path-plan', json=data)
    
    if response.status_code == 200:
        result = response.json()
        path = result['path']
        
        print("\nPath Planning Results:")
        print(f"Field Size: {data['fieldWidth']}x{data['fieldHeight']} meters")
        print(f"Coverage Radius: {data['coverageRadius']} meters")
        print(f"Start Point: ({data['startX']}, {data['startY']})")
        print(f"\nGenerated Path Points: {len(path)}")
        print("\nPath Coordinates:")
        for i, point in enumerate(path):
            print(f"Point {i+1}: ({point['x']}, {point['y']})")
    else:
        print(f"Error: {response.json().get('error', 'Unknown error')}")

if __name__ == "__main__":
    test_path_planning() 