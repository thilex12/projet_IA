import pandas as pd
import folium
import pickle as pk
import branca.colormap as cm
import requests
import datetime
import sys

if len(sys.argv) > 1:
    date = str(sys.argv[1])
else:
    date = datetime.date.today()

def write_json(df, path):
    df.to_json(path)

def read_json(path):
    return pd.read_json(path)

def csv_to_json(csv_path, json_path):
    df = pd.read_csv(csv_path)
    return write_json(df, json_path)

# csv_to_json('Data_Arbre.csv', 'data.json')


# "model":feat_forest,
# "features":top_features,
# "scaler":scaler,
# "hot":hot, 
# "categorielle":categorielle,
# "numerique":numerique,
# "binaire":['remarquable']


def prediction(df, pkl_path):
    dic = pk.load(open(pkl_path, 'rb'))
    
    #Données numérique
    data_num_scaled = dic['scaler'].transform(df[dic['numerique']])
    data_num_scaled = pd.DataFrame(data_num_scaled,columns=dic['numerique'])

    #Données categorielle
    hot_df = pd.DataFrame(dic['hot'].transform(df[dic["categorielle"]]), columns=dic['hot'].get_feature_names_out(dic['categorielle']))
    
    #Données binaire
    
    #Remarquable ou non
    data_bin = df[dic['binaire']]
    data_bin.loc[data_bin["remarquable"] == "Oui", "remarquable"] = 1
    data_bin.loc[data_bin["remarquable"] != 1, "remarquable"] = 0
    data_bin.remarquable = data_bin.remarquable.astype(int)
    
    X = pd.concat([data_num_scaled, hot_df, data_bin], axis=1)
    
    # X = df.drop("fk_arb_etat", axis=1)
    X = X[dic['features']]
    
    prediction = pd.DataFrame(dic['model'].predict(X), columns=["prediction"])
    prediction_proba = pd.DataFrame(dic['model'].predict_proba(X), columns=["prediction_proba_1","prediction_proba_0"])
    

    
    return pd.concat([df, prediction, prediction_proba], axis=1)
    # return pd.concat([df, prediction], axis=1)



def proba_wind(windgust, data):
    data["proba_wind"] = data["prediction_proba_0"]
    if (windgust > 128):
        data.loc[data["prediction_proba_0"] > 0.3, "proba_wind"] = 1
    elif (windgust > 117):
        data.loc[data["prediction_proba_0"] > 0.4, "proba_wind"]  = 1
    elif (windgust > 102):
        data.loc[data["prediction_proba_0"] > 0.5, "proba_wind"]  = 1
    elif (windgust > 88):
        data.loc[data["prediction_proba_0"] > 0.6, "proba_wind"]  = 1
    elif (windgust > 74):
        data.loc[data["prediction_proba_0"] > 0.7, "proba_wind"]  = 1
    elif (windgust > 61):
        data.loc[data["prediction_proba_0"] > 0.8, "proba_wind"]  = 1
    elif (windgust > 49):
        data.loc[data["prediction_proba_0"] > 0.9, "proba_wind"]  = 1
    return data



def carte_to_htlm(json, pkl_dic, date = datetime.date.today()):
    json = prediction(json, pkl_dic)

    windgust = val_api(date)
    json = proba_wind(windgust, json)

    map = folium.Map(zoom_start=12, location=[49.8476780339, 3.2866348474000002])
    colormap = cm.LinearColormap(colors=['green', 'red'], vmin=0, vmax=1)
    map.add_child(colormap)
    groupe1 = folium.FeatureGroup(name = "Arbre abattu sans météo", show = True).add_to(map)
    groupe2 = folium.FeatureGroup(name = f"Arbre abattu avec météo du {date}", show = False).add_to(map)
    
    for i in range(len(json)):

        #Sans prise en compte du vent
        folium.Circle(
            location = [json.iloc[i]['latitude'], json.iloc[i]['longitude']],
            radius =  (json.iloc[i]['tronc_diam']/3.1415) * 0.1 + 1,
            color = colormap(json.iloc[i]['prediction_proba_0']),
            fill = True,
            popup=f'<div style="width : 200px">Position de l\'arbre : {json.iloc[i]['latitude'], json.iloc[i]['longitude']}<br>'
                  f'Remarquable : {json.iloc[i]['remarquable']}<br>'
                  f'Stade de développement : {json.iloc[i]['fk_stadedev']}<br>'
                  f'Etat de l\'arbre : {json.iloc[i]['fk_arb_etat']}<br>'
                  f'Quartier : {json.iloc[i]['clc_quartier']}<br>'
                  f'Secteur : {json.iloc[i]['clc_secteur']}<br>'
                  f'Probabilité que l\'arbre soit à abattre : {format(json.iloc[i]['prediction_proba_0'],'.2f')}</div>'
            ).add_to(groupe1)
        
        #Prise en compte du vent à Saint Quentin
        folium.Circle(
            location = [json.iloc[i]['latitude'], json.iloc[i]['longitude']],
            radius =  (json.iloc[i]['tronc_diam']/3.1415) * 0.1 + 1,
            color = colormap(json.iloc[i]['proba_wind']),
            fill = True,
            popup=f'<div style="width : 200px">Position de l\'arbre : {json.iloc[i]['latitude'], json.iloc[i]['longitude']}<br>'
                  f'Remarquable : {json.iloc[i]['remarquable']}<br>'
                  f'Stade de développement : {json.iloc[i]['fk_stadedev']}<br>'
                  f'Etat de l\'arbre : {json.iloc[i]['fk_arb_etat']}<br>'
                  f'Quartier : {json.iloc[i]['clc_quartier']}<br>'
                  f'Secteur : {json.iloc[i]['clc_secteur']}<br>'
                  f'Probabilité que l\'arbre soit à abattre : {format(json.iloc[i]['proba_wind'],'.2f')}</div>'
            ).add_to(groupe2)
        
    folium.LayerControl().add_to(map)
    
    return map.save('map.html')    





def val_api(date):
    request = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Saint%20Quentin/{date}/{date}?unitGroup=metric&elements=datetime%2Cwindgust%2Cwindspeedmean&key=JPUDYABXYPJW583PUU43DB6U7&contentType=json'
    # request = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Saint%20Quentin/2010-02-28/2010-02-28?unitGroup=metric&elements=datetime%2Cwindgust%2Cwindspeedmean&key=JPUDYABXYPJW583PUU43DB6U7&contentType=json'
    retour = requests.get(request).json()

    return retour['days'][0]['windgust']


if __name__ == "__main__":
    # 2010-02-28    
    # date = datetime.date.today()

    # windgust = val_api(date)


    pkl_dic = 'dic_client_3.pkl'
    df_json = read_json('data.json')


    test = carte_to_htlm(df_json, pkl_dic, date)

