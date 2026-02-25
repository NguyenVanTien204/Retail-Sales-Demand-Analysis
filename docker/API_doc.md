# Retail Demand Forecasting API

A compact FastAPI demo for sampling the prepared retail dataset and running predictions from either the LightGBM or XGBoost model.

## Available Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| / | GET | Basic hello payload plus active model name. |
| /health | GET | Simple readiness probe. |
| /data/summary | GET | Dataset stats with feature/target column lists. |
| /data/sample | GET | Tail sample of the prepared dataset with optional date filters. |
| /predict | POST | Run inference on sampled internal data or custom records. |

/predict accepts either:
-
ecords: list of dictionaries matching the feature schema, or
- limit + optional start_date/end_date to reuse the stored parquet slice (Dashboard/data/test_data.parquet).

## Local Development

`ash
# Pick the variant you want to test locally
pip install -r docker/requirements.lightgbm.txt  # or requirements.xgboost.txt

# Set the active model before starting FastAPI
export MODEL_VARIANT=lightgbm  # Linux/macOS
set MODEL_VARIANT=lightgbm     # Windows PowerShell

uvicorn docker.app:app --reload --host 0.0.0.0 --port 8080
`

## Docker Images Per Model

Each model has its own Dockerfile so the images stay lean:

`ash
# LightGBM service
docker build -f docker/Dockerfile.lightgbm -t forecast-lightgbm .
docker run --rm -p 8080:8080 forecast-lightgbm

# XGBoost service
docker build -f docker/Dockerfile.xgboost -t forecast-xgboost .
docker run --rm -p 8080:8080 forecast-xgboost
`

> Need GPU acceleration for XGBoost retraining? Replace the base image inside Dockerfile.xgboost with an NVIDIA CUDA runtime (for example
nvidia/cuda:12.2.0-runtime-ubuntu22.04) and start the container with --gpus all.
