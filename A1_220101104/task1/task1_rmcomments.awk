# code to remove comments from a C\C++ code

BEGIN {
    check = false
    # variable tells whether field is a part of block comment or not
}

{
    while (NF > 0) {						# while code has non empty fields
        
        # change current line ($0) to line without /* ... */ using match function
        # utilise RSTART and RLENGTH properties we store required record

        if (check == 0) {					# if outside block comment
            if (match($0, /\/\*/)) {				# if occurence of /* is found while outside comment implies beginning of comments
                printf ("%s", substr($0, 1, RSTART - 1))	# print upto /* not including /* string
                $0 = substr($0, RSTART)				# change record to desired string
                check = 1					# change presence check to present inside string(i.e 1)
            } else {
                print
                break						# no occurences were found in current record so break while loop to next record
            }

        } else {  						# if inside block comment

            if (match($0, /\*\//)) {				# if occurence of /* found while inside block comment
                $0 = substr($0, RSTART + RLENGTH)		# store after */ inside record
                check = 0					# change presence check to present outside string (i.e 0)
            } else {
                break						# no occurences were found in current record so break while loop to next record
            }

        }
    }
}
END {
    printf("\n")						# move to new line once the code has been traversed through
}
