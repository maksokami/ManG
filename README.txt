-------------ManG-------------

This is a small utility to ping a range or list of IP addresses and see status changes.
Run this program as administrator, as it's using native python ping and creates sockets.


python 2.7 + PyQt

------------------
IP string format:
  Any number of spaces is allowed
  IP separators - ',' or ';'
Example:
    127.0.0.1-20 , 45.2.54.1 ; 9.9.1.1-2

------------------
Default intervals:
  Ping timeout: 4sec
  Ping exec: 5sec
  Gui grid refresh: 5sec

Restart ping after you change settings.

------------------
Possible windows binary dependensies: (not included in the package)
*  To get MSVCP90.dll you may need to install Microsoft Visual C++ 2008 Redistributable Package
   OLEAUT32.dll - C:\WINDOWS\system32\OLEAUT32.dll
   USER32.dll - C:\WINDOWS\system32\USER32.dll
   IMM32.dll - C:\WINDOWS\system32\IMM32.dll
   SHELL32.dll - C:\WINDOWS\system32\SHELL32.dll
   ole32.dll - C:\WINDOWS\system32\ole32.dll
   WINMM.dll - C:\WINDOWS\system32\WINMM.dll
   COMDLG32.dll - C:\WINDOWS\system32\COMDLG32.dll
   ADVAPI32.dll - C:\WINDOWS\system32\ADVAPI32.dll
   GDI32.dll - C:\WINDOWS\system32\GDI32.dll
   WS2_32.dll - C:\WINDOWS\system32\WS2_32.dll
   WINSPOOL.DRV - C:\WINDOWS\system32\WINSPOOL.DRV
   CRYPT32.dll - C:\WINDOWS\system32\CRYPT32.dll
   KERNEL32.dll - C:\WINDOWS\system32\KERNEL32.dll
   MSVCP90.dll - D:\Documents\PyProjects\gui-test\MSVCP90.dll
