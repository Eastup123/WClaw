# Project instructions

## PowerShell / Windows file reading

When running PowerShell commands to read text files, always use explicit UTF-8 encoding.

Use:

```powershell
Get-Content -Path <file> -Raw -Encoding UTF8