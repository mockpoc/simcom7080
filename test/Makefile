CC=gcc
CFLAGS=-Wall -O
EXEC=test
SRC := $(wildcard *.c)
SRC := $(SRC) ../Unity/src/unity.c -I../Unity/src/ -I. 
SRC := $(SRC) ../src/parser.c -I../src/ -I. 
SRC := $(SRC) ../GSM_Engine/library/at_engine.c -I../GSM_Engine/library/ -I. 
DEFINE = -DTEST
$(info $(SRC))
all: Release

Release:
	gcc $(SRC) -o $(EXEC) $(CFLAGS) $(DEFINE)
clean:
	rm -f go

