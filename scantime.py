



def getStartingTime(fileName):
    '''
    Function : getStartingTime

    Description : This function returns the starting time for NMR scan in seconds.

    Usage : final_time = getStartingTime(fileName)

    Arguments : fileName  - the name of the file having starting time

    Returns : final_time - the starting time in seconds.
    '''
    import sys
    try:
        file = open(fileName, 'r')
        lines = file.readlines()
    except:
        print("Error in opening file.:: %s"%fileName)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+ WARNING : Scan time calcualted up to this scan !!!  +")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        return None
    req_line = ""
    for line in lines:
        if ('started at' in line):
            req_line = str(line)

    if req_line == "":
        print("May have formatting error in NMR file: %s"%(fileName))
        sys.exit()
    splited_line = req_line.split()
    begin_time = splited_line[3]
    
    hhmmss = begin_time.split(':')


    hh = float(hhmmss[0])
    mm = float(hhmmss[1])
    ss = float(hhmmss[2])

    final_time = (hh*3600) + (mm*60) + ss

    return(final_time)


def time_difference(t_list, ref_time):
    '''
    Function : time_difference

    Description : This function returns the list of time difference from reference time.

    Usage : time_list = time_difference(t_list, ref_time)

    Arguments : t_list -list of time
                ref_time -reference time of NMR scan

    Returns : time_list -list of time difference from reference time
    

    '''
    difference = []
    
    for index in range(0, len(t_list)):
        diff = t_list[index]- ref_time
        difference.append(diff)
    
    return difference


def nmr_scantime(input_dir, time_hour, time_min, time_sec, output_name):
    '''

    Function : nmr_scantime

    Description : This function dumbs the nmr elapsed time for each scan into a file

    Usage : nmr_scantime(input_dir, time_hour, time_min, time_sec, output_name)

    Arguments : input_dir -directory where nmr scans are located
                time_hour -hour of reference time
                time_min -minute of reference time
                time_sec -second of reference time
                output_name -name of the file where you want to dump all informations 
    


    '''
    import os
    
    directory = input_dir
    outfile_name = output_name
    
    reference_time = time_hour * 3600 + time_min * 60 + time_sec

    dirlist = os.listdir(directory)
    newlist = []
    
    

    for num in dirlist:
        if num.isdigit() == True:
            int_num = int(num)        
            newlist.append(int_num)
           

    newlist.sort()       
    
    time_list = [] 

    for num in newlist:
        file_path = directory + str(num) + "/audita.txt"
        print("Reading time from %s"%(file_path))
        time = getStartingTime(file_path)
        if time == None:
            break
        time_list.append(time)
    
    
    
    time_difference_in_seconds = time_difference(time_list, reference_time)

    outfile = open(outfile_name, 'w')
    outfile.write("## NMR-Folder_Name: %s\n"%(input_dir))
    outfile.write("## Reference_time : %d:%d:%f\n"%(time_hour, time_min, time_sec))
    outfile.write('# Scan_number\tStarting_time(min)\tTime_difference(min)\n')
    
    
    for index in range(len(time_list)):
        outfile.write("%d\t%f\t%f\n"%(newlist[index],time_list[index]/60.0,time_difference_in_seconds[index]/60.0))
    
    
    outfile.close()
                   






if __name__ == "__main__":
    import argparse
    import os
    import sys




    parser = argparse.ArgumentParser(
        prog='SCANTIME',
        formatter_class=argparse.RawDescriptionHelpFormatter,
         description='''Calculates NMR elapse time from some reference time and generates
         a output file with all informations.''',
     epilog='''
            Example: python scantime.py -i ~/Desktop/NMR/ECD/ --hh 16 --mm 36  --ss 45.50 -o ECD_scan.txt\n
            
            Note:If the NMR scans for ECD is located at ~/Desktop/NMR/ECD/ and the referecne time noted
            is 16:36:45.50. To generate the elapse time and save to ECD_scan.txt. Use above as an example.
             ''')
   
    parser.add_argument('-i','--input', dest='input_dir',type = str, action='store', help="provide directory containing all the scans",required = True)
    parser.add_argument('-hh','--hour', dest='time_hour', type = int, action='store', help="provide hour of your reference time in 24 hr format", required = True)
    parser.add_argument('-mm','--min', dest='time_min', type = int, action='store', help="provide minutes of your reference time", required = True)
    parser.add_argument('-ss','--sec', dest='time_sec', type = float, action='store', help="provide seconds of your reference time", required = True)

    parser.add_argument('-o', '--output', dest = 'output_name', type= str, action = 'store', help = 'provide output name for the final elapsed time', required = True)
    args = parser.parse_args()




    input_dir = args.input_dir
    time_hour = args.time_hour
    time_min = args.time_min
    time_sec = args.time_sec

    output_name = args.output_name

    if os.path.exists(input_dir) == False:
        print("\n\t\t\t++++++++++++++++++++++++++++++++++++++++++")
        print('\t\t\t+  The given directory doesnot exists!!!!  +')
        print("\t\t\t++++++++++++++++++++++++++++++++++++++++++++\n")
        parser.print_help()
        sys.exit()



        



    nmr_scantime(input_dir, time_hour, time_min, time_sec, output_name)

                              