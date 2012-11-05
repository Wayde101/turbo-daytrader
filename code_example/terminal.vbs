DIM objShell
set objShell=wscript.createObject("wscript.shell")
iReturn=objShell.Run("cmd.exe /C D:\cygwin\home\yuting\autostart\9998_M_5222.bat", 0, TRUE)
