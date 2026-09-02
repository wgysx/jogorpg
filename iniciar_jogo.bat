@echo off
setlocal

title A Ultima Chama de Eldareth
set "PASTA_JOGO=%~dp0webpyscript"
set "PYTHON="

where py >nul 2>&1
if not errorlevel 1 set "PYTHON=py"

if not defined PYTHON (
    where python >nul 2>&1
    if not errorlevel 1 set "PYTHON=python"
)

if not defined PYTHON (
    where python3 >nul 2>&1
    if not errorlevel 1 set "PYTHON=python3"
)

if not defined PYTHON (
    echo Python nao foi encontrado neste computador.
    echo Instale o Python em https://www.python.org/downloads/
    echo Marque a opcao "Add Python to PATH" durante a instalacao.
    pause
    exit /b 1
)

if not exist "%PASTA_JOGO%\index.html" (
    echo A pasta webpyscript nao foi encontrada.
    pause
    exit /b 1
)

cd /d "%PASTA_JOGO%"
start "" http://localhost:8000
echo Servidor iniciado em http://localhost:8000
echo Feche esta janela para encerrar o servidor.
"%PYTHON%" -m http.server 8000

endlocal