# Smelly Code Assignment – Report

This project demonstrates six classic **code smells** in Python.  
The folder layout is:

```
SMELLY CODE/
├─ .venv/
├─ docs/
│   └─ smell.md
├─ tests/
│   └─ tests_app.py
└─ app.py
```

---

## How to Run

### 1. Activate Virtual Environment
- **PowerShell (Windows):**
```powershell
.venv\Scripts\Activate.ps1
```

- **Command Prompt (Windows):**
```cmd
.venv\Scripts\activate.bat
```

- **Git Bash / WSL (Linux/Mac style):**
```bash
source .venv/bin/activate
```

---

### 2. Run the Application
Run the deliberately smelly code:
```powershell
python app.py
```

---

### 3. Run Unit Tests
Run all unit tests inside the `tests` folder:
```powershell
python -m unittest discover -s tests -p "tests_*.py"
```

---

## Implemented Smells

1. **God Class (Blob)**  
   - **File:** `app.py`  
   - **Lines:** 18–116  
   - **Justification:** `MegaApp` manages users, products, orders, pricing, audit logs, and receipts — too many responsibilities for one class.

2. **Duplicated Code**  
   - **File:** `app.py`  
   - **Lines:** 52–73 (`calculate_discount_a`) and 75–84 (`calculate_discount_b`)  
   - **Justification:** Two functions contain nearly identical discount logic with only slight variation.

3. **Magic Numbers**  
   - **File:** `app.py`  
   - **Lines:** 55–60 (discount thresholds and rates), 100 (tax rate = `0.07`), 108–112 (shipping = `42.0`, `3.14`).  
   - **Justification:** Hard-coded values make the code unclear and difficult to maintain.

4. **Long Method**  
   - **File:** `app.py`  
   - **Lines:** 86–140 (`process_order`)  
   - **Justification:** Performs many unrelated tasks in one method: item building, pricing, discounts, taxes, shipping, loyalty, and audit logging.

5. **Large Parameter List**  
   - **File:** `app.py`  
   - **Lines:** 28–31 (`register_user`)  
   - **Justification:** Accepts 10+ arguments; better design would pass a user object or dataclass.

6. **Feature Envy**  
   - **File:** `app.py`  
   - **Lines:** 146–157 (`ReportGenerator.summarize_order`)  
   - **Justification:** This method digs into `Order` and `MegaApp` internals instead of encapsulating behavior where it belongs.

---

## Notes
- The smells are **intentional** for learning purposes.  
- All smells are marked inline with comments like `# [SMELL: Long Method]`.  
- The program runs successfully and the unit tests pass.  
