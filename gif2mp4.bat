@echo off
setlocal enabledelayedexpansion

REM 配置路径（使用绝对路径更可靠）
set "input_dir=F:\Downloads\动图"
set "output_dir=F:\Downloads\视频"

REM 创建输出目录
if not exist "%output_dir%" mkdir "%output_dir%"

REM 批量转换
for %%F in ("%input_dir%\*.gif") do (
    ffmpeg -i "%%F" ^
        -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" ^
        -c:v libx264 ^
        -preset slow ^
        -crf 23 ^
        -pix_fmt yuv420p ^
        -an ^
        -movflags +faststart ^
        "%output_dir%\%%~nF.mp4"
)

echo 转换完成！按任意键退出
pause