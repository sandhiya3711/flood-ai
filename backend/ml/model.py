import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os

class FloodModel:
    def __init__(self):
        self.model = None
        self._train_mock_model()

    def _train_mock_model(self):
        """
        Trains a simple Random Forest on synthetic data that mimics EM-DAT attributes.
        """
        print("Training Flood Prediction Model on Synthetic Data...")
        
        # 1. Generate Synthetic Data
        # Features: rainfall_1h (mm), water_level (ft), terrain_slope (deg), drainage_capacity (0-1)
        # Target: Risk Level (0: Low, 1: Moderate, 2: High, 3: Critical)
        
        data_size = 1000
        rainfall = np.random.uniform(0, 150, data_size)
        water_level = np.random.uniform(0, 30, data_size)
        terrain_slope = np.random.uniform(0, 45, data_size)
        drainage = np.random.uniform(0.1, 1.0, data_size)
        
        # Simple Logic to define Ground Truth for training
        # Risk is high if Rain is High AND Water Level is High OR Drainage is Bad
        risk = []
        for r, w, t, d in zip(rainfall, water_level, terrain_slope, drainage):
            score = (r * 0.5) + (w * 2.0) - (d * 50) + (t * 0.2)
            
            if score > 80:
                risk.append(3) # Critical
            elif score > 60:
                risk.append(2) # High
            elif score > 40:
                risk.append(1) # Moderate
            else:
                risk.append(0) # Low
                
        df = pd.DataFrame({
            "rainfall": rainfall,
            "water_level": water_level,
            "terrain_slope": terrain_slope,
            "drainage": drainage,
            "risk": risk
        })
        
        # 2. Train Model
        X = df[["rainfall", "water_level", "terrain_slope", "drainage"]]
        y = df["risk"]
        
        self.model = RandomForestClassifier(n_estimators=10)
        self.model.fit(X, y)
        print("Model Training Complete.")

    def predict_risk(self, rainfall, water_level, terrain_slope=10, drainage=0.5):
        """
        Predicts flood risk level.
        Returns: String (Low, Moderate, High, Critical)
        """
        if not self.model:
            return "Error: Model not trained"
            
        input_data = pd.DataFrame([{
            "rainfall": rainfall,
            "water_level": water_level,
            "terrain_slope": terrain_slope,
            "drainage": drainage
        }])
        
        prediction = self.model.predict(input_data)[0]
        
        risk_map = {0: "Low", 1: "Moderate", 2: "High", 3: "Critical"}
        return risk_map.get(prediction, "Unknown")

model_instance = FloodModel()
