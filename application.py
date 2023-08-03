from flask import Flask , request , render_template
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline


application = Flask(__name__)

app = application

#route for home
@app.route('/')
def index():
    return render_template('index.html') 


@app.route('/predict',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('form.html')
    else:
        data=CustomData(
            holiday=request.form.get('holiday'),
            temp=float(request.form.get('temp')),
            clouds_all=float(request.form.get('cloud_all')),
            weather_main=request.form.get('weather_main'),
            weekday=float(request.form.get('weekday')),
            hour=request.form.get('hour'),
            month=float(request.form.get('month'))

        )
        pred_df=data.get_data_as_data_frame()
        print(pred_df)
        print("Before Prediction")

        predict_pipeline=PredictPipeline()
        print("Mid Prediction")
        results=predict_pipeline.predict(pred_df)
        results = round(results[0])
        print(results)
        print("after Prediction")
        return render_template('results.html',results=results)
    
    
if __name__=="__main__":
    app.run(host="0.0.0.0")    
    # http://127.0.0.1:5000    