# M5 Forecasting on BigQuery

## 1. Project Overview

This project focuses on building a large-scale time series forecasting pipeline using the M5 Forecasting dataset, with BigQuery as the central data warehouse and processing engine.

The main objectives are:

* Designing a scalable data pipeline for large-scale time series data
* Performing feature engineering directly in BigQuery
* Applying and comparing classical statistical models (ARIMA/SARIMA) with tree-based machine learning models
* Evaluating trade-offs between accuracy, scalability, and operational complexity in a real-world business context

The project is designed from a Data Engineer and Data Analyst perspective, emphasizing not only model performance but also data architecture, scalability, and production readiness.

---

## 2. Dataset: M5 Forecasting

The M5 Forecasting dataset simulates real-world retail sales data from Walmart in the United States. It includes:

* Daily sales data
* More than 30,000 time series (item × store combinations)
* Product, store, state, and category metadata
* Calendar information such as holidays, events, and SNAP indicators

Key characteristics:

* Large volume, well-suited for BigQuery
* Long time horizons with strong seasonality patterns
* Presence of exogenous variables (calendar events, pricing)

---

## 3. System Architecture

```
Raw CSV Files (M5 Dataset)
        ↓
BigQuery Raw Tables
        ↓
BigQuery Cleaned & Feature Tables
        ↓
Query / Export
        ↓
Model Training (ARIMA / SARIMA / Tree-based)
        ↓
Evaluation and Comparison
```

BigQuery serves as the backbone of the system, handling:

* Storage of large-scale datasets
* Joins and aggregations over tens of millions of rows
* Batch feature engineering
* Reducing preprocessing load on downstream Python workflows

---

## 4. Data Modeling in BigQuery

Main tables:

* `sales_train`: daily sales data
* `calendar`: date-level calendar and event information
* `prices`: item prices by store and week
* `dim_item`, `dim_store`: dimension tables

Design principles:

* Clear separation between fact and dimension tables
* Date-based partitioning
* Clustering by `item_id` and `store_id`
* Avoiding unnecessary full-table scans

---

## 5. Feature Engineering

Feature engineering is primarily performed in BigQuery to ensure scalability.

Time-based features:

* Day of week, week number, month
* Weekend indicators
* Holiday and event flags

Lag and rolling statistics:

* Lag features (7, 14, 28 days)
* Rolling mean and rolling standard deviation (7, 14, 28 days)

Price-related features:

* Price changes
* Price momentum

Moving feature engineering upstream into BigQuery allows the pipeline to scale efficiently as the number of time series increases.

---

## 6. Models

### 6.1 ARIMA and SARIMA

Purpose:

* Establishing interpretable baselines
* Understanding trend and seasonality patterns

Characteristics:

* Trained per individual time series
* Suitable for stable and less volatile series
* Computationally expensive when scaled to thousands of series

Role in the project:

* Baseline comparison
* Model interpretability and diagnostic analysis

---

### 6.2 Tree-based Models

Models include:

* Random Forest
* Gradient Boosting (e.g., XGBoost, if applicable)

Characteristics:

* Reformulates forecasting as a supervised learning problem
* Effectively leverages lag and rolling features
* Scales better than classical statistical models

Rationale:

* Tree-based models are widely adopted in production environments
* They offer a strong balance between performance and operational cost

---

## 7. Model Evaluation

Evaluation metrics:

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)
* Optional extensions: MAPE, WRMSSE

High-level comparison:

| Model Type | Accuracy    | Scalability | Interpretability |
| ---------- | ----------- | ----------- | ---------------- |
| ARIMA      | Medium      | Low         | High             |
| SARIMA     | Medium–High | Low         | High             |
| Tree-based | High        | High        | Medium           |

---

## 8. Results and Observations

* BigQuery significantly reduces preprocessing time for large datasets
* ARIMA and SARIMA are useful for analysis but difficult to scale
* Tree-based models provide better performance in large-scale retail forecasting
* Data architecture decisions are as important as model selection

---

## 9. Future Improvements

* Experimenting with BigQuery ML
* Evaluating Prophet or deep learning models (LSTM, Temporal Fusion Transformer)
* Automating the pipeline using Airflow
* Building dashboards for forecast monitoring

---

## 10. Learning Outcomes

* Working with large-scale time series data
* Designing data warehouse schemas for forecasting use cases
* Understanding trade-offs between classical and modern forecasting models
* Approaching forecasting problems with a production-oriented mindset

---

This project is an educational and practical simulation of real-world retail forecasting workflows.
