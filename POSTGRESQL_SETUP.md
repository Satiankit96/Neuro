# PostgreSQL Setup for Neuro Index

## Quick Setup (Windows)

### Step 1: Install PostgreSQL
1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Run installer (use default settings)
3. Set password for `postgres` user: `postgres` (or remember your own)
4. Keep default port: `5432`

### Step 2: Create Database
```powershell
# Option A: Using pgAdmin (GUI)
1. Open pgAdmin 4
2. Right-click "Databases" → Create → Database
3. Name: neuro_index
4. Click Save

# Option B: Using command line (if psql is in PATH)
psql -U postgres
CREATE DATABASE neuro_index;
\q
```

### Step 3: Initialize Database & Add Dummy Data
```powershell
Set-Location C:\Copilot_Projects\UPSC-Neuro-OS
C:\Copilot_Projects\venv\Scripts\python.exe init_db.py
```

### Step 4: Run the App
```powershell
C:\Copilot_Projects\venv\Scripts\python.exe -m streamlit run app.py --server.port 8508
```

---

## Database Connection

**Default connection (hardcoded in `utils/database.py`):**
```
postgresql://postgres:postgres@localhost:5432/neuro_index
```

**If you used a different password:**
1. Create `.env` file in project root
2. Add: `DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/neuro_index`

---

## For Render Deployment

**No setup needed!** Render auto-provides `DATABASE_URL` environment variable.

Just:
1. Create PostgreSQL database on Render (FREE tier)
2. Deploy app
3. Visit: `https://your-app.onrender.com/init-db-secret` (one time only)
4. App is ready!
