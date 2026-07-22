# Super Enhanced Research Agent - Administrator Mode

This guide explains how to run the Super Enhanced Research Agent GUI with administrator privileges on Windows.

## Why Administrator Mode?

Some research operations may require elevated privileges for:
- Accessing system files and directories
- Installing dependencies or updates
- Running intensive computational tasks
- Accessing network resources with restrictions

## Available Runner Files

### 1. `run_gui_admin.bat` (Batch File) ✅ **FIXED v2.0**
**Recommended for most users**
- Simple double-click execution
- Automatic privilege escalation
- **Enhanced working directory preservation** - Uses temporary script method
- Clear status messages
- **New approach:** Creates temporary admin script to ensure correct directory

**Usage:**
```batch
# Double-click the file or run from command prompt:
run_gui_admin.bat
```

**Fix Applied:** Now uses temporary script creation method that guarantees the correct working directory is maintained during privilege escalation. No more System32 errors!

### 2. `run_gui_admin.ps1` (PowerShell Script)
**Best for advanced users**
- More reliable privilege detection
- Better error handling
- PowerShell execution policy compatibility

**Usage:**
```powershell
# From PowerShell (may need execution policy change):
.\run_gui_admin.ps1

# Or from command prompt:
powershell -ExecutionPolicy Bypass -File run_gui_admin.ps1
```

### 3. `run_gui_admin.vbs` (VBScript)
**Fallback option**
- Works when PowerShell is restricted
- Uses Windows Script Host
- Simple execution

**Usage:**
```batch
# Double-click or run:
run_gui_admin.vbs
```

## How It Works

1. **Privilege Check**: Script detects if already running as administrator
2. **Elevation Request**: If not admin, requests elevated privileges via UAC
3. **GUI Launch**: Runs `python run_desktop_gui.py` with full admin rights
4. **Session Management**: Keeps terminal open until GUI closes

## Troubleshooting

### UAC Prompt Not Appearing
- Ensure User Account Control is enabled in Windows Security settings
- Try running the script from an elevated command prompt first

### PowerShell Execution Policy
If PowerShell scripts are blocked:
```powershell
# Set execution policy (run as admin):
Set-ExecutionPolicy RemoteSigned

# Or use bypass for this session:
powershell -ExecutionPolicy Bypass -File run_gui_admin.ps1
```

### Python Not Found
Ensure Python is in your system PATH or use full path:
```batch
# Edit the batch file to use full Python path:
"C:\Python39\python.exe" run_desktop_gui.py
```

### "Can't open file 'C:\Windows\System32\..." Error ✅ **FIXED v2.0**
**Problem:** When elevating privileges, Windows changes working directory to System32
**Solution:** Batch file now uses temporary script creation method
**Status:** Fixed in v2.0 - creates temporary admin script with correct directory commands
**Method:** `cd /d "%BATCH_DIR%"` command embedded in elevated script

## Security Notes

- Administrator mode grants full system access
- Only use when necessary for research operations
- Close the elevated session when finished
- The GUI itself doesn't require admin rights for basic research

## Alternative Methods

### Create Desktop Shortcut
1. Right-click on `run_gui_admin.bat`
2. Select "Create shortcut"
3. Right-click the shortcut → Properties
4. Click "Advanced" → Check "Run as administrator"

### Command Line
```batch
# Run with explicit admin request:
runas /user:Administrator "cmd /c python run_desktop_gui.py"
```

## Support

If you encounter issues:
1. Try a different runner file (.bat, .ps1, or .vbs)
2. Check Windows Event Viewer for error details
3. Ensure all dependencies are installed
4. Verify Python and pip are working correctly

---
**Super Enhanced Research Agent** - Maximum Intelligence Without API Keys