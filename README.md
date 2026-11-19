# TrafficSense AI (no Maven)
A React dashboard, Flask ML API, Random Forest classifier, OpenStreetMap map, route alternatives, and floating traffic chatbot.

## Quick Start (Windows)
Double-click `run.bat` in the project root directory, or run manually:

Terminal 1 (ML Backend):
```powershell
cd "D:\trafficsensenew\ml-service"
python app.py
```

Terminal 2 (Frontend UI):
```powershell
cd "D:\trafficsensenew\frontend"
npm run dev
```

Open the dashboard in your browser: **http://localhost:5173/** (or **http://127.0.0.1:5173/**).

## Dataset
CSV columns: `vehicle_count,avg_speed,hour,day_of_week,rain_mm,congestion_level`.
Train: `python train_model.py --csv "C:\path\to\traffic.csv"`.
Default training is synthetic demo data, not real traffic measurements. For true forecasting, labels must represent traffic at the future horizon and evaluation should use a chronological split.

## Routing and limitations
The route planner geocodes origin/destination with Nominatim and requests alternatives from the public OSRM demo service. It compares estimated duration but **does not use live congestion**. For true traffic-aware routing, integrate a provider with live traffic data. Road markers, metrics and charts are illustrative. The chatbot is a local data-aware helper, not a generative AI service.


## Delhi-only demo configuration
The dashboard map center, road markers, road labels and default route origin are configured for Delhi, India. The congestion values remain illustrative sample data, not verified real-time Delhi traffic observations. Use a Delhi-specific, properly licensed traffic dataset to train and evaluate a real model.


## Delhi-focused interface update
The navigation switches between separate dashboard views: Dashboard, Live Map, Prediction, Traffic Analytics, Saved Routes, Alerts & Notifications, Chat Assistant and Settings. The UI uses Delhi-specific sample road names and plain-language explanations. Road counts, congestion labels, speeds and charts are illustrative, not verified live Delhi observations. The initial model trains on synthetic data unless you provide a verified Delhi dataset. Routing estimates use public OSRM and do not include live traffic congestion.
