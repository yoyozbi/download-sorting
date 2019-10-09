Set Shell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject" )
startupPath = Shell.SpecialFolders("Startup")
If objFSO.FileExists( startupPath & "\\download_sorter.lnk") = False Then
    Set ink = Shell.CreateShortcut(startupPath & "\\download_sorter.lnk")
    ink.TargetPath = "C:\\users\\yohan\\code\\python\\download-sorting\\autoStart.vbs"
    ink.Save
End If
Shell.Run Chr(34) & "C:\\users\\yohan\\code\\python\\download-sorting\\start.bat" & Chr(34), 0
Set Sehll = Nothing