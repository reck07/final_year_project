import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def load_data(file_path):
    """Load and preprocess the crop recommendation dataset."""
    try:
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # If file doesn't exist, create a sample dataset
        if not os.path.exists(file_path):
            create_sample_dataset(file_path)
        
        # Load the dataset
        data = pd.read_csv(file_path)
        
        # Split features and target
        X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
        y = data['label']
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test, scaler
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None, None, None

def create_sample_dataset(file_path):
    """Create a sample dataset for crop recommendation."""
    # Sample data for common crops
    data = {
        'N': [90, 85, 60, 50, 70, 80, 65, 75],
        'P': [42, 58, 55, 40, 45, 50, 35, 48],
        'K': [43, 41, 50, 45, 38, 42, 40, 44],
        'temperature': [20.8, 21.7, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0],
        'humidity': [82.0, 80.0, 75.0, 70.0, 65.0, 60.0, 55.0, 50.0],
        'ph': [6.5, 6.7, 6.8, 7.0, 7.2, 7.5, 7.8, 8.0],
        'rainfall': [202.9, 226.7, 242.9, 262.9, 282.9, 302.9, 322.9, 342.9],
        'label': ['rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas', 'mothbeans', 'mungbean', 'blackgram']
    }
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    print(f"Created sample dataset at {file_path}")

def train_model(data_file, model_file):
    """Train and save the crop recommendation model."""
    try:
        # Load and preprocess data
        X_train, X_test, y_train, y_test, scaler = load_data(data_file)
        
        if X_train is None:
            raise Exception("Failed to load data")
        
        # Train the model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Save the model and scaler
        os.makedirs(os.path.dirname(model_file), exist_ok=True)
        joblib.dump(model, model_file)
        joblib.dump(scaler, model_file.replace('.joblib', '_scaler.joblib'))
        
        # Print model accuracy
        train_accuracy = model.score(X_train, y_train)
        test_accuracy = model.score(X_test, y_test)
        print(f"Model trained successfully!")
        print(f"Training accuracy: {train_accuracy:.2f}")
        print(f"Testing accuracy: {test_accuracy:.2f}")
        
        return model, scaler
    except Exception as e:
        print(f"Error training model: {e}")
        return None, None

def load_model(model_file):
    """Load the trained model."""
    try:
        model = joblib.load(model_file)
        print("Model loaded successfully!")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

if __name__ == "__main__":
    # Train the model if run directly
    data_file = "data/crop_data.csv"
    model_file = "models/crop_model.joblib"
    train_model(data_file, model_file)
