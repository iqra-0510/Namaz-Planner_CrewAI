# CrewAI in VS Code - Namaz & Daily Ibadah Planner Edition

Topic: **Namaz (five daily prayers) and a peaceful daily routine**. Same structure as the original CrewAI project, only the topic is different.

**IMPORTANT:** prayer times in `04_tools.py`, `07_lab_ibadah_planner.py` and the solutions are SAMPLE (fake) data for learning.
AI answers about religion can contain mistakes. For real prayer times use a trusted app or mosque timetable, and ask a scholar for religious rulings.

Python 3.10, 3.11, 3.12 or 3.13 is needed (CrewAI does not support 3.14 yet). Check with `python --version`.

## 1. Setup (once)

Open this folder in VS Code (File > Open Folder), then open the terminal (Ctrl + `).

**Windows PowerShell**
```
python -m venv .venv
.venv\Scripts\Activate.ps1
```
If PowerShell says "running scripts is disabled", run this once and try again:
```
Set-ExecutionPolicy -Scope Process Bypass
```
**Windows CMD:** `.venv\Scripts\activate.bat`
**Mac / Linux:** `source .venv/bin/activate`

Then:
```
pip install -r requirements.txt
```
(The install is big. Wait for it.)

In VS Code press Ctrl+Shift+P > "Python: Select Interpreter" > choose the one inside `.venv`.

## 2. Your Groq key

Copy `.env.example` to a new file named `.env` and paste your key:
```
GROQ_API_KEY=gsk_xxxxxxxx
```
Never share `.env` (it is already in `.gitignore`).

## 3. Run

```
python 01_first_crew.py
python 02_role_goal_backstory.py     # includes TASK 1 (cricket-lover agent)
python 03_team_sequential.py         # includes TASK 2 (Reviewer agent)
python 04_tools.py                   # includes TASK 3 (tasbeeh_total tool)
python 05_structured_output.py
python 06_hierarchical.py
python 07_lab_ibadah_planner.py      # the lab
```
### Web interface (Streamlit)
```
streamlit run app.py
```
Run it from inside this folder (where `app.py` is). It opens in the browser at http://localhost:8501

Teacher/reference solutions: `python solutions/teacher_solutions.py`

## What is in each file

| File | Concept |
|------|---------|
| 01 | One agent, one task, one crew |
| 02 | Role / goal / backstory change the style (Task 1) |
| 03 | Sequential crew with context between tasks (Task 2) |
| 04 | Tools: prayer time, calculator, own tool (Task 3) |
| 05 | JSON output checked with Pydantic |
| 06 | Hierarchical process with a manager LLM |
| 07 | Lab: Prayer Time Planner -> Routine Writer -> Routine Reviewer |
| app.py + ibadah_crew.py | Streamlit web interface for the same crew |

## Notes
- In a script, plain `crew.kickoff()` is correct. (Only Colab/Jupyter needs `await crew.kickoff_async()`.)
- Free Groq has rate limits. If you see a 429 error, wait a minute and run again.
- `GROQ_API_KEY not found` means `.env` is missing or in the wrong folder (it must be next to `config.py`).
