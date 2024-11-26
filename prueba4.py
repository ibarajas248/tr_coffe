import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

# Cargar el dataset
df = pd.read_csv("dataset_cafe_10000.csv")

# Seleccionar variables relevantes
X = df[["Precio_anterior", "Calidad", "Temperatura_media"]]
y = df["Demanda"]

# Dividir los datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Guardar el modelo entrenado
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)