@echo off
@chcp 65001 > nul
setlocal enableextensions enabledelayedexpansion

:: 进入脚本所在目录
cd /d "%~dp0"

:: ==========================================
:: [配置区] 
:: ==========================================
:: llama.cpp 核心程序 (server.exe) 所在的文件夹
set "LLAMA_DIR=.\llama"

:: 模型文件 (.gguf) 所在的文件夹
set "MODEL_DIR=."
:: ==========================================

echo [1/3] 正在检查环境...

:: server.exe存在检测
if not exist "%LLAMA_DIR%\server.exe" (
    echo [错误] 找不到执行文件: "%LLAMA_DIR%\server.exe"
    echo 请检查脚本顶部的 LLAMA_DIR 配置。
    goto quit
)

:: 模型文件夹存在检测
if not exist "%MODEL_DIR%" (
    echo [错误] 找不到模型文件夹: "%MODEL_DIR%"
    goto quit
)

echo [2/3] 环境检查通过。
echo.

:choose_mode
echo ===================================
echo 请选择启动模式:
echo 1. CPU 模式 (不使用显卡)
echo 2. GPU 模式 (全显卡加速)
echo 3. MoE 模式 (CPU+GPU混合模式，需设定加载到显存的模型层数)
echo ===================================
set "mode_choice="
set /p "mode_choice= 请输入数字选择 (默认2): "
if "%mode_choice%"=="" set "mode_choice=2"

if "%mode_choice%"=="1" (
    set "RUN_MODE=CPU"
    set "NGL_VAL=0"
) else if "%mode_choice%"=="2" (
    set "RUN_MODE=GPU"
    set "NGL_VAL=999"
) else if "%mode_choice%"=="3" (
    set "RUN_MODE=MoE"
    set "NGL_VAL=999"
    set /p "custom_ngl= 请输入加载到GPU的层数 -ngl (默认 999): "
    if not "!custom_ngl!"=="" set "NGL_VAL=!custom_ngl!"
) else (
    echo 选择无效，请重新输入!
    goto choose_mode
)

echo.
echo [3/3] 正在扫描模型文件...

:: 扫描模型文件
set n=0
for /f "delims=" %%i in ('dir /b "%MODEL_DIR%\*.gguf" 2^>nul') do (
    set "models[!n!].file=%%i"
    set "models[!n!].name=%%~ni"
    set /a n+=1
)

if %n% equ 0 (
    echo [错误] 在 "%MODEL_DIR%" 中没找到 .gguf 文件。
    goto quit
)

if %n% equ 1 (
    set "MODEL_FILE=!models[0].file!"
    set "MODEL_NAME=!models[0].name!"
    goto launch
)

:many_model
set /a end=%n%-1
echo ===================================
echo 发现多个模型，请选择:
for /l %%i in (0,1,%end%) do (
    echo %%i. !models[%%i].name!
)
echo ===================================

:choice_model
set "choice="
set /p "choice= 请输入数字选择 (默认0): "
if "%choice%"=="" set "choice=0"

:: 验证合法性
set "found=0"
for /l %%i in (0,1,%end%) do (
    if "!choice!"=="%%i" (
        set "MODEL_FILE=!models[%%i].file!"
        set "MODEL_NAME=!models[%%i].name!"
        set "found=1"
    )
)

if "!found!"=="0" (
    echo 选择无效,请重新输入
    goto choice_model
)

:launch
@title 启动llama_cpp服务器 - !RUN_MODE! - !MODEL_NAME!
echo.
echo ===================================
echo 启动配置:
echo 运行模式 : !RUN_MODE! 
echo GPU载入层数: !NGL_VAL! (-ngl)
echo 模型名称 : !MODEL_NAME!
echo 模型路径 : %MODEL_DIR%\!MODEL_FILE!
echo ===================================
echo 准备启动llama_cpp服务器...

:: 执行最终启动命令
"%LLAMA_DIR%\server.exe" -m "%MODEL_DIR%\!MODEL_FILE!" -c 2048 -ngl !NGL_VAL! -a "!MODEL_NAME!" --host 127.0.0.1

echo.
echo [提示] 程序已运行结束或崩溃。
goto quit

:quit
echo.
echo 按任意键关闭窗口...
pause > nul
