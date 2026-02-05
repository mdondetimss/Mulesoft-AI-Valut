# Setup Instructions

## 1. Install `uv`

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
````

### Windows (PowerShell)

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Verify:

```bash
uv --version
```

Docs:
[https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

---

## 2. Install Ollama

Download and install Ollama:
[https://ollama.com/download](https://ollama.com/download)

Verify installation:

```bash
ollama --version
```

Start the Ollama server:

```bash
ollama serve
```

---

## 3. Pull the required model

```bash
ollama pull qwen2.5-coder:3b
```

Verify:

```bash
ollama list
```

---

## 4. Sync project dependencies

From the project root:

```bash
cd python
```

Sync dependencies from `pyproject.toml`:

```bash
uv sync
```

---

## 5. Create the database (run once)

```bash
uv run create_database.py
```

---

## 6. Run the application

```bash
uv run streamlit run frontend.py
```

Open in browser:

```
http://localhost:8501
```

---

## Sample Business Questions

After deployment, the application should be able to answer the following sample questions:
```
1. How many customers do we have?
```
```
2. Which cities do our customers come from?
```
```
3. What is the total revenue from all orders?
```
```
4. What is the average order value?
```
```
5. How many products do we sell?
```
```
6. What is the average price of our products?
```
```
7. How many products are in each category?
```

---
