import sys

# this was the number to replace the zero for the LKH solver input format
LKH_CITY_ZERO = 41012

def main():
    lkh_tour_file_path = sys.argv[1]
    with open(lkh_tour_file_path, 'r') as lkh_tour_file:
        # ignore first 6 lines
        for i in range(6):
            lkh_tour_file.readline()
        first_city = int(lkh_tour_file.readline())
        print first_city
        for line in lkh_tour_file:
            if int(line) == LKH_CITY_ZERO:
                print 0,
            elif int(line) == -1:
                print first_city,
                # by breaking the loop we ignore the last line
                break
            else:
                print line,

if __name__ == "__main__":
    main()
