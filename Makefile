#Shashank Venkat,Kevin Antony
#705303381,205380862
#shashank18@g.ucla.edu,kevin.m.antony@gmail.com
build: lab3b.py
	rm -f lab3b
	ln run.sh lab3b
	chmod u+x lab3b

clean:
	rm -f lab3b-705303381.tar.gz lab3b

dist:
	tar -czvf lab3b-705303381.tar.gz lab3b.py README Makefile run.sh