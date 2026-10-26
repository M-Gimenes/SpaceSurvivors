@echo off
REM Gera dist\Space Survivors.exe. Rode a partir da raiz do repo.
cd /d "%~dp0"
if not exist script\routes.py (echo Falta script\routes.py - copie de script\routes.example.py & pause & exit /b 1)
set PY=py -3
where py >nul 2>nul || set PY=python
if not exist .venv\Scripts\python.exe %PY% -m venv .venv || (echo Nao achei o Python & pause & exit /b 1)
.venv\Scripts\python -m pip install -q --upgrade pip
.venv\Scripts\python -m pip install -q -r requirements.txt || (pause & exit /b 1)
.venv\Scripts\python -m pip install -q --no-deps pygame-textinput || (pause & exit /b 1)
.venv\Scripts\python -m PyInstaller --noconfirm --onefile --noconsole --name "Space Survivors" --icon assets\Images\idle1.ico --add-data "assets;assets" --paths script script\initializer.py || (pause & exit /b 1)
echo.
echo Pronto: dist\Space Survivors.exe
pause
