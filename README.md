# Cafe Stock Predictor

A Streamlit application that uses AutoGluon machine learning to predict cafe stock demand by combining historical sales data with weather forecasts from the Open-Meteo API.

## Features

- **Demand Forecasting**: Predicts stock requirements for cafe items using AutoGluon
- **Weather Integration**: Incorporates temperature and precipitation data from Open-Meteo API
- **Easy Data Upload**: Simple CSV upload for sales history
- **7-Day Forecast**: Provides predictions for the next week
- **Smart Recommendations**: Highlights items with high predicted demand for tomorrow

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. In the sidebar:
   - Enter your cafe's latitude and longitude (defaults to New York City)
   - Upload a CSV file with your sales history

3. CSV Format:
   - Required columns: `Date`, `Item Name`, `Quantity Sold`
   - Date format: YYYY-MM-DD

4. Click "Train AI" to train the model

5. View predictions:
   - Recommended stock for tomorrow (highlighted)
   - Full 7-day forecast table

## CSV Example

```csv
Date,Item Name,Quantity Sold
2024-01-01,Coffee,150
2024-01-01,Croissant,80
2024-01-02,Coffee,165
2024-01-02,Croissant,75
```

## Model Training

The app uses AutoGluon TabularPredictor with:
- Training time: 60 seconds
- Quality preset: medium_quality
- Features: Item Name, Max Temperature, Precipitation, Day of Week, Is Weekend

Models are saved in the `models/` directory and can be reused for future predictions.

