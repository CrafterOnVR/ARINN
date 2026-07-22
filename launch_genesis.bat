@echo off
echo ====================================================
echo      ARINN: 336-HOUR GENESIS RUN LAUNCHER
echo ====================================================

:: Set the OpenRouter Base URL to bypass OpenAI servers
set LLM_BASE_URL=https://openrouter.ai/api/v1

:: Inject the provided free OpenRouter API Key
set LLM_API_KEY=your_openrouter_api_key_here

:: Define the specific Qwen model to pull from OpenRouter (Using the actual physical OpenRouter tags)
set OPENAI_MODEL=qwen/qwen-2-7b-instruct:free

:: (Optional) Set your remote website database here if you build it
:: set ARINN_REMOTE_URL=http://your-website-url

echo [BOOT] OpenRouter Connection Configured (Qwen 3.6 API)
echo [BOOT] Initializing Continuous Learning Matrices...
echo.

:: Launch the main 336-Hour Temporal execution loop
python run_genesis.py
pause
