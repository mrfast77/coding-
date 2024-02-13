import sys
import csv

def main():
    
    if len(sys.argv) != 2:
        print("There must be 1 command-line argument")
        sys.exit()

    if not str(sys.argv[1]).endswith(".csv"):
        print("You must enter a CSV file")
        sys.exit()

    try:
        with open(sys.argv[1]) as file:
            reader = csv.DictReader(file)
            with open("people_2.csv", "w") as new_file:
                writer = csv.DictWriter(new_file, fieldnames=["first", "last", "house"])
                writer.writeheader()
                for row in reader:
                    full_name = row['name'].split(',')
                    first = full_name[1].lstrip()
                    last = full_name[0]
                    writer.writerow({'first': first, 'last': last, 'house': row['house']})

    except FileNotFoundError:
        print("File not found")
        sys.exit()

if __name__ == "__main__":
    main()