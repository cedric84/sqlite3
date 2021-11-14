#! /bin/bash

CC=cc
SQLITE3_PATH=../install/x86_64-linux
${CC} -Wall -Werror -o./app			\
	-I${SQLITE3_PATH}/include		\
	-L${SQLITE3_PATH}/lib			\
	-Wl,-rpath=${SQLITE3_PATH}/lib	\
	./main.c						\
	-lsqlite3
