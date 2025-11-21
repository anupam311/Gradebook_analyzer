# Project Title : Gradebook Analyzer CLI
# Name : Anupam Chaudhary
# Department : B.Tech. C.S.E ( AI/ML ) section-A
# Roll no. 2501730151


import csv

# -------------------------------------------------------
# MANUAL INPUT
# -------------------------------------------------------

def manual_input():
    students = []
    n = int(input("Enter number of students: "))

    for _ in range(n):
        name = input("\nEnter student name: ")

        marks = []
        print("Enter marks for 5 subjects:")
        for i in range(1, 6):
            marks.append(float(input(f"Subject {i}: ")))

        total = sum(marks)
        avg = total / 5

        students.append([name] + marks + [total, avg, None])

    return students, None


# -------------------------------------------------------
# CSV INPUT (Corrected: reads only name + 5 subject marks)
# -------------------------------------------------------

def csv_input():
    filename = input("Enter CSV filename: ")
    students = []

    with open(filename, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header

        for row in reader:

            # Ignore blank rows or class statistics rows
            if len(row) < 6:
                continue

            name = row[0]
            marks = list(map(float, row[1:6]))   # Only 5 marks taken

            total = sum(marks)
            avg = total / 5

            students.append([name] + marks + [total, avg, None])

    print("\nCSV data loaded successfully!")
    return students, filename


# -------------------------------------------------------
# CHOOSE INPUT METHOD
# -------------------------------------------------------

def get_student_data():
    while True:
        print("\n1. Manual Input")
        print("2. Import from CSV")
        print("3. Exit")
        choice = input("Choose desired option code : ")

        if choice == "1":
            return manual_input()
        elif choice == "2":
            return csv_input()
        elif choice == "3":
            exit()
        else:
            print("INVALID ENTRY. Please try Again !!!")


# -------------------------------------------------------
# CLASS STATISTICS
# -------------------------------------------------------

def class_statistics(students):
    averages = [s[7] for s in students]

    highest_student = max(students, key=lambda s: s[7])[0]
    lowest_student = min(students, key=lambda s: s[7])[0]
    class_avg = sum(averages) / len(averages)

    sorted_avg = sorted(averages)
    n = len(sorted_avg)

    if n % 2 == 1:
        median = sorted_avg[n // 2]
    else:
        median = (sorted_avg[n // 2 - 1] + sorted_avg[n // 2]) / 2

    return highest_student, lowest_student, class_avg, median


# -------------------------------------------------------
# GRADE ASSIGNMENT
# -------------------------------------------------------

def assign_grades(students):
    for s in students:
        avg = s[7]

        if avg >= 90:
            s[8] = "A"
        elif avg >= 80:
            s[8] = "B"
            s[8] = "B"
        elif avg >= 70:
            s[8] = "C"
        elif avg >= 60:
            s[8] = "D"
        else:
            s[8] = "F"


# -------------------------------------------------------
# PASS / FAIL
# -------------------------------------------------------

def pass_fail_lists(students):
    passed = [s[0] for s in students if s[7] >= 40]
    failed = [s[0] for s in students if s[7] < 40]
    return passed, failed


# -------------------------------------------------------
# SAVE CLASS STATISTICS TO CSV
# -------------------------------------------------------

def save_class_stats(writer, highest, lowest, class_avg, median):
    writer.writerow([])
    writer.writerow(["CLASS STATISTICS"])
    writer.writerow(["Highest Scorer", highest])
    writer.writerow(["Lowest Scorer", lowest])
    writer.writerow(["Class Average", class_avg])
    writer.writerow(["Class Median", median])


# -------------------------------------------------------
# SAVE RESULTS (MANUAL)
# -------------------------------------------------------

def save_results_manual(students, highest, lowest, class_avg, median):
    filename = input("Enter filename to save CSV: ")

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Sub1", "Sub2", "Sub3", "Sub4", "Sub5",
                         "Total", "Average", "Grade"])

        for s in students:
            writer.writerow(s)

        save_class_stats(writer, highest, lowest, class_avg, median)

    print(f"\nResults saved to {filename}!")


# -------------------------------------------------------
# UPDATE EXISTING CSV (Fix: write to new file)
# -------------------------------------------------------

def update_existing_csv(old_filename, students, highest, lowest, class_avg, median):
    new_filename = "updated_" + old_filename

    with open(new_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Sub1", "Sub2", "Sub3", "Sub4", "Sub5",
                         "Total", "Average", "Grade"])

        for s in students:
            writer.writerow(s)

        save_class_stats(writer, highest, lowest, class_avg, median)

    print(f"\nUpdated data saved to {new_filename}")


# -------------------------------------------------------
# SAVE PROMPT
# -------------------------------------------------------

def ask_to_save(students, csv_file_used, highest, lowest, class_avg, median):
    choice = input("\nDo you want to save/update the CSV file? (y/n): ").lower()
    if choice != "y":
        return

    if csv_file_used is None:
        save_results_manual(students, highest, lowest, class_avg, median)
    else:
        update_existing_csv(csv_file_used, students, highest, lowest, class_avg, median)


# -------------------------------------------------------
# PRINT REPORT (Now shows all 5 subject marks)
# -------------------------------------------------------

def print_report(students, highest, lowest, class_avg, median, passed, failed):
    print("\n==================== STUDENT REPORT ====================")
    print(f"{'Name':<12}{'Sub1':<8}{'Sub2':<8}{'Sub3':<8}{'Sub4':<8}{'Sub5':<8}{'Total':<10}{'Average':<10}{'Grade':<6}")
    print("-------------------------------------------------------------------------------")

    for s in students:
        print(f"{s[0]:<12}{s[1]:<8}{s[2]:<8}{s[3]:<8}{s[4]:<8}{s[5]:<8}{s[6]:<10.2f}{s[7]:<10.2f}{s[8]:<6}")

    print("\n-------------------- CLASS STATISTICS -------------------")
    print(f"Highest Scorer : {highest}")
    print(f"Lowest Scorer  : {lowest}")
    print(f"Class Average  : {class_avg:.2f}")
    print(f"Class Median   : {median:.2f}")

    print("\n---------------- PASS / FAIL SUMMARY -------------------")
    print(f"Passed Students ({len(passed)}): {passed}")
    print(f"Failed Students ({len(failed)}): {failed}")
    print("========================================================\n")


# -------------------------------------------------------
# MAIN PROGRAM
# -------------------------------------------------------

print("Welcome to the Gradebook Analyzer\n")
students, csv_file_used = get_student_data()

highest, lowest, class_avg, median = class_statistics(students)
assign_grades(students)
passed, failed = pass_fail_lists(students)

print_report(students, highest, lowest, class_avg, median, passed, failed)

ask_to_save(students, csv_file_used, highest, lowest, class_avg, median)

