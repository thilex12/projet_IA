import pandas as pd
import folium

def write_json(df, path):
    df.to_json(path)

def read_json(path):
    return pd.read_json(path)

def csv_to_json(csv_path, json_path):
    df = pd.read_csv(csv_path)
    return write_json(df, json_path)

# csv_to_json('Data_Arbre.csv', 'data.json')


df_json = read_json('data.json')

def carte_to_htlm(json):
    map = folium.Map(zoom_start=12, location=[49.8476780339, 3.2866348474000002])
    
    for i in range(len(json)):
        folium.Circle(
            location = [json.iloc[i]['latitude'], json.iloc[i]['longitude']],
            radius =  (json.iloc[i]['tronc_diam']/3.1415) * 0.1 + 1,
            popup=f'<div style="width : 200px">Position de l\'arbre : {json.iloc[i]['latitude'], json.iloc[i]['longitude']}<br>'
                  f'Remarquable : {json.iloc[i]['remarquable']}<br>'
                  f'Stade de développement : {json.iloc[i]['fk_stadedev']}<br>'
                  f'Etat de l\'arbre : {json.iloc[i]['fk_arb_etat']}<br>'
                  f'Quartier : {json.iloc[i]['clc_quartier']}<br>'
                  f'Secteur : {json.iloc[i]['clc_secteur']}</div>'
            ).add_to(map)
    
    return map.save('map.html')    

test = carte_to_htlm(df_json)

# test