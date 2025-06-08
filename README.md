# Smart Farming System Documentation

## Project Overview
This smart farming system is a comprehensive solution that combines crop prediction, path planning for field coverage, and pesticide recommendations. The system uses machine learning and optimization algorithms to help farmers make data-driven decisions.

## System Components

### 1. Crop Prediction System
**Algorithm Steps:**
1. Data Collection
   - Gather soil parameters (N, P, K)
   - Collect environmental data (temperature, humidity, pH, rainfall)
   - Store historical crop data

2. Model Training Process
   - Preprocess data using scaling
   - Train machine learning model
   - Save model and scaler for future predictions

3. Prediction Flow
   - Receive input parameters
   - Scale input data
   - Generate crop recommendations
   - Return prediction results

### 2. Path Planning System
**Algorithm Steps:**
1. Field Analysis
   - Input field dimensions (width, height)
   - Set coverage radius
   - Define start point coordinates

2. Path Generation
   - Create grid-based field representation
   - Calculate optimal coverage points
   - Generate efficient path between points
   - Ensure complete field coverage

3. Coverage Calculation
   - Calculate total distance
   - Compute coverage area
   - Account for overlapping areas
   - Estimate completion time

### 3. Pesticide Recommendation System
**Algorithm Steps:**
1. Input Processing
   - Receive crop type
   - Identify pest type
   - Assess severity level

2. Recommendation Generation
   - Match crop-pest combinations
   - Consider severity levels
   - Generate appropriate recommendations
   - Include application instructions

## API Endpoints

### Authentication
- `/api/auth/register` - User registration
- `/api/auth/login` - User login
- `/api/auth/me` - Get current user info
- `/api/auth/google` - Google OAuth login

### Core Features
- `/predict` - Crop prediction
- `/path-plan` - Field coverage path planning
- `/path-plan/visualize` - Path visualization
- `/api/pesticide-recommendation` - Pesticide recommendations

## Technical Implementation

### Database Structure
- Users table
- Crops table
- Recommendations table

### Security Features
- JWT authentication
- Password hashing
- Google OAuth integration

### Data Processing
1. Input Validation
2. Data Scaling
3. Model Prediction
4. Result Formatting

## Usage Examples

### Crop Prediction
```json
{
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 20.87,
    "humidity": 82.00,
    "ph": 6.50,
    "rainfall": 202.93
}
```

### Path Planning
```json
{
    "fieldWidth": 100,
    "fieldHeight": 100,
    "coverageRadius": 10,
    "startX": 5,
    "startY": 5
}
```

### Pesticide Recommendation
```json
{
    "crop": "rice",
    "pest": "aphids",
    "severity": "medium"
}
```

## Error Handling
- Input validation
- Model loading checks
- Database connection management
- API error responses

## Performance Considerations
- Model caching
- Database indexing
- API response optimization
- Path planning efficiency

## Future Improvements
1. Real-time weather integration
2. Mobile app development
3. Drone control integration
4. Advanced machine learning models
5. Multi-language support

## Setup Instructions
1. Install dependencies
2. Configure environment variables
3. Initialize database
4. Train/load models
5. Start the server

## Environment Variables
```
SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:5000/auth/google/callback
```

## Dependencies
- Flask
- SQLAlchemy
- scikit-learn
- pandas
- numpy
- JWT
- Google OAuth

# Image Text Extractor

This Python script extracts text from images using OCR (Optical Character Recognition) technology.

## Prerequisites

1. Python 3.6 or higher
2. Tesseract OCR engine installed on your system

### Installing Tesseract OCR

#### Windows:
1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer and note the installation path
3. Add the Tesseract installation directory to your system's PATH environment variable

#### Linux:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

#### macOS:
```bash
brew install tesseract
```

## Installation

1. Clone this repository or download the files
2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Create an `images` directory in the same location as the script (it will be created automatically if it doesn't exist)
2. Place your image files (PNG, JPG, JPEG, BMP, or TIFF) in the `images` directory
3. Run the script:
```bash
python ocr_script.py
```

The script will:
- Process all images in the `images` directory
- Extract text from each image
- Display the extracted text in the console
- Save the extracted text to separate text files in the same directory as the script

## Output

For each processed image, a corresponding text file will be created with the naming format:
`[original_image_name]_text.txt`

## Supported Image Formats

- PNG
- JPG/JPEG
- BMP
- TIFF

## Notes

- The quality of text extraction depends on the image quality and clarity
- For best results, use images with clear, well-contrasted text
- The script supports multiple languages if you have the corresponding Tesseract language data installed 

## Step-by-Step Algorithm Guide

### 1. System Initialization
```bash
# Step 1: Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Set up environment variables
# Create .env file with required variables:
SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:5000/auth/google/callback
```

### 2. Database Setup
```bash
# Step 4: Initialize database
python init_db.py
```

### 3. Model Training
```bash
# Step 5: Train the crop prediction model
python train_model.py
```

### 4. Start the Application
```bash
# Step 6: Run the Flask application
python app.py
```

### 5. System Workflow Algorithm

#### A. User Authentication Flow
1. User Registration
   - Input: name, email, password
   - Process: Hash password, create user record
   - Output: JWT token

2. User Login
   - Input: email, password
   - Process: Verify credentials
   - Output: JWT token

#### B. Crop Prediction Flow
1. Data Input
   - Collect soil parameters (N, P, K)
   - Gather environmental data
   - Validate input ranges

2. Model Processing
   - Scale input data
   - Apply prediction model
   - Generate recommendation

3. Result Output
   - Return predicted crop
   - Provide confidence score
   - Display recommendations

#### C. Path Planning Flow
1. Field Setup
   - Input field dimensions
   - Set coverage parameters
   - Define start point

2. Path Generation
   - Create field grid
   - Calculate coverage points
   - Generate optimal path

3. Coverage Analysis
   - Calculate total distance
   - Compute coverage area
   - Estimate completion time

#### D. Pesticide Recommendation Flow
1. Problem Assessment
   - Identify crop type
   - Determine pest type
   - Evaluate severity

2. Recommendation Generation
   - Match crop-pest combinations
   - Consider severity levels
   - Generate treatment plan

3. Output Delivery
   - Provide pesticide options
   - Include application instructions
   - List safety precautions

### 6. Testing the System

#### A. Test Crop Prediction
```bash
# Send POST request to /predict endpoint
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 20.87,
    "humidity": 82.00,
    "ph": 6.50,
    "rainfall": 202.93
  }'
```

#### B. Test Path Planning
```bash
# Send POST request to /path-plan endpoint
curl -X POST http://localhost:5000/path-plan \
  -H "Content-Type: application/json" \
  -d '{
    "fieldWidth": 100,
    "fieldHeight": 100,
    "coverageRadius": 10,
    "startX": 5,
    "startY": 5
  }'
```

#### C. Test Pesticide Recommendation
```bash
# Send POST request to /api/pesticide-recommendation endpoint
curl -X POST http://localhost:5000/api/pesticide-recommendation \
  -H "Content-Type: application/json" \
  -d '{
    "crop": "rice",
    "pest": "aphids",
    "severity": "medium"
  }'
```

### 7. Monitoring and Maintenance

1. System Health Checks
   - Monitor database connections
   - Check model performance
   - Verify API endpoints

2. Regular Maintenance
   - Update dependencies
   - Backup database
   - Retrain models if needed

3. Performance Optimization
   - Monitor response times
   - Optimize database queries
   - Cache frequently used data 

# Smart Farming - Crop Recommendation System

## System Architecture

### Overview
The Crop Recommendation System is a full-stack application that uses machine learning to recommend suitable crops based on soil parameters and environmental conditions. The system consists of three main components:

1. Frontend (React.js)
2. Backend (Flask)
3. Machine Learning Model

### Architecture Diagram
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│    Frontend     │     │    Backend      │     │    Database     │
│    (React.js)   │◄────┤    (Flask)      │◄────┤    (SQLite)     │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        ▲                       ▲
        │                       │
        │                       │
        ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │
│  User Interface │     │  ML Model       │
│                 │     │  (scikit-learn) │
└─────────────────┘     └─────────────────┘
```

### Detailed Technical Architecture

#### 1. Frontend Architecture (React.js)
```
┌─────────────────────────────────────────┐
│              Frontend Layer             │
├─────────────────────────────────────────┤
│ ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│ │  Pages  │  │Components│  │  Hooks  │  │
│ └─────────┘  └─────────┘  └─────────┘  │
├─────────────────────────────────────────┤
│ ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│ │ Services│  │  Utils  │  │ Context │  │
│ └─────────┘  └─────────┘  └─────────┘  │
└─────────────────────────────────────────┘
```

**Components Breakdown:**
- **Pages:**
  - `CropRecommendation.js`: Main recommendation interface
  - `Dashboard.js`: User dashboard
  - `Login.js`: Authentication page
  - `Register.js`: User registration

- **Components:**
  - `InputForm.js`: Parameter input form
  - `RecommendationCard.js`: Display recommendations
  - `Visualization.js`: Data visualization
  - `Navigation.js`: Navigation menu

- **Services:**
  - `api.js`: API communication
  - `auth.js`: Authentication handling
  - `validation.js`: Input validation

- **State Management:**
  - React Context for global state
  - Local state for component-specific data

#### 2. Backend Architecture (Flask)
```
┌─────────────────────────────────────────┐
│              Backend Layer              │
├─────────────────────────────────────────┤
│ ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│ │ Routes  │  │Services │  │ Models  │  │
│ └─────────┘  └─────────┘  └─────────┘  │
├─────────────────────────────────────────┤
│ ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│ │  Utils  │  │  Auth   │  │  ML     │  │
│ └─────────┘  └─────────┘  └─────────┘  │
└─────────────────────────────────────────┘
```

**Components Breakdown:**
- **Routes:**
  - `/api/crop-recommendation`: Crop prediction
  - `/api/auth/*`: Authentication endpoints
  - `/api/pesticide-recommendation`: Pesticide suggestions

- **Services:**
  - `model_service.py`: ML model handling
  - `auth_service.py`: Authentication logic
  - `validation_service.py`: Input validation

- **Models:**
  - `User`: User data model
  - `Crop`: Crop information
  - `Recommendation`: Prediction history

#### 3. Machine Learning Architecture
```
┌─────────────────────────────────────────┐
│            ML Pipeline Layer            │
├─────────────────────────────────────────┤
│ ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│ │  Data   │  │  Model  │  │Predict  │  │
│ │Processing│  │ Training│  │ Engine  │  │
│ └─────────┘  └─────────┘  └─────────┘  │
└─────────────────────────────────────────┘
```

**Components Breakdown:**
- **Data Processing:**
  - Data cleaning
  - Feature scaling
  - Data validation

- **Model Training:**
  - Model selection
  - Hyperparameter tuning
  - Model evaluation

- **Prediction Engine:**
  - Real-time predictions
  - Confidence scoring
  - Result formatting

#### 4. Database Architecture (SQLite)
```
┌─────────────────────────────────────────┐
│            Database Layer               │
├─────────────────────────────────────────┤
│ ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│ │  Users  │  │ Crops   │  │  Recs   │  │
│ └─────────┘  └─────────┘  └─────────┘  │
└─────────────────────────────────────────┘
```

**Schema Design:**
```sql
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crops Table
CREATE TABLE crops (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    optimal_conditions JSON
);

-- Recommendations Table
CREATE TABLE recommendations (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    crop_id INTEGER,
    parameters JSON,
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (crop_id) REFERENCES crops(id)
);
```

#### 5. Security Architecture
```
┌─────────────────────────────────────────┐
│            Security Layer               │
├─────────────────────────────────────────┤
│ ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│ │   JWT   │  │  CORS   │  │ Input   │  │
│ │  Auth   │  │  Policy │  │Validation│  │
│ └─────────┘  └─────────┘  └─────────┘  │
└─────────────────────────────────────────┘
```

**Security Components:**
- JWT Authentication
- CORS Protection
- Input Validation
- Password Hashing
- Rate Limiting

#### 6. API Architecture
```
┌─────────────────────────────────────────┐
│              API Layer                  │
├─────────────────────────────────────────┤
│ ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│ │  REST   │  │  Error  │  │Response │  │
│ │ Endpoints│  │Handling │  │Formatting│  │
│ └─────────┘  └─────────┘  └─────────┘  │
└─────────────────────────────────────────┘
```

**API Endpoints:**
```python
# Authentication
POST /api/auth/register
POST /api/auth/login
GET /api/auth/me

# Crop Recommendation
POST /api/crop-recommendation
GET /api/crop-recommendation/history

# Pesticide Recommendation
POST /api/pesticide-recommendation
```

#### 7. Data Flow Architecture
```
┌─────────┐    ┌─────────┐    ┌─────────┐
│ Frontend│    │ Backend │    │Database │
└────┬────┘    └────┬────┘    └────┬────┘
     │              │              │
     ▼              ▼              ▼
┌─────────┐    ┌─────────┐    ┌─────────┐
│  Input  │    │Process  │    │  Store  │
│Validation│    │ Request │    │  Data   │
└─────────┘    └─────────┘    └─────────┘
```

**Data Flow Steps:**
1. User Input → Frontend Validation
2. API Request → Backend Processing
3. Model Prediction → Result Generation
4. Database Storage → Response Return
5. Frontend Display → User Interface

## Input Parameters
- **Soil Nutrients**:
  - Nitrogen (N): 0-140 mg/kg
  - Phosphorus (P): 0-145 mg/kg
  - Potassium (K): 0-205 mg/kg
- **Environmental Factors**:
  - Temperature: 8-44°C
  - Humidity: 14-100%
  - pH: 3.5-10
  - Rainfall: 20-300 mm

## Security Features
- JWT-based authentication
- Input validation
- CORS protection
- Environment variable configuration

## Dependencies
#### Backend
- Flask
- scikit-learn
- pandas
- numpy
- SQLAlchemy
- PyJWT
- python-dotenv

#### Frontend
- React
- Material-UI
- Axios
- Framer Motion

## Setup Instructions
1. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Start backend server:
   ```bash
   python app.py
   ```

4. Start frontend server:
   ```bash
   cd frontend
   npm start
   ```

## Environment Variables
Create a `.env` file with:
```
SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:5000/auth/google/callback
```

## API Documentation
#### Crop Recommendation
- **Endpoint**: `/api/crop-recommendation`
- **Method**: POST
- **Input**:
  ```json
  {
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 20.87,
    "humidity": 82.00,
    "ph": 6.50,
    "rainfall": 202.93
  }
  ```
- **Output**:
  ```json
  {
    "recommendations": [
      {
        "name": "crop_name",
        "confidence": 0.95,
        "description": "Based on the provided conditions..."
      }
    ]
  }
  ``` 