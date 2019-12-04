def read_file():
    """Returns contents of input file

    """
    try:
        with open('C:/Users/Deepali Mayekar/Documents/input.txt') as content_file:  # One time setup
            content = content_file.read()
            print(" ")
            print('Input file details printing')
            print(" ")
            print("Input File_name is" + content)
    except FileNotFoundError:
        print("Please provide file name in the txt file suggested ")
    with open(content, 'r') as f:
        proposals = f.readlines()
        # print("Printing proposals list in read operation ")
    content_file.close()
    f.close()
    return proposals


def parse_file_contents(proposals):
    """

    :type proposals: list
    Reads the file and separates Proposal and time
    """

    proposal_matrix = [[0 for x in range(4)] for y in range(len(proposals))]

    for i in range(0, len(proposals)):
        file_line_content = proposals[i].rstrip("\n")

        if file_line_content.endswith("min"):
            assert isinstance(file_line_content, str)
            length_of_string = len(file_line_content)
            assert isinstance(length_of_string, int)

            proposal_string = file_line_content[0:length_of_string - 5]
            mins = file_line_content[length_of_string - 6:length_of_string]
            proposal_matrix[i][0] = str(proposal_string)
            proposal_matrix[i][1] = int(mins.strip("min"))

        else:
            if file_line_content.endswith('ning'):  # This is special timing and value is assumed to be 0
                length_of_string = len(file_line_content)
                proposal_string = file_line_content[0:length_of_string - 9]
                proposal_matrix[i][0] = proposal_string
                proposal_matrix[i][1] = int(0)

    if len(proposal_matrix) == 0:
        print("Today's file was empty, hope that was the intent")

    return proposal_matrix


input_matrix = parse_file_contents(read_file())


def conference_tracks_finder(input_matrix):  # Method written to calculate tracks when necessary
    MAX_TIME_ALLOWED_IN_DAY = 420
    number_of_tracks = 0

    total_input_mins = 0
    for i in range(0, len(input_matrix)):
        total_input_mins = total_input_mins + input_matrix[i][1]
    tracks_finder = total_input_mins % MAX_TIME_ALLOWED_IN_DAY

    if tracks_finder == 0:
        number_of_tracks = total_input_mins / MAX_TIME_ALLOWED_IN_DAY
        return number_of_tracks

    if tracks_finder > 0:
        no_of_tracks = (total_input_mins - tracks_finder) / MAX_TIME_ALLOWED_IN_DAY
        no_of_tracks = int(no_of_tracks) + 1
    return no_of_tracks
    # return nooftracks


no_of_tracks = int(conference_tracks_finder(input_matrix))


def conference_planner(input_matrix):
    """Returns a 2D matrix with Morning / Afteroon and track numbers
    """
    MAX_TIME_ALLOWED_IN_MORNING = 180
    MAX_TIME_ALLOWED_IN_AFTERNOON = 240
    morning_afternoon = "M"  # Flag to determine if the topic is for morning or afternoon
    sum_time_morning = 0  # Calculates the sum of the time planned in morning
    sum_time_afternoon = 0  # Calculates the sum of the time planned in morning
    temp_no_of_tracks = 1

    for i in range(0, len(input_matrix)):
        if morning_afternoon == "M":
            sum_time_morning = sum_time_morning + input_matrix[i][1]
            if sum_time_morning <= MAX_TIME_ALLOWED_IN_MORNING:  # Based on the home assignment shared morning can
                # have so many mins only
                input_matrix[i][2] = "M"
                input_matrix[i][3] = temp_no_of_tracks
            else:
                sum_time_afternoon = input_matrix[i][1]
                morning_afternoon = "A"  # Switch to Afternoon
                input_matrix[i][2] = morning_afternoon
                input_matrix[i][3] = temp_no_of_tracks
        else:
            sum_time_afternoon = sum_time_afternoon + input_matrix[i][1]
            if sum_time_afternoon <= MAX_TIME_ALLOWED_IN_AFTERNOON:  # Based on the home assignment shared
                # afternoon can have so many mins only
                morning_afternoon = "A"  # Switch to afternoon
                input_matrix[i][2] = morning_afternoon
                input_matrix[i][3] = temp_no_of_tracks
            else:
                sum_time_afternoon = input_matrix[i][1]
                morning_afternoon = "M"  # Switch to morning
                temp_no_of_tracks += 1  # Switch to new track
                sum_time_morning = input_matrix[i][1]
                input_matrix[i][2] = morning_afternoon
                input_matrix[i][3] = temp_no_of_tracks
    # print(input_matrix)
    return input_matrix


output = conference_planner(input_matrix)


def conference_planner_printer(output):
    """

    Prints in formatted manner

    """
    START_TIME_CONSTANT = "09:00AM"  # these constants (also below) can be altered to change the lunch and start time
    POST_LUNCH_START = "01:00PM"
    post_lunch = ""
    time_start_hh = 9
    str_time_start_hh = "09"
    str_time_start_mm = "00"
    time_start_mm = 0
    time_am_pm = "AM"
    # time_formatted = "9:00 AM"
    track_flag = "Y"
    track_counter = 0
    for i in range(0, len(output)):
        # Simple code to write the Tracks and number
        if track_flag == "Y":
            if i == 0:
                print("   ")
                print("Track : " + str(output[i][3]))
                print("   ")
            track_flag = "N"

        if i > 0:
            track_counter = 0
            if track_flag == "N":
                track_counter = int(output[i][3]) - int(output[i - 1][3])
            if track_counter > 0:
                track_flag = "Y"
                if i > 0:
                    print("05:00PM Networking ")
                    print("   ")
                print("   ")
                print("Track : " + str(output[i][3]))
                print(" ")
                time_start_mm = int(output[i][1])
                time_start_hh = 9
                print(START_TIME_CONSTANT + " " + str(output[i][0]) + str(output[i][1]) + "min")
                track_counter = int(output[i][3]) - int(output[i - 1][3])

        else:
            print(str_time_start_hh + ":" + str_time_start_mm + time_am_pm + " " + str(output[i][0]) +
                  str(output[i][1]) + "min")
            time_start_mm = time_start_mm + int(str(output[i][1]))
            if time_start_mm >= 60:
                time_start_hh += 1
                time_start_mm = time_start_mm - 60

        if i > 0:
            if track_flag == "N":
                if output[i][2] == "A":
                    time_am_pm = "PM"
                else:
                    time_am_pm = "AM"
                if output[i][2] == "A":
                    if output[i - 1][2] == "M":
                        post_lunch = "Y"
                        time_start_hh = 12
                if time_start_mm < 10:
                    str_time_start_mm = "0" + str(time_start_mm)
                else:
                    str_time_start_mm = str(time_start_mm)
                if time_start_hh < 10:
                    str_time_start_hh = "0" + str(time_start_hh)
                else:
                    str_time_start_hh = str(time_start_hh)
                if time_start_hh == 12:
                    post_lunch = "Y"
                    print("12" + ":" + "00" + "PM Lunch")
                    time_start_hh = 1
                    time_start_mm = output[i][1]
                    print(POST_LUNCH_START + " " + str(output[i][0]) + str(output[i][1]) + "min")
                    if post_lunch == "Y":
                        post_lunch = ""

                else:
                    print(str_time_start_hh + ":" + str_time_start_mm + time_am_pm + " " + str(output[i][0]) +
                          str(output[i][1]) + "min")
                    time_start_mm = time_start_mm + int(str(output[i][1]))
                    if time_start_mm >= 60:
                        time_start_hh += 1
                        time_start_mm = time_start_mm - 60
        track_flag = "N"
    print("05:00PM Networking ")
    print("   ")


conference_planner_printer(output)
