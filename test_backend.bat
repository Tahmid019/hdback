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
curl -s -o NUL -w "    Status: %%{http_code}" %BASE%/iot/health/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

:: -----------------------------------------------
:: snapshot
:: -----------------------------------------------
echo [2] Full Snapshot
curl -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/snapshot/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

:: -----------------------------------------------
:: sections
:: -----------------------------------------------
echo [3] Section - meta
curl -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/meta/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [4] Section - pump
curl -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/pump/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [5] Section - vitals
curl -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/vitals/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [6] Section - ecg
curl -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/ecg/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [7] Section - respiration
curl -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/respiration/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [8] Section - dialysate
curl -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/dialysate/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [9] Section - session
curl -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/session/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [10] Section - fluid_balance
curl -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/fluid_balance/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [11] Section - events
curl -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/events/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [12] Section - unknown (expect 404)
curl -s -o NUL -w "    Status: %%{http_code}" %BASE%/api/section/invalid/
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

:: -----------------------------------------------
:: wave
:: -----------------------------------------------
echo [13] Wave Chunk (default n=25)
curl -s -o NUL -w "    Status: %%{http_code}" "%BASE%/api/wave/"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [14] Wave Chunk (n=50)
curl -s -o NUL -w "    Status: %%{http_code}" "%BASE%/api/wave/?n=50"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

:: -----------------------------------------------
:: iot single ingest
:: -----------------------------------------------
echo [15] IoT Ingest - vitals
curl -s -o NUL -w "    Status: %%{http_code}" -X POST %BASE%/iot/ingest/ ^
  -H "Content-Type: application/json" ^
  -d "{\"section\":\"vitals\",\"payload\":{\"heart_rate\":82,\"spo2\":98,\"temperature\":36.9}}"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [16] IoT Ingest - pump
curl -s -o NUL -w "    Status: %%{http_code}" -X POST %BASE%/iot/ingest/ ^
  -H "Content-Type: application/json" ^
  -d "{\"section\":\"pump\",\"payload\":{\"blood_flow_rate\":310,\"pump_state\":\"START\"}}"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [17] IoT Ingest - session
curl -s -o NUL -w "    Status: %%{http_code}" -X POST %BASE%/iot/ingest/ ^
  -H "Content-Type: application/json" ^
  -d "{\"section\":\"session\",\"payload\":{\"elapsed_time\":\"02:30\",\"completion_percent\":62}}"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [18] IoT Ingest - event push
curl -s -o NUL -w "    Status: %%{http_code}" -X POST %BASE%/iot/ingest/ ^
  -H "Content-Type: application/json" ^
  -d "{\"section\":\"events\",\"payload\":{\"time\":\"11:30\",\"type\":\"info\",\"message\":\"Test event from bat file\"}}"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [19] IoT Ingest - partial payload (null safety check)
curl -s -o NUL -w "    Status: %%{http_code}" -X POST %BASE%/iot/ingest/ ^
  -H "Content-Type: application/json" ^
  -d "{\"section\":\"dialysate\",\"payload\":{\"ph\":7.40}}"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

echo [20] IoT Ingest - unknown section (expect 400)
curl -s -o NUL -w "    Status: %%{http_code}" -X POST %BASE%/iot/ingest/ ^
  -H "Content-Type: application/json" ^
  -d "{\"section\":\"bogus\",\"payload\":{}}"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

:: -----------------------------------------------
:: bulk ingest
:: -----------------------------------------------
echo [21] IoT Bulk Ingest
curl -s -o NUL -w "    Status: %%{http_code}" -X POST %BASE%/iot/ingest/bulk/ ^
  -H "Content-Type: application/json" ^
  -d "{\"pump\":{\"blood_flow_rate\":320},\"vitals\":{\"heart_rate\":75,\"spo2\":97},\"fluid_balance\":{\"uf_removed\":2400,\"uf_goal\":2500}}"
if %errorlevel%==0 (echo  ^| PASS & set /a PASS+=1) else (echo  ^| FAIL & set /a FAIL+=1)
echo.

:: -----------------------------------------------
:: verify state updated
:: -----------------------------------------------
echo [22] Verify State Updated After Ingest
echo.
echo     Snapshot (trimmed):
curl -s %BASE%/api/snapshot/ | findstr /i "heart_rate\|blood_flow\|uf_removed\|elapsed"
echo.

:: -----------------------------------------------
:: results
:: -----------------------------------------------
echo ================================================
echo   RESULTS:  PASS: %PASS%   FAIL: %FAIL%
echo ================================================
echo.
pause
