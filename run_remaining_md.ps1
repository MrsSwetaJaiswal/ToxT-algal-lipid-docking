# Runs the two remaining 50 ns MD jobs sequentially (one GPU job at a time).
# Launch this only AFTER the epa_50ns run has finished.
#   powershell -File run_remaining_md.ps1
$py = "C:\Users\ASUS\miniforge3\envs\md\python.exe"
Set-Location "C:\Users\ASUS\Claude\Projects\AutoDock"

Write-Host "=== [1/2] methyl-EPA ester, 50 ns ===" -ForegroundColor Cyan
& $py -u md_production.py "md\methyl_epa_pose.sdf" methyl_epa_50ns 50

Write-Host "=== [2/2] EPA carboxylate (deprotonated), 50 ns ===" -ForegroundColor Cyan
& $py -u md_production.py "md\epa_deprot_pose.sdf" epa_deprot_50ns 50

Write-Host "=== All queued MD runs complete ===" -ForegroundColor Green
