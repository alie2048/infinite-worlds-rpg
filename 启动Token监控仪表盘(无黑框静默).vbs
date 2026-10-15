Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)
pywPath = WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python312\pythonw.exe"

If Not fso.FileExists(pywPath) Then
    pywPath = "pythonw.exe"
End If

' 0 表示完全隐藏窗口启动后台服务
WshShell.Run """" & pywPath & """ -m antigravity_token_monitor web --port 8765", 0, False
WScript.Sleep 500
WshShell.Run "http://127.0.0.1:8765"