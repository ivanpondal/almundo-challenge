.PHONY: clean 

build: LKH-2.0.7/LKH

clean:
	rm -rf LKH-2.0.7 src/*.pyc

LKH-2.0.7/Makefile:
	curl -L http://webhotel4.ruc.dk/~keld/research/LKH/LKH-2.0.7.tgz | tar zxf -

LKH-2.0.7/LKH: LKH-2.0.7/Makefile
	$(MAKE) -C LKH-2.0.7
