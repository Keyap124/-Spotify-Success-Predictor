# Spotify Success Predictor

## Overview

Spotify Success Predictor is a machine learning and data engineering project designed to predict the popularity of songs on Spotify using audio features, artist metadata, and track-level information. The project combines Spotify API integration, SQL database design, data cleaning, feature engineering, and predictive modeling to better understand the factors that contribute to streaming success.

Using Python and the Spotify Web API, metadata such as track names, artist popularity, release dates, and genres was collected and stored inside a structured relational SQL database. Since Spotify no longer publicly provides audio feature data through its API, a supplemental Kaggle dataset containing features such as danceability, energy, tempo, loudness, valence, and acousticness was integrated into the workflow.

After cleaning and organizing the datasets, the information was merged into a final machine learning dataset used to train predictive models. The project primarily uses Random Forest Regression to model nonlinear relationships between musical characteristics and Spotify popularity scores.

The final model achieved:

* **R² Score:** 0.852
* **RMSE:** 10.36

The analysis revealed that artist popularity, danceability, energy, loudness, and tempo were among the strongest predictors of streaming success.

---

## Features

* Spotify API integration using Python
* Automated metadata collection workflows
* Relational SQL database design using SQLite
* Data cleaning and preprocessing pipelines
* Feature engineering and dataset merging
* Machine learning with Random Forest Regression
* Predictive analytics for Spotify popularity
* Feature importance analysis

---

## Technologies Used

* Python
* Spotify Web API
* SQLite
* Pandas
* Scikit-learn
* Kaggle Datasets
* SQL

---

## Dataset Information

The project combines:

1. Spotify API metadata
2. Public Kaggle audio feature datasets

The dataset includes:

* Track popularity
* Artist popularity
* Genres
* Danceability
* Energy
* Tempo
* Loudness
* Acousticness
* Instrumentalness
* Valence
* Speechiness
* Release date information

---

## Machine Learning

The project evaluates predictive performance using:

* Random Forest Regression
* Linear Regression

Evaluation metrics include:

* Root Mean Squared Error (RMSE)
* R² Score

---

## Future Improvements

* Expand dataset size across multiple years
* Integrate playlist and social media metrics
* Experiment with advanced ML models such as XGBoost or Neural Networks
* Build an interactive dashboard for popularity prediction visualization
* Deploy the model as a web application

---

## Goal

The purpose of this project is not only to predict Spotify popularity scores, but also to better understand how streaming platforms, artist recognition, and musical characteristics influence listener behavior and music trends.
