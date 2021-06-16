CC=gcc
CFLAGS=-Wall -O
EXEC=test
SRC := $(wildcard *.c)
SRC := $(SRC) ../Unity/src/unity.c -I../Unity/src/ -I. 
SRC := $(SRC) ../src/parser.c -I../src/ -I. 
DEFINE = -DTEST
$(info $(SRC))
all: Release

Release:
	gcc $(SRC) -o $(EXEC) $(CFLAGS) $(DEFINE)
clean:
	rm -f go

