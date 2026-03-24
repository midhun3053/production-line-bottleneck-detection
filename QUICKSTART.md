# 🚀 QUICK START GUIDE - 5 Minutes to Running Project

## Step 1: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

**What this does:** Installs all required Python libraries (pandas, scikit-learn, streamlit, etc.)

---

## Step 2: Run the Analysis Notebook (2 minutes)

```bash
jupyter notebook notebooks/Production_Line_Analysis.ipynb
```

**What to expect:**
- Notebook opens in your browser
- Click "Cell" → "Run All" to execute everything
- You'll see:
  - ✅ Data loading
  - ✅ Bottleneck scores
  - ✅ Stage analysis
  - ✅ 4 beautiful charts
  - ✅ ML clustering results
  - ✅ Prediction model accuracy
  - ✅ Business recommendations

---

## Step 3: Launch the Dashboard (1 minute)

```bash
streamlit run src/app.py
```

**What to expect:**
- Dashboard opens in browser automatically
- Live filtering by production stage
- Real-time KPI metrics
- Interactive visualizations

---

## Alternative: Quick Demo Mode

If you just want to see results quickly:

```bash
# Run notebook in command line (headless)
jupyter nbconvert --to notebook --execute notebooks/Production_Line_Analysis.ipynb
```

---

## Dataset Format

If you have your own data, save it as `data/dataset.csv` with these columns:

```
Stage,Cycle_Time,Waiting_Time,Downtime,Defect_Rate,Units_Produced
Assembly,45.2,15.3,8.5,0.05,280
Welding,65.3,22.1,15.2,0.08,200
...
```

---

## Project Files Explained

| File | Purpose |
|------|---------|
| `notebooks/Production_Line_Analysis.ipynb` | Main analysis (9-step breakdown) |
| `src/app.py` | Interactive Streamlit dashboard |
| `data/dataset.csv` | Sample manufacturing data |
| `requirements.txt` | All dependencies |
| `README.md` | Full documentation |
| `HACKATHON_GUIDE.md` | Presentation tips |

---

## Troubleshooting

**Problem:** `ModuleNotFoundError: No module named 'pandas'`
```bash
# Solution:
pip install --upgrade pandas numpy scikit-learn matplotlib streamlit
```

**Problem:** Streamlit not found
```bash
# Solution:
pip install streamlit
```

**Problem:** Jupyter won't start
```bash
# Solution:
pip install jupyter jupyterlab
jupyter notebook  # Try this directly
```

**Problem:** Dataset CSV not found
- The notebook auto-generates sample data if `dataset.csv` doesn't exist
- Place your CSV in the `data/` folder if you have custom data

---

## Testing the Pipeline

To verify everything works:

```bash
# Test Python imports
python -c "import pandas, numpy, sklearn, matplotlib, streamlit; print('✅ All imports OK')"

# Test notebook without opening browser
jupyter nbconvert --execute --to notebook notebooks/Production_Line_Analysis.ipynb
```

---

## 🎯 Hackathon Workflow

```
1. Install dependencies       → 2 min
2. Run notebook analysis      → 3 min (auto-generates charts)
3. Check results             → 2 min
4. Launch dashboard          → 1 min
5. Demo to judges            → 6 min (WINNING!)
```

**Total: ~15 minutes from zero to demo-ready** ⏱️

---

## Key Outputs to Show Judges

After running the notebook, you'll have:

✅ **Console Output:**
- Bottleneck scores by stage
- Stage performance summary
- Model R² score
- Business recommendations

✅ **Visualizations:**
- Bar chart: Bottleneck by stage
- Scatter: Cycle Time vs Production
- Pie chart: Machine clusters
- Bar chart: Downtime by stage
- Feature importance chart
- Prediction accuracy chart

✅ **Dashboard Screens:**
- KPI metrics
- Interactive filtering
- Real-time analytics

---

## Commands Cheatsheet

```bash
# Setup
cd "Production Line Bottleneck"
pip install -r requirements.txt

# Jupyter
jupyter notebook notebooks/Production_Line_Analysis.ipynb

# Streamlit  
streamlit run src/app.py

# Test imports
python -c "import pandas, numpy, sklearn; print('OK')"

# Clean up (if needed)
pip uninstall pandas numpy scikit-learn matplotlib streamlit -y
pip install -r requirements.txt
```

---

## Next Steps (After Basic Run)

1. **Modify for your data:**
   - Replace `data/dataset.csv` with your production data
   - Adjust column names in notebook if different
   - Rerun notebook cells

2. **Customize recommendations:**
   - Edit the `recommend()` function in step 9
   - Adjust thresholds based on your business needs

3. **Deploy dashboard:**
   - `streamlit run src/app.py --logger.level=error`
   - Share deployment URL with team

---

## Pro Tips 💡

- **Notebook runs slow?** - Use smaller dataset or reduce KMeans clusters from 3 to 2
- **Dashboard crashing?** - Clear Streamlit cache: `rm -r ~/.streamlit`
- **Show one visualization at a time** - More impactful than showing all at once
- **Practice your narration** - Data without story is just numbers

---

**Ready? Let's go!** 🚀

Questions? Check README.md for full documentation.
