tskill gradint-wrapper 2>nul
taskkill /f /im gradint-wrapper.exe 2>nul >nul
start gradint-wrapper.exe once_per_day=2
