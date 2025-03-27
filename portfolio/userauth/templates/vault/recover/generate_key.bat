@echo off
for /f "tokens=2 delims={}" %%A in ('"wmic path win32_computersystemproduct get UUID /format:list"') do set UUID=%%A
echo SecretInfinityKey-%UUID% > E:\infinitykey.txt
echo Infinity Key saved to E:\infinitykey.txt
