## TimeLogParsing

This project involves reading an input log file with time stamps
and finding the total time spent in the log file in hours and mins.
The report is generated in Report.txt file
Python script file is TimeLogParser.py


## Problem Statement
Write a Python3 program tlparser.py to parse the five given timelog data files to get how many hours and minutes the author spent in each file. 
The timelog file name will be an argument for your Python program.
For example, you run your program on the spirit machine like “python3 timelogparser.py TimeLogCarbon.txt”
a) Your program needs to report the line number if there is something wrong in that line that your Python program cannot parse.
b) Your program start to count the time after it found the hard-coded "Time Log:" (case insensitive, there is a space between Time and Log).
c) The “pm” and “am” should be case insensitive, i.e., 9:10pm or 9:10PM or 9:10pM or 9:10Pm are all valid time value.
d) “9:10pm - 11:40pm” or “9:10pm-11:40pm” or “9:10pm -11:40pm” are all valid time periods, i.e., the spaces between "-" and the time value are not important.

See above in the Small Parser,
Please issue “python3 tlparser.py TimeLogCarbon.txt” on the spirit machine (Python version 3.6.9) to test your Python program before your turnin it.
Please use “if __name__ == ‘__main__’:” in your code and avoid global variables (read sections 2.5 and 3.17 at https://google.github.io/styleguide/pyguide.html).


## How to run the script
On the terminal type

$ python3 TimelogParser.py < Input_Log_File>

e.g.
$ python3 TimelogParser.py TimeLogCarbon.txt

Report is generated in Report.txt
