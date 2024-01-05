# code to calculate time difference in 2 columns of iinput time
# the time difference must be in 24-h format

BEGIN{	
	OFS = "\t"						# setting default field separator to tab (/t)
	print "Time1","","Time2","","DIfference"		# printing headings as required
} NR > 0 {

	# save hours, minutes, seconds of time 1 in field $1 in variables using substr function
	hour1	= substr($1, 1, 2)
	min1	= substr($1, 3, 2)
	sec1	= substr($1, 5, 2)
	
	# save hours, minutes, seconds of time 2 in field $2 in variables using substr function
	hour2	= substr($2, 1, 2)
	min2	= substr($2, 3, 2)
	sec2	= substr($2, 5, 2)
	
	# calculating both times in seconds from 00:00:00 using simple mathematical relations between time units
	time1 = hour1*3600 + min1*60 + sec1
	time2 = hour2*3600 + min2*60 + sec2
	
	# calculating unit wise time differences across different variables
	diff		= time2 - time1
	diff_hour	= int(diff / 3600)
	diff_sec	= int(diff % 60)
	diff_min	= int((diff % 3600) / 60)
	
	# printing required results in tab separated columns
	printf("%02d:%02d:%02d\t%02d:%02d:%02d\t%02d:%02d:%02d \n", hour1, min1, sec1, hour2, min2, sec2, diff_hour, diff_min, diff_sec)
}
