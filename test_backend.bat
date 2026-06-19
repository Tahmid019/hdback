@echo off
setlocal enabledelayedexpansion

set BASE=http://localhost:8000
set PASS=0
set FAIL=0

echo.
echo ================================================
echo   HD MONITOR BACKEND - ENDPOINT TEST SUITE
echo ================================================
echo.

:: -----------------------------------------------
:: health
:: -----------------------------------------------
echo [1] IoT Health Check
curl.exe -s -o NUL -w "    Status: %%{http_code}" %BASE%/iot/health/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

:: -----------------------------------------------
:: dashboard (role-shaped)
:: -----------------------------------------------
echo [2] Dashboard - technician (default)
curl.exe -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/dashboard/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [3] Dashboard - doctor (X-Role: doctor)
curl.exe -s -o NUL -w "    Status: %%{http_code}" -H "X-Role: doctor" %BASE%/api/dashboard/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

:: -----------------------------------------------
:: sections
:: -----------------------------------------------
echo [4] Section - meta
curl.exe -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/meta/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [5] Section - pump
curl.exe -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/pump/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [6] Section - pump as doctor (expect 403)
curl.exe -s -o NUL -w "    Status: %%{http_code}" -H "X-Role: doctor" %BASE%/api/section/pump/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [7] Section - vitals
curl.exe -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/vitals/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [8] Section - ecg
curl.exe -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/ecg/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [9] Section - respiration
curl.exe -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/respiration/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [10] Section - dialysate
curl.exe -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/dialysate/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [11] Section - session
curl.exe -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/session/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [12] Section - fluid_balance
curl.exe -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/fluid_balance/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [13] Section - events
curl.exe -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/events/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [14] Section - unknown (expect 404)
curl.exe -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/invalid/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

:: -----------------------------------------------
:: wave (technician only)
:: -----------------------------------------------
echo [15] Wave Chunk - technician (default n=25)
curl.exe -s -o NUL -w "    Status: %%{http_code}" "%BASE%/api/wave/"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [16] Wave Chunk - technician (n=50)
curl.exe -s -o NUL -w "    Status: %%{http_code}" "%BASE%/api/wave/?n=50"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [17] Wave Chunk - doctor (expect 403)
curl.exe -s -o NUL -w "    Status: %%{http_code}" -H "X-Role: doctor" "%BASE%/api/wave/"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

:: -----------------------------------------------
:: iot single ingest
:: -----------------------------------------------
echo [18] IoT Ingest - vitals
curl.exe -s -o NUL -w "    Status: %%{http_code}" -X POST %BASE%/iot/ingest/ ^
  -H "Content-Type: application/json" ^
  -d "{\"section\":\"vitals\",\"payload\":{\"heart_rate\":82,\"spo2\":98,\"temperature\":36.9}}"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [19] IoT Ingest - pump
curl.exe -s -o NUL -w "    Status: %%{http_code}" -X POST %BASE%/iot/ingest/ ^
  -H "Content-Type: application/json" ^
  -d "{\"section\":\"pump\",\"payload\":{\"blood_flow_rate\":310,\"pump_state\":\"START\"}}"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [20] IoT Ingest - session
curl.exe -s -o NUL -w "    Status: %%{http_code}" -X POST %BASE%/iot/ingest/ ^
  -H "Content-Type: application/json" ^
  -d "{\"section\":\"session\",\"payload\":{\"elapsed_time\":\"02:30\",\"completion_percent\":62}}"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [21] IoT Ingest - event push
curl.exe -s -o NUL -w "    Status: %%{http_code}" -X POST %BASE%/iot/ingest/ ^
  -H "Content-Type: application/json" ^
  -d "{\"section\":\"events\",\"payload\":{\"time\":\"11:30\",\"type\":\"info\",\"message\":\"Test event from bat file\"}}"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [22] IoT Ingest - partial payload (null safety check)
curl.exe -s -o NUL -w "    Status: %%{http_code}" -X POST %BASE%/iot/ingest/ ^
  -H "Content-Type: application/json" ^
  -d "{\"section\":\"dialysate\",\"payload\":{\"ph\":7.40}}"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [23] IoT Ingest - unknown section (expect 400)
curl.exe -s -o NUL -w "    Status: %%{http_code}" -X POST %BASE%/iot/ingest/ ^
  -H "Content-Type: application/json" ^
  -d "{\"section\":\"bogus\",\"payload\":{}}"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

:: -----------------------------------------------
:: bulk ingest
:: -----------------------------------------------
echo [24] IoT Bulk Ingest
curl.exe -s -o NUL -w "    Status: %%{http_code}" -X POST %BASE%/iot/ingest/bulk/ ^
  -H "Content-Type: application/json" ^
  -d "{\"pump\":{\"blood_flow_rate\":320},\"vitals\":{\"heart_rate\":75,\"spo2\":97},\"fluid_balance\":{\"uf_removed\":2400,\"uf_goal\":2500}}"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

:: -----------------------------------------------
:: verify state updated
:: -----------------------------------------------
echo [25] Verify State Updated After Ingest
echo.
echo     Dashboard (trimmed):
curl.exe -s %BASE%/api/dashboard/ | findstr /i "heart_rate blood_flow uf_removed elapsed role"
echo.

:: -----------------------------------------------
:: results
:: -----------------------------------------------
echo ================================================
echo   RESULTS:  PASS: %PASS%   FAIL: %FAIL%
echo ================================================
echo.
pause
