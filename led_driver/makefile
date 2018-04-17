# Makefile for project. Attempting to implement the following:
# gcc -Wall src/main.c ../../rpi_ws281x/ws2811.c ../../rpi_ws281x/dma.c 
# ../../rpi_ws281x/mailbox.c ../../rpi_ws281x/pwm.c 
# ../../rpi_ws281x/pcm.c ../../rpi_ws281x/rpihw.c -o main 
# -I../../rpi_ws281x


INC_DIR = inc
SRC_DIR = src
OBJ_DIR = obj
LIB_DIR = rpi_ws281x
LIBS = bcm2835

CC = gcc
CXX = g++
C_FLAGS = -c -Wall -I$(LIB_DIR) -I$(INC_DIR) -l$(LIBS)

SRCS = $(SRC_DIR)/main.c $(LIB_DIR)/ws2811.c
OBJS = $(OBJ_DIR)/main.o $(OBJ_DIR)/ws2811.o $(OBJ_DIR)/dma.o \
	$(OBJ_DIR)/mailbox.o $(OBJ_DIR)/pwm.o $(OBJ_DIR)/pcm.o \
	$(OBJ_DIR)/rpihw.o
DEPS = $(INC_DIR)/main.h $(LIB_DIR)/version.h $(LIB_DIR)/ws2811.h

main: $(OBJS)
	$(CC) $(OBJ_DIR)/main.o \
		  $(OBJ_DIR)/ws2811.o \
		  $(OBJ_DIR)/dma.o \
		  $(OBJ_DIR)/mailbox.o \
		  $(OBJ_DIR)/pwm.o \
		  $(OBJ_DIR)/pcm.o \
		  $(OBJ_DIR)/rpihw.o -l$(LIBS) -lczmq -lzmq -o $@

$(OBJ_DIR)/main.o: $(SRC_DIR)/main.c
	$(CC) -o $@ $< $(C_FLAGS) -lczmq -lzmq

$(OBJ_DIR)/ws2811.o: $(LIB_DIR)/ws2811.c
	$(CC) -o $@ $< $(C_FLAGS)

$(OBJ_DIR)/dma.o: $(LIB_DIR)/dma.c
	$(CC) -o $@ $< $(C_FLAGS)

$(OBJ_DIR)/mailbox.o: $(LIB_DIR)/mailbox.c
	$(CC) -o $@ $< $(C_FLAGS)

$(OBJ_DIR)/pwm.o: $(LIB_DIR)/pwm.c
	$(CC) -o $@ $< $(C_FLAGS)

$(OBJ_DIR)/pcm.o: $(LIB_DIR)/pcm.c
	$(CC) -o $@ $< $(C_FLAGS)
 
$(OBJ_DIR)/rpihw.o: $(LIB_DIR)/rpihw.c
	$(CC) -o $@ $< $(C_FLAGS)

PHONY: all
all: ; $(info $$SRCS is [${SRCS}]) 

clean:
	rm $(OBJ_DIR)/* main
