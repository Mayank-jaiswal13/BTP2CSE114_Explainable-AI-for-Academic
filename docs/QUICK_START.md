# Quick start

## Run the web application

From the repository root, install the web dependencies and start Flask:

```bash
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`. Demo login: `admin` / `admin123`.

## Train or refresh the model

```bash
pip install -r requirements-research.txt
python main.py
```

The script reads `data/Student_performance_data _.csv` and writes the model to `models/academic_risk_xgboost.pkl`.

For the project overview, repository layout, Vercel setup, and research files, see the [main README](../README.md).
