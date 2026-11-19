from flask import Flask,request,jsonify
from flask_cors import CORS
from pathlib import Path
from datetime import datetime,timezone
import joblib,pandas as pd
app=Flask(__name__);CORS(app);MODEL=Path(__file__).parent/"model.joblib";FEATURES=["vehicle_count","avg_speed","hour","day_of_week","rain_mm"]
def load():return joblib.load(MODEL) if MODEL.exists() else None
@app.get("/health")
def health():
 b=load();return jsonify(status="ok",model_loaded=b is not None,model_type=b.get("model_type") if b else None,training_data=b.get("training_data") if b else None,timestamp=datetime.now(timezone.utc).isoformat())
@app.post("/predict")
def predict():
 b=load()
 if not b:return jsonify(error="Model missing. Run python train_model.py first."),503
 d=request.get_json(silent=True) or {}
 try:
  x=dict(vehicle_count=float(d.get("vehicle_count",60)),avg_speed=float(d.get("avg_speed",30)),hour=int(d.get("hour",datetime.now().hour)),day_of_week=int(d.get("day_of_week",datetime.now().weekday())),rain_mm=float(d.get("rain_mm",0))); horizon=int(d.get("horizon_minutes",30))
  if min(x["vehicle_count"],x["avg_speed"],x["rain_mm"])<0:raise ValueError("Traffic values must be non-negative.")
  if not 0<=x["hour"]<=23 or not 0<=x["day_of_week"]<=6 or not 5<=horizon<=180:raise ValueError("Invalid hour, day_of_week or horizon.")
 except (TypeError,ValueError) as e:return jsonify(error=str(e)),400
 m=b["model"];row=pd.DataFrame([x],columns=FEATURES);label=str(m.predict(row)[0]);probs=m.predict_proba(row)
 return jsonify(congestion_level=label,class_probabilities={str(c):round(float(v),4) for c,v in zip(m.classes_,probs[0])},model_confidence=round(float(max(probs[0])),4),prediction_horizon_minutes=horizon,model_type=b["model_type"],training_data=b["training_data"],is_synthetic_demo_model=b["training_data"]=="synthetic-demo")
if __name__=="__main__":
 if not MODEL.exists():
  from train_model import main;main()
 app.run(host="127.0.0.1",port=5001,debug=False)
