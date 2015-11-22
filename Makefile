install:
	cp revirc.example ~/.revirc
clean:
	rm -f revi.log
	rm -f ~/revi.rc
	git clean -dfx
