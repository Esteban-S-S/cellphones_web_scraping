from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

personal = pd.read_csv('personal/celulares_personal.csv')
musimundo = pd.read_csv('musimundo/celulares_musimundo.csv')
claro = pd.read_csv('claro/celulares_claro.csv')



companies_df = pd.concat([personal,musimundo,claro])


class Celular(BaseModel):
    modelo: str

@app.get("/celulares/{modelo}")
async def get_celular_details(modelo: str):
    comparacion = {}
    for _, row in companies_df.iterrows():
        if modelo.lower() in row["model"].lower():
            empresa = row["company"]
            comparacion[empresa] = {
                "modelo": row['model'],
                "precio": row["price"],
                "ram": row["ram"],
                "procesador": row["processor"],
                "camara": row["camera"]
            }

    if not comparacion:
        comparacion["error"] = "Modelo no encontrado en ninguna empresa"

    return comparacion
