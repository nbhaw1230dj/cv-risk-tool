# Quick Start Guide - CV Risk Assessment Tool

## For Non-Technical Users (Physicians/Clinic Staff)

### Installation (One-Time Setup)

1. **Install Python** (if not already installed):
   - Download from: https://www.python.org/downloads/
   - Choose Python 3.8 or newer
   - During installation, CHECK the box "Add Python to PATH"

2. **Install the application**:
   - Save all files to a folder (e.g., `C:\CVRiskTool\`)
   - Open Command Prompt (Windows) or Terminal (Mac)
   - Navigate to the folder:
     ```
     cd C:\CVRiskTool
     ```
   - Install required software:
     ```
     pip install -r requirements.txt
     ```

### Running the Application

1. **Start the app**:
   - Open Command Prompt or Terminal
   - Navigate to your folder:
     ```
     cd C:\CVRiskTool
     ```
   - Run:
     ```
     streamlit run cv_risk_app.py
     ```

2. **Use the app**:
   - A web browser will open automatically
   - If not, open your browser and go to: `http://localhost:8501`
   - Fill in patient data
   - Click "Calculate Risk Assessment"
   - View results and download report

### Quick Tips

✓ **All fields with asterisk (*) are required**
✓ **Results update immediately** after clicking Calculate
✓ **Download button** saves a text report you can copy to EMR
✓ **"New Assessment" button** clears the form for the next patient
✓ **Browser stays open** - just click "New Assessment" for each patient

### Troubleshooting

**Problem:** "streamlit: command not found"
- **Solution:** Reinstall using: `pip install --upgrade streamlit`

**Problem:** Browser doesn't open
- **Solution:** Manually go to `http://localhost:8501`

**Problem:** Port already in use
- **Solution:** Run with different port: `streamlit run cv_risk_app.py --server.port 8502`

### Stopping the Application

- Press `Ctrl+C` in the Command Prompt/Terminal window
- Or simply close the terminal window

### Files Required

Make sure these files are in the same folder:
- `cv_risk_app.py` (the web interface)
- `cv_risk_calculators.py` (the calculation engine)
- `requirements.txt` (software dependencies)

### Clinical Use Workflow

1. Patient arrives for cardiovascular risk assessment
2. Launch app (or leave running between patients)
3. Enter patient demographics and vitals
4. Enter lab values from recent bloodwork
5. Check relevant medical/family history boxes
6. Click "Calculate Risk Assessment"
7. Review results with patient
8. Download report and document in EMR
9. Click "New Assessment" for next patient

### Data Privacy Note

- **All data stays on your computer** - nothing is sent to internet
- **No data is saved** between assessments
- **For production use**, consider implementing proper patient data storage

### Support

For clinical interpretation questions, refer to:
- 2019 ACC/AHA Cholesterol Management Guidelines
- 2013 ACC/AHA ASCVD Risk Assessment Guidelines
- README.md file for detailed calculator information

---

**Need help?** Contact your IT department or email the development team.
