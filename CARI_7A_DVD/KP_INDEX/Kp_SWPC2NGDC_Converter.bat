@ECHO OFF
REM This script pulls data from NOAA *_DGD.txt files, one line at a time, skipping the first 12 lines (headers)
REM FOR /F "skip=12 tokens=1-3,23-30" %%A IN (2019Q1_DGD.txt) DO @echo %%A%%B%%C %%D %%E %%F %%G %%H %%I %%J %%K Ap--------------------------
FOR /F "skip=12 tokens=1-3,23-30 delims=+- " %%A IN (%1) DO @echo %%A%%B%%C %%D %%E %%F %%G %%H %%I %%J %%K Ap-------------------------- 
