# EUBIA demo data

The seed script creates a fictional, bilingual German/French HR corpus:

```powershell
Set-Location D:\HrAssistant\rh-assistant\backend
.\.venv\Scripts\python.exe scripts\seed_demo_database.py
```

It writes metadata and extracted text to the configured database and indexes
the same documents in Chroma. If Azure OpenAI embedding variables are present,
the script uses the configured Azure embedding deployment; otherwise it uses
the existing local Chroma embedding function.

Run the synthetic retrieval checks with:

```powershell
.\.venv\Scripts\python.exe scripts\evaluate_demo_retrieval.py
```

The generated documents are synthetic test data. They are not EUBIA policy
and must not be presented to employees as official guidance.
