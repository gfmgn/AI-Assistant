@echo off
echo [1/3] Verificando ambiente virtual (venv)...
if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)

echo [2/3] Instalando/Atualizando dependencias...
call .\venv\Scripts\activate.bat
pip install -r requirements.txt --quiet

echo [3/3] Iniciando a Sora (AI Study Assistant)...
echo --------------------------------------------
python main.py
pause