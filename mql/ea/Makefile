MT4_TOP=D:/MinGW/msys/1.0/home/yuting/Alpari

#CCOPTS=-Wall -Werror -g -mthreads

.PHONY: all

all: 

%.ex4: %.mq4
	$(MT4_TOP)/metalang $<

test2.exe: test2.o cJSON.dll
	gcc $(CCOPTS) -o $@ $^

test.exe: test.o mt4web.dll
	gcc $(CCOPTS) -o $@ $^

test.c: mt4web.h 

test2.c: cJSON.h

mt4web.dll libmt4web.a: mt4web.o
	gcc $(CCOPTS) -shared $< -Wl,--add-stdcall-alias -o $@ -lws2_32 \
            -Wl,--out-implib,libmt4web.a

cJSON.dll libcJSON.a: cJSON.o
	gcc $(CCOPTS) -shared $< -Wl,--add-stdcall-alias -o $@ -lws2_32 \
            -Wl,--out-implib,libcJSON.a


%.o: %.c
	gcc $(CCOPTS) -c $<

mt4web.c: mt4web.h

cJSON.c: cJSON.h

install: all
	cp *.mq4 $(MT4_TOP)/experts/
	cp *.ex4 $(MT4_TOP)/experts/
	cp *.dll $(MT4_TOP)/experts/libraries/

clean:
	rm *.o *.dll *.a *.exe *.ex4 *.log

instex4: *.ex4
	cp *.mq4 $(MT4_TOP)/experts/
	cp *.ex4 $(MT4_TOP)/experts/



run: clean all install
	$(MT4_TOP)/terminal.exe
