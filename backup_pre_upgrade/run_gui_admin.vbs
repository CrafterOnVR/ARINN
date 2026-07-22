' Super Enhanced Research Agent - Run GUI as Administrator
' VBScript to run the research agent GUI with administrator privileges

Dim shell, fso, scriptDir, pythonCmd, guiCmd
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get script directory
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Check if running as administrator
If Not IsAdmin() Then
    ' Request administrator privileges
    MsgBox "Super Enhanced Research Agent" & vbCrLf & vbCrLf & "Requesting administrator privileges to run the GUI...", vbInformation, "Administrator Access Required"

    ' Relaunch with admin rights
    shell.Run "powershell -Command ""Start-Process 'wscript.exe' -ArgumentList '\"" & WScript.ScriptFullName & "\""' -Verb RunAs -Wait""", 0, True
    WScript.Quit
End If

' If we get here, we're running as admin
MsgBox "Super Enhanced Research Agent" & vbCrLf & vbCrLf & "Running with administrator privileges." & vbCrLf & "Starting GUI...", vbInformation, "Administrator Mode"

' Change to script directory and run the GUI
On Error Resume Next
shell.CurrentDirectory = scriptDir
shell.Run "cmd /c cd /d """ & scriptDir & """ && python run_desktop_gui.py", 1, True

If Err.Number <> 0 Then
    MsgBox "Error running GUI: " & Err.Description, vbCritical, "Error"
End If

On Error GoTo 0

MsgBox "GUI session ended.", vbInformation, "Super Enhanced Research Agent"

Function IsAdmin()
    On Error Resume Next
    Dim adminCheck
    adminCheck = shell.RegRead("HKEY_USERS\S-1-5-19\")
    IsAdmin = (Err.Number = 0)
    On Error GoTo 0
End Function