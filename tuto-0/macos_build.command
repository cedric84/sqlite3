#! /bin/bash

CC=cc
INSTALL_PREFIX=../install/x86_64-macos
SQLITE3_PATH=${INSTALL_PREFIX}
${CC} -Wall -Werror -o${INSTALL_PREFIX}/bin/app	\
	-I${SQLITE3_PATH}/include		\
	-L${SQLITE3_PATH}/lib			\
	-Wl,-rpath,${SQLITE3_PATH}/lib	\
	./main.c						\
	-lsqlite3
