# AI Data Analyst

**Natural Language → SQL for Secure, Local Data Analysis**

AI Data Analyst is a locally deployed, LLM-powered system that enables users to query SQL databases using natural language. It removes the need for SQL expertise while enforcing **deterministic behavior**, **read-only execution**, and **strict data privacy**.

The system is designed for **enterprise and regulated environments** where correctness, reproducibility, and data sovereignty matter more than convenience or hype .

---

## Core Principle

> **Natural language is an interface, not a trust boundary.**

LLMs are treated as SQL *generators*, not autonomous actors. Every query is schema-aware, tightly constrained, post-processed, and validated before execution. If you skip any of those steps, the system becomes unsafe.

---

## Problem Statement

Traditional data analysis fails for structural reasons:

* Business users lack SQL expertise
* Data teams become bottlenecks
* Hand-written queries are error-prone
* There is no reliable bridge between human language and structured data

This project exists to close that gap without lowering technical or security standards .

---

## High-Level Workflow

The system follows a strict four-step pipeline :

1. **Schema Extraction**
   Automatically inspects the SQLite database to capture tables, columns, and relationships.

2. **Prompt Construction**
   Combines schema context and user input into a constrained, role-defined prompt.

3. **LLM Processing**
   A locally hosted LLM generates SQL using deterministic settings.

4. **Execution & Display**
   Only validated `SELECT` queries are executed and rendered in the UI.

---

## Architecture Diagram

### Architectural Principle

> **Control context flow, constrain the model, and never trust generated code blindly.**

This architecture enforces hard boundaries between user input, LLM generation, and database execution.

```
┌────────────────┐
│   User (UI)    │
│  Streamlit     │
└───────┬────────┘
        │ Natural Language Question
        ▼
┌──────────────────────────┐
│   Application Layer      │
│  (Python / LangChain)    │
│                          │
│  • Schema Extraction     │
│  • Prompt Construction   │
│  • Output Validation     │
└───────┬──────────────────┘
        │ Constrained Prompt
        ▼
┌──────────────────────────┐
│   Local LLM Runtime      │
│  (Ollama + DeepSeek-R1)  │
│                          │
│  • Temperature = 0.0     │
│  • SQL-only output       │
└───────┬──────────────────┘
        │ Generated SQL
        ▼
┌──────────────────────────┐
│   Query Guardrail Layer  │
│                          │
│ • Regex Sanitization     │
│ • SELECT-only Enforcement│
└───────┬──────────────────┘
        │ Validated SQL
        ▼
┌──────────────────────────┐
│   Database Layer         │
│  (SQLite / SQLAlchemy)   │
└───────┬──────────────────┘
        │ Query Results
        ▼
┌────────────────┐
│   Streamlit    │
│   Result View  │
└────────────────┘
```

---

## Component Responsibilities

### Streamlit Frontend

* Accepts natural language questions
* Displays execution status and results
* Has **no direct access** to the database or LLM runtime

---

### Application Layer (Python)

This is the **control plane**.

Responsibilities:

* Database schema inspection and caching
* Prompt engineering with explicit constraints
* Post-processing and validation of LLM output

This layer exists because LLMs cannot be trusted with execution authority.

---

### Local LLM Runtime (Ollama + DeepSeek-R1)

* Fully on-premise execution
* Schema-aware prompts
* Zero temperature for deterministic output
* No explanations, no commentary—SQL only 

---

### Query Guardrail Layer

Enforces:

* Removal of non-SQL artifacts
* Blocking of all mutating or destructive SQL:

  * `INSERT`, `UPDATE`, `DELETE`, `DROP`, `DDL`

This is the final enforcement point before execution.

---

### Database Layer (SQLite)

* Local, file-based database
* Accessed via SQLAlchemy
* Read-only execution enforced at code level 

SQLite is a deliberate choice to reduce operational and security complexity.

---

## Key Features

* Natural language to SQL conversion
* Automatic schema mapping and join inference
* Deterministic query generation (temperature = 0.0)
* Local-only execution (no data exfiltration)
* Strict read-only enforcement
* Clean, intuitive Streamlit UI 

---

## Example Query

**User Input**

```
Top 5 products by sales volume
```

**System Behavior**

* Detects relevant tables
* Infers joins and aggregations
* Generates executable SQL
* Returns structured results for visualization 

No schema memorization. No SQL typing. No unsafe execution.

---

## Performance & Scalability

* Schema caching minimizes repeated overhead
* Modular architecture supports future database engines
* Flexible model selection based on hardware capacity 

---

## Roadmap

Planned enhancements include :

1. Automatic data visualization (Plotly, Altair)
2. Multi-turn conversational querying
3. Natural language error explanations
4. Hybrid local + cloud deployment options

---
