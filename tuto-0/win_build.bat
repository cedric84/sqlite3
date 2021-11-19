@set CC=%MINGW_HOME%\bin\gcc.exe
@set INSTALL_PREFIX=../install/i686-mingw
@set SQLITE3_PATH=%INSTALL_PREFIX%
@%CC% -Wall -Werror -o%INSTALL_PREFIX%\bin\app	^
	-I%SQLITE3_PATH%/include	^
	-L%SQLITE3_PATH%/lib		^
	.\main.c					^
	-lsqlite3.dll
