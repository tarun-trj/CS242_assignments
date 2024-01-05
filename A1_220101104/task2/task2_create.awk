# creating file according to instructions

BEGIN{	OFS = "\t"			# one time execution only at beginning, print all required data
	print "034023","052030"
	print "051811","061150"
	print "061711","091050"
	print "071811","111150"
	print "031811","151150"
	print "091811","123412"
	print "060021","180042"
	print "123500","142832"
	exit				# exits code from command line
}
