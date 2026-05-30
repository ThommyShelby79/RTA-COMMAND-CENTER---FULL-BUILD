# 📊 RTA Command Center

**Real-Time Adherence Monitoring Dashboard for Contact Center Operations**

Built by [Hatem Shalaby](https://linkedin.com/in/hatem-shalaby-7359611a2) | [Portfolio](https://hatemismail2011shalaby.github.io/RTA-Operations-Portfolio/)

## 🎯 What This Does

Automates Real-Time Adherence (RTA) monitoring for contact centers:
- ✅ Calculates agent adherence percentages instantly
- 📊 Visual dashboards with color-coded status indicators
- 🚨 Automated alerts for agents out of adherence
- 📈 Summary metrics and distribution analysis
- 📥 Export reports to Excel/CSV
- 💾 Historical trend analysis capability

**Impact:** Saves supervisors 2-3 hours daily on manual adherence tracking

## 🚀 Quick Start (5 minutes)

### Option 1: Run Locally

```bash
# Clone/download the project
cd rta-command-center

# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run src/app.py
```

Opens at `http://localhost:8501`

### Option 2: Deploy to Streamlit Cloud (Free)

1. Fork/upload to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub account
4. Select this repository
5. Set main file: `src/app.py`
6. Deploy!

## 📊 How to Use

### Step 1: Prepare Your Data

Create CSV file with these EXACT columns (case-sensitive):
```csv
agent_id,agent_name,scheduled_start,scheduled_end,actual_start,actual_end,break_scheduled,break_actual
A001,John Smith,09:00,17:00,09:05,17:10,60,58
```

**Column Specifications:**
- `agent_id`: Unique agent identifier (text)
- `agent_name`: Agent's full name (text)
- `scheduled_start`: Shift start time in HH:MM (24-hour format)
- `scheduled_end`: Shift end time in HH:MM
- `actual_start`: When agent actually started
- `actual_end`: When agent actually ended
- `break_scheduled`: Scheduled break duration in minutes (integer)
- `break_actual`: Actual break duration in minutes (integer)

### Step 2: Upload & Analyze

1. Click "Browse files" in sidebar
2. Select your CSV
3. Dashboard auto-calculates and displays
4. Adjust alert threshold if needed

### Step 3: Review Results

**Color Coding:**
- 🟢 **Green (≥95%)**: Adherent - Agent met target
- 🟡 **Yellow (90-95%)**: At Risk - Close to target
- 🔴 **Red (<90%)**: Out of Adherence - Below target

### Step 4: Export Reports

- Download Excel with full analysis
- Export filtered CSV
- Export alerts only

## 🧮 Calculation Logic
Adherence % = (Actual Productive Time / Scheduled Productive Time) × 100
Where:
Productive Time = Total Time - Break Time
Example:
Scheduled: 09:00-17:00 (480 min) - 60 min break = 420 min scheduled
Actual: 09:05-17:10 (485 min) - 58 min break = 427 min actual
Adherence = (427 / 420) × 100 = 101.7%
Status = ✅ Adherent (exceeds 95%)

## 🎨 Customization Guide

### Change Adherence Targets

Edit `src/calculations.py`, function `calculate_adherence()`:
```python
if adherence_pct >= 95:  # Change 95 to your target (e.g., 90)
    status = "✅ Adherent"
```

### Modify Alert Threshold

In sidebar: Drag slider from default 10 to your threshold

### Add New Metrics

Edit `src/calculations.py` - `calculate_summary_metrics()` function

### Change Colors

Edit `src/visualizations.py` - update color hex codes:
```python
colors.append('#00AA00')  # Change green code
```

## 📁 Project Structure
rta-command-center/
├── src/
│   ├── app.py              # Main Streamlit app
│   ├── calculations.py     # Adherence math
│   └── visualizations.py   # Plotly charts
├── examples/
│   └── sample_data.csv     # Demo data
├── requirements.txt        # Dependencies
└── README.md

## 🧪 Testing

```bash
# Run calculation tests
python src/calculations.py

# Run visualization tests  
python src/visualizations.py

# Both should print: ✅ ALL TESTS PASSED
```

## 🚀 Deployment Checklist

- [ ] All files copied to correct folders
- [ ] `requirements.txt` installed
- [ ] Sample data loads without errors
- [ ] Tests pass (`python src/calculations.py`)
- [ ] Streamlit app runs (`streamlit run src/app.py`)
- [ ] Upload sample CSV and verify output
- [ ] Export to Excel works
- [ ] Deploy to Streamlit Cloud (optional)

## 💡 Use Cases

**Supervisor Monitoring:** Check agent adherence in real-time without manual tracking

**Compliance Reporting:** Generate hourly/daily adherence reports for audits

**Performance Management:** Identify top performers and coaching opportunities

**Workforce Planning:** Predict staffing needs based on adherence patterns

## 🤝 Troubleshooting

**Error: "Missing required columns"**
→ Verify CSV has exact column names (case-sensitive)

**Error: "Invalid time format"**
→ Use HH:MM format only (e.g., 09:30, not 9:30 AM)

**Dashboard won't load**
→ Run tests first: `python src/calculations.py`
→ Check CSV has at least one row

**Export to Excel fails**
→ Make sure openpyxl is installed: `pip install openpyxl`

## 📊 Sample Data Included

`examples/sample_data.csv` contains 20 agents with realistic adherence patterns:
- Some agents at 100% adherence
- Some between 90-95% (at risk)
- Some below 90% (alerts generated)
- Various break durations

Use this to test before using real data.

## 📝 License

MIT License - Free to use, modify, and distribute

## 👤 Author

**Hatem Shalaby**  
RTA Operations Automation Expert

- 📧 Email: [Your Email]
- 💼 LinkedIn: [linkedin.com/in/hatem-shalaby-7359611a2](https://linkedin.com/in/hatem-shalaby-7359611a2)
- 🌐 Portfolio: [hatemismail2011shalaby.github.io](https://hatemismail2011shalaby.github.io/RTA-Operations-Portfolio/)
- 💻 GitHub: [@hatemismail2011shalaby](https://github.com/hatemismail2011shalaby)

---

## 🚀 What's Next?

Check out the WFM Forecasting Calculator for:
- Erlang C staffing calculations
- Shrinkage analysis
- FTE planning
- Cost modeling

⭐ If this helped you, please star the repository!


