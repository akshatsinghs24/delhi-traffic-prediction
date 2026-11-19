from pathlib import Path
import argparse, joblib, numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
FEATURES=["vehicle_count","avg_speed","hour","day_of_week","rain_mm"]; TARGET="congestion_level"; OUT=Path(__file__).parent/"model.joblib"
def demo(n=5000):
 r=np.random.default_rng(42); v=r.integers(0,181,n); s=r.uniform(5,80,n); h=r.integers(0,24,n); d=r.integers(0,7,n); rain=np.clip(r.gamma(1.1,1.5,n),0,25)
 rush=(((h>=7)&(h<=10))|((h>=16)&(h<=20))).astype(float); score=v/180*.56+(1-s/80)*.34+rush*.08+np.minimum(rain,20)*.004+r.normal(0,.045,n)
 return pd.DataFrame(dict(vehicle_count=v,avg_speed=s,hour=h,day_of_week=d,rain_mm=rain,congestion_level=np.where(score>=.67,"High",np.where(score>=.38,"Moderate","Low"))))
def main():
 p=argparse.ArgumentParser();p.add_argument("--csv");a=p.parse_args()
 if a.csv: df=pd.read_csv(a.csv); source=a.csv
 else: print("Using SYNTHETIC DEMO DATA, not real traffic observations.");df=demo();source="synthetic-demo"
 missing=set(FEATURES+[TARGET])-set(df.columns)
 if missing: raise SystemExit("Missing columns: "+", ".join(sorted(missing)))
 df=df[FEATURES+[TARGET]].dropna(subset=[TARGET]);X=df[FEATURES].apply(pd.to_numeric,errors="coerce");y=df[TARGET].astype(str).str.strip().str.title()
 if y.nunique()<2 or not set(y.unique()).issubset({"Low","Moderate","High"}):raise SystemExit("Labels must be Low, Moderate, High (at least two classes).")
 xt,xv,yt,yv=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
 model=Pipeline([("imputer",SimpleImputer(strategy="median")),("rf",RandomForestClassifier(n_estimators=250,max_depth=14,min_samples_leaf=2,class_weight="balanced",random_state=42,n_jobs=-1))]);model.fit(xt,yt);pred=model.predict(xv)
 print("Holdout accuracy:",round(accuracy_score(yv,pred),3));print(classification_report(yv,pred,zero_division=0))
 joblib.dump(dict(model=model,features=FEATURES,model_type="RandomForestClassifier",training_data=source),OUT);print("Saved model:",OUT)
if __name__=="__main__":main()
