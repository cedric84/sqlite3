@set CC=%MINGW_HOME%\bin\gcc.exe
@set SQLITE3_PATH=../install/i686-mingw
@%CC% -Wall -Werror -o.\app		^
	-I%SQLITE3_PATH%/include	^
	-L%SQLITE3_PATH%/lib		^
	.\main.c					^
	-lsqlite3.dll
