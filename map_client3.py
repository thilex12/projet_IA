import pandas as pd
import folium

def write_json(df, path):
    df.to_json(path)

def read_json(path):
    return pd.read_json(path)

def csv_to_json(csv_path, json_path):
    df = pd.read_csv(csv_path)
    return df.to_json(json_path)

# csv_to_json('Data_Arbre.csv', 'data.json')


df_json = read_json('data.json')

def carte_to_htlm(json):
    map = folium.Map(location=[48.8566, 2.3522], zoom_start=12)
    
    
    return map.save('map.html')    

test = carte_to_htlm(df_json)

# test