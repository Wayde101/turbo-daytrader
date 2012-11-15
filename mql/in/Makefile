MT4_TOP=D:/MinGW/msys/1.0/home/yuting/Alpari.dev

.PHONY: all install run

all: mon.ex4 snapshot.ex4 mwcc.ex4 MaCross.ex4 zc.ex4

%.ex4: %.mq4
	$(MT4_TOP)/metalang $<

install: all
	cp *.mq4 $(MT4_TOP)/experts/
	cp *.ex4 $(MT4_TOP)/experts/
	cp *.tpl $(MT4_TOP)/templates/
	cp *.mq4 $(MT4_TOP)/experts/indicators/
	cp *.ex4 $(MT4_TOP)/experts/indicators/

clean:
	rm -f *.o *.dll *.a *.exe *.ex4 *.log *~

run: clean all install 
	$(MT4_TOP)/terminal.exe
