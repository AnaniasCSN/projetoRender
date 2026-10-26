@echo off
title Sistema Web com Banco de Dados - Flask
echo ===================================================
echo Iniciando o Servidor Web e o Banco de Dados...
echo ===================================================

cd /d "%~dp0"

:: Ativa o ambiente virtual
call venv\Scripts\activate.bat

:: Inicia o servidor Python/Flask em segundo plano
start /b python app.py

echo Aguardando o Banco de Dados e o Servidor iniciarem...
timeout /t 3 /nobreak >nul

:: Abre o navegador no endereço local
start http://127.0.0.1:5000

echo ===================================================
echo Sistema ativo em http://127.0.0.1:5000
echo Mantenha esta janela aberta para salvar dados no banco.
echo ===================================================