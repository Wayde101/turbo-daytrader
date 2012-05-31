MT4_TOP=D:/MinGW/msys/1.0/home/yuting/Alpari

.PHONY: all install run

all: snapshot.ex4 

%.ex4: %.mq4
	$(MT4_TOP)/metalang $<

install: all
	cp *.mq4 $(MT4_TOP)/experts/
	cp *.ex4 $(MT4_TOP)/experts/
	cp *.mq4 $(MT4_TOP)/experts/indicators/
	cp *.ex4 $(MT4_TOP)/experts/indicators/

clean:
	rm -f *.o *.dll *.a *.exe *.ex4 *.log *~

run: clean all install 
	$(MT4_TOP)/terminal.exe
