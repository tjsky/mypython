@echo off
setlocal enabledelayedexpansion

REM ����·����ʹ�þ���·�����ɿ���
set "input_dir=F:\Downloads\��ͼ"
set "output_dir=F:\Downloads\��Ƶ"

REM �������Ŀ¼
if not exist "%output_dir%" mkdir "%output_dir%"

REM ����ת��
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

echo ת����ɣ���������˳�
pause