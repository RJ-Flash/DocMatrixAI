# Schedule monitoring task
$taskName = "ExpenseDocAI_Monitor"
$scriptPath = Join-Path $PSScriptRoot "monitor.py"
$pythonPath = Join-Path $PSScriptRoot "venv\Scripts\python.exe"

# Create task action
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument $scriptPath

# Create task trigger (run every 5 minutes)
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)

# Create task settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Register the task
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Monitor ExpenseDocAI system health"

Write-Host "Monitoring task scheduled successfully!" 