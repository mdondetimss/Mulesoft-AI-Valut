# Run the Project

## 1️⃣ Clone the Repository

```bash
git clone <your-repository-url>
cd <repository-folder>
```

---

## 2️⃣ Install uv (If Not Installed)

### Mac / Linux

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

### Windows (Command Prompt)

```bash
pip install uv
```

### Verify Installation

```bash
uv --version
```

---

## 3️⃣ Change Directory to `Python`

```bash
cd Python
```

---

## 4️⃣ Install Dependencies

```bash
uv sync
```

---

## 5️⃣ Run the Application

```bash
uv run streamlit run frontend.py
```
