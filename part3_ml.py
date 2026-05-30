import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

FILE_PATH = "data/spotify_2023_complete_dataset.csv"
TARGET = "track_popularity"
RANDOM_SEED = 42

df_raw = pd.read_csv(FILE_PATH)
df_raw = df_raw.dropna(subset=[TARGET])

df = df_raw.copy()
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['release_year'] = df['release_date'].dt.year.fillna(2023).astype(int)
df['release_month'] = df['release_date'].dt.month.fillna(1).astype(int)

numerical_features = ['danceability','energy','loudness','speechiness','acousticness',
                      'instrumentalness','liveness','valence','tempo','duration',
                      'artist_popularity','release_year','release_month']
categorical_nominal = ['key','mode','time_signature']

num_cols = [c for c in numerical_features if c in df.columns]
cat_cols = [c for c in categorical_nominal if c in df.columns]
features = num_cols + cat_cols

for col in num_cols:
    df[col] = df[col].fillna(df[col].mean())
df = df.dropna(subset=features)

X = df[features]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_SEED)

model = RandomForestRegressor(n_estimators=200, max_depth=20, min_samples_leaf=5,
                              random_state=RANDOM_SEED, n_jobs=-1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"R-squared (R²): {r2:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")

joblib.dump(model, "rf_popularity_model.pkl")
