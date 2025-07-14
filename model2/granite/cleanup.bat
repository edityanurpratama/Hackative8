@echo off
REM cleanup.bat - Bersihkan folder projek dari virtual environments dan cache

REM 1. Pastikan dijalankan di folder root proyek
cd /d "%~dp0"

echo [1/6] Menghapus virtual environment...
if exist venv ( 
    rmdir /s /q "venv"
    echo   -> venv terhapus.
) else (
    echo   -> venv tidak ditemukan, lanjut.
)

echo [2/6] Menghapus folder build dan dist (jika ada)...
if exist build rmdir /s /q "build" && echo   -> build terhapus.
if exist dist rmdir /s /q "dist" && echo   -> dist terhapus.

echo [3/6] Menghapus cache Python (__pycache__)...
for /d /r . %%D in (__pycache__) do (
    if exist "%%D" rmdir /s /q "%%D"
)
echo   -> __pycache__ dihapus (jika ada).

echo [4/6] Menghapus pip cache...
where pip >nul 2>&1
if %errorlevel% equ 0 (
    pip cache purge
    echo   -> Pip cache berhasil dibersihkan.
) else (
    echo   -> Pip tidak ditemukan, lanjut.
)

echo [5/6] Menghapus cache pengujian (.pytest_cache)...
for /d /r . %%D in (.pytest_cache) do (
    if exist "%%D" rmdir /s /q "%%D"
)
echo   -> .pytest_cache dihapus (jika ada).

echo [6/6] Selesai! Projek sudah bersih.
echo.
echo Sekarang kamu bisa membuat ulang venv dan install paket via:
echo   python -m venv venv
echo   venv\Scripts\activate
echo   pip install -r requirements.txt
echo.
echo Ingat untuk push hanya file kode dan konfigurasi:
echo   - src/ (folder kode)
echo   - requirements.txt
echo   - .gitignore (.venv, __pycache__, pip cache, dsb)
echo   - docs/ atau notebook .ipynb jika perlu.
echo.
pause