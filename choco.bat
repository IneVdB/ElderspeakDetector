REM install chocolatey and mkcert
powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin
choco feature enable -n=allowGlobalConfirmation
choco install python310 --allow-downgrade
choco install vcredist-all
choco install mkcert
choco install ffmpeg