REM Download Miniconda
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o .\miniconda.exe
start /wait "" .\miniconda.exe /S
del .\miniconda.exe

call "%UserProfile%\miniconda3\Scripts\activate.bat"
REM Accept Terms of Service
call conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
call conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
call conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/msys2
call conda create -n FijiCloneEnv python=3.11 -y
call conda activate FijiCloneEnv
call conda install --yes --file "%~dp0requirements.txt"

pause