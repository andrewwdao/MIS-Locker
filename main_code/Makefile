#
# This is a project Makefile. It is assumed the directory this Makefile resides in is a
# project subdirectory.
#

CC=gcc

###############################################################################
# INCLUDES DIRECTION
###############################################################################
IDIR =     /                                                               \
###############################################################################
# INCLUDES DIRECTION
###############################################################################
_RFID_DEPS =                                                               \
            rfid_wiegand.h                                                 \
												   						   \
RFID_DEPS = $(patsubst %,$(IDIR)/%,$(_RFID_DEPS))

_PERIPHERAL_DEPS =                                                         \
            Rasp_HC595.h                                                   \
												   						   \
PERIPHERAL_DEPS = $(patsubst %,$(IDIR)/%,$(_PERIPHERAL_DEPS))

_BUZZER_DEPS =                                                             \
                                                                           \
BUZZER_DEPS = $(patsubst %,$(IDIR)/%,$(_BUZZER_DEPS))
###############################################################################
# OBJECTS CREATED
###############################################################################
_RFID_OBJ =                                                                \
			rfid_main.o                                                    \
            rfid_wiegand.o												   \
			
RFID_OBJ = $(patsubst %,$(ODIR)/%,$(_RFID_OBJ))

_PERIPHERAL_INIT_OBJ =                                                     \
            peripheral_init.o                                              \
            Rasp_HC595.o												   \
			
PERIPHERAL_INIT_OBJ = $(patsubst %,$(ODIR)/%,$(_PERIPHERAL_INIT_OBJ))

_PERIPHERAL_MAIN_OBJ =                                                     \
			peripheral_main.o                                              \
            Rasp_HC595.o												   \
			
PERIPHERAL_MAIN_OBJ = $(patsubst %,$(ODIR)/%,$(_PERIPHERAL_MAIN_OBJ))

_BUZZER_OBJ =                                                              \
			buzzer_main.o                                                  \
			
BUZZER_OBJ = $(patsubst %,$(ODIR)/%,$(_BUZZER_OBJ))
###############################################################################
# OBJECTS DIRECTORY
###############################################################################
ODIR=obj
###############################################################################
# LIBRARY DIRECTORY
###############################################################################
LDIR =/lib
###############################################################################
# OUTSIDE LIBRARY INCLUDE
###############################################################################
LIBS =                                                                     \
  #          -l wiringPi                                                   \
###############################################################################
# DEFINES
###############################################################################
CFLAGS  = -l wiringPi -lpthread -lrt  -Wall -O2 -pipe -I$(IDIR)                            \

$(ODIR)/%.o: %.c $(RFID_DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

$(ODIR)/%.o: %.c $(PERIPHERAL_DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

$(ODIR)/%.o: %.c $(BUZZER_DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)
	
rfid_main: $(RFID_OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)

peripheral_init: $(PERIPHERAL_INIT_OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)

peripheral_main: $(PERIPHERAL_MAIN_OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)

buzzer_main: $(BUZZER_OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~
	rm -rf rfid_main
	rm -rf peripheral_init
	rm -rf peripheral_main
	rm -rf buzzer_main
