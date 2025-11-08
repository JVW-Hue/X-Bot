Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd /d ""c:\X Bot"" && python main.py", 0, False
