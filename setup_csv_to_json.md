# 📘 Setup Guide: CSV → JSON Converter on Ubuntu (Option 1: System-wide Installation)

This guide explains how to install all dependencies and run the script `csv_to_json.py` 
to convert AI Talent Hub CSV files into MongoDB-ready JSON.

---

## 1. Install Python 3

Ubuntu usually comes with Python 3 pre-installed. Verify:

```bash
python3 --version
```

If not installed, run:

```bash
sudo apt update
sudo apt install -y python3 python3-full
```

---

## 2. Install Pip (Python package manager)

```bash
sudo apt install -y python3-pip
```

Verify installation:

```bash
pip3 --version
```

---

## 3. Install Pandas (via apt, recommended)

```bash
sudo apt install -y python3-pandas
```

This installs the **pandas** library system-wide from the Ubuntu repositories.

---

## 4. Download/Prepare the Script

Save the script `csv_to_json.py` somewhere on your system, e.g.:

```bash
/home/<your-username>/csv_to_json.py
```

Make it executable (optional):

```bash
chmod +x csv_to_json.py
```

---

## 5. Run the Script

### Default usage:
```bash
python3 csv_to_json.py "AI Profiles for Talent Hub(AI_Talent_Database).csv"
```

This generates:
```
AI Profiles for Talent Hub(AI_Talent_Database).json
```

### Specify custom output file:
```bash
python3 csv_to_json.py input.csv output.json
```


---


✅ With this setup, you can run the script on any CSV with fields like 
`aiSpecialization[0]`, `aiSpecialization[1]`, `aiTools[0]`, etc., 
and get a proper JSON file ready for MongoDB import.
