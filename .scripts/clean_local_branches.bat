@echo off
git fetch -p
echo Branches to delete:
git branch -vv | findstr ": gone]"
set /p confirm="Delete these branches? (y/n): "
if /i "%confirm%"=="y" (
    for /f "tokens=1" %%i in ('git branch -vv ^| findstr ": gone]"') do git branch -D %%i
    echo Cleanup completed!
)
pause