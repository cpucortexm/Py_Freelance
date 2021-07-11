# to get how many hours and minutes the author spent in each file.
# The timelog file name will be an argument for your Python program.
import argparse
import re


def main(filename):
    """
        This is the main() function, which takes time log file name as input. Starts extracting the time stamp am and pm.
        Adds the individual hrs and mins to generate the final hours and min spent in the input log file.
        Prepares the dictionary with hrs and mins to print to a report
    """
    print("Start parsing:", filename)
    total_hr_spent_per_file = 0
    total_min_spent_per_file = 0
    with open(filename) as file:
        start_calculation = False
        for line in file:
            if 'time log' in line.lower():  # start time calculations now
                start_calculation = True
                continue  # no need to parse text with 'time log:' line

            if start_calculation:
                # print(line)
                timeslogged = re.findall(r'\b\d+:\d+[aAmMpP]+',
                                         line)  # \b\d = match word boundary which ends with a digit

                if timeslogged:  # is cannot be used because it compares addresses
                    pos = timeslogged[0].index(':')
                    meridian = timeslogged[0][-2:]  # last 2 chars are 'am' or 'pm'
                    hr1, min1 = calculate_hr_mins(pos, meridian, timeslogged[0])

                    pos = timeslogged[1].index(':')
                    meridian = timeslogged[1][-2:]  # last 2 chars are 'am' or 'pm'
                    hr2, min2 = calculate_hr_mins(pos, meridian, timeslogged[1])

                    # At this stage we extracted hrs and mins spent for a given day. Now get the difference
                    # to know the actual time spent on the log for that particular day.

                    total_hr_perslot, total_min_perslot = difference(hr1, min1, hr2, min2)
                    print('total time per slot hr:min', total_hr_perslot, total_min_perslot)

                    # keep adding to the total time spent per file
                    total_hr_spent_per_file += total_hr_perslot
                    total_min_spent_per_file += total_min_perslot

                    if total_min_spent_per_file > 60:
                        total_hr_spent_per_file += 1
                        total_min_spent_per_file = total_min_spent_per_file % 60

    print('total time per file hr:min', total_hr_spent_per_file, total_min_spent_per_file)

    # Prepare dictionary with key, values to write to the report file
    timeconsumedinfile = {
        'filename': filename,
        'consumed_hrs': total_hr_spent_per_file,
        'consumed_mins': total_min_spent_per_file
    }
    generateReport(timeconsumedinfile)


def calculate_hr_mins(pos, meridian, timelogged):
    """
       It takes position of : present in the time stamp, meridian (am or pm) and the complete time stamp.
       From time stamp it separates hr and mins. Based on am or pm does necessary modifications for hr
    """
    assert (0 < pos <= 2)  # pos for hr can be 1 or 2 digits e.g. 4: or 10:
    assert (meridian != "am" or meridian != "pm")  # pos for hr can be 1 or 2 digits e.g. 4: or 10:
    hr = int(timelogged[0])  # string first element is always hr
    mins = int(timelogged[pos + 1:pos + 3])
    if pos == 2:
        hr = int(timelogged[0:2])

    if meridian == "am" and hr == 12:
        hr = 0
    elif meridian == "pm" and hr != 12:
        hr += 12
    print('time in hrs:mins', hr, mins)
    return hr, mins


def difference(h1, m1, h2, m2):  # enter in h1,h2 hrs. For am 00-12, for pm 12-24
    """
        difference() calculates the time difference between inputs times t1 = hr1, min1 and t2 = hr2,min2
        From time stamp it separates hr and mins. Based on am or pm does necessary modifications to get
        exact hours and mins from the two times.
    """
    # convert h1 : m1 into
    # minutes
    t1 = h1 * 60 + m1

    # convert h2 : m2 into
    # minutes
    t2 = h2 * 60 + m2

    if t1 == t2:
        print("Both are same times")
        return 0, 0
    else:

        # calculating the difference
        diff = t2 - t1

    # calculating hours from
    # difference
    h = (int(diff / 60)) % 23
    # calculating minutes from
    # difference
    m = diff % 60

    return h, m


def generateReport(timeconsumedinfile):  # timeconsumedinfile is a dictionary and must contain total_hrs and total_mins
    """
        generateReport() takes input dictionary and prints it to the report in a user readable format
    """
    TEMPLATE = '''
        ========================

        Total time spent in {filename} 
        consumed_hrs: {consumed_hrs}
        consumed_mins: {consumed_mins}

        ========================
        '''
    report = TEMPLATE.format(**timeconsumedinfile)  # {}: curly braces are not used before format.
    # in such case dict keys will be passed as default with values as **dict to format()
    print(report)

    with open('Report.txt', 'w') as file:
        file.write(report)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('timelogfile', type=str, help='time file to parse')
    args = parser.parse_args()
    main(args.timelogfile)
