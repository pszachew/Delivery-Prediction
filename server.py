#!/usr/bin/env python3

from flask import Flask, request, json
from sklearn.linear_model import LogisticRegression
import joblib
import pandas as pd

MLP_classifier = joblib.load("MLP_model2.sav")
app = Flask(__name__)


def process_data(data: dict) -> dict:
    name = request.json["city"]
    response_data = {"name": name, "url": "www"}
    ls=['monday', 'tuesday','wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    flag_morning = 0
    data['city'] = [data['city']]
        
    data_df = pd.DataFrame(data)
    data_df['purchase_timestamp'] = data_df['purchase_timestamp'].apply(lambda x: pd.to_datetime(x))
    data_df['delivery_weekday'] = data_df['purchase_timestamp'].apply(lambda x: ls[x.weekday()])
    data_df['purchase_morning'] = data_df['purchase_timestamp'].apply(lambda x: 1 if x.hour<=14 else 0)
    if data_df['purchase_morning'][0] == 1:
        flag_morning = 1
    data_df.drop(["purchase_timestamp","purchase_morning"], axis=1, inplace=True)

    final_df = {} 
    column_names = ['purchase_morning', 'Kraków','Poznań','Radom', 'Szczecin', 'Warszawa', 'Wrocław',	360, 516, 620, 'monday', 'saturday', 'sunday', 'thursday', 'tuesday', 'wednesday']
    for feature in column_names:
        final_df.setdefault(feature,[0])
    features = pd.DataFrame(final_df)

    for inp_el in data_df.columns:
        if data_df[inp_el][0] in features.columns:
            features[data_df[inp_el][0]][0]=1
    if flag_morning==1:
        features["purchase_morning"][0]=1
    
    features = features.rename(columns={360:'delivery_360', 254:'delivery_254', 516:'delivery_516', 620:'delivery_620'})
    pred = MLP_classifier.predict(features)
    print(f"predicted delivery days: {pred}")
    out_dict = {"days":int(pred[0])}
    return out_dict


@app.route('/', methods=["GET"])
def process_request():
    if request.method == "GET":
        if request.get_json(force=True):
            print("Got request: ", request.json)
            response = process_data(request.json)
            return json.jsonify(response)
        else:
            return "Missing json"


if __name__ == '__main__':
    app.run()
