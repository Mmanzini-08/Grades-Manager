import os
import re
import sys
import json
import matplotlib.pyplot as plt


def main():
    subj = '' #to declare the variable since it's a problem for the else here
    try:
        with open('subjects.example.json', 'r') as file:
            pdata = json.load(file) #this is the data gotten from the JSON file converted into python
    except json.JSONDecodeError as err:
        print("Error parsing JSON file:", err)

    math = pdata["subjects"]["math"] #now math exists since the program sees only subjects
    physics = pdata["subjects"]["physics"] #now physics exists
    science = pdata["subjects"]["science"] #now even science exists, wow!

    #this is used to check if this particular variable is used in the program
    #so that the first time it says something and after wards something else
    if "RESTARTED" not in os.environ:
        print("Welcome to grade_calculator!")
        print("What subject are you interested in?\n"
                     "The available subjects are:")
        for subject in pdata["subjects"]:
            print("-", subject)
        print("Which subject would you like to take into consideration: ", end = '')
        #you can now set the "flag" so that the next time you run the program can know it's a restart
        os.environ["RESTARTED"] = "true"
        os.environ["SSUBJ"] = subj
    else:
        subj = os.environ.get("SSUBJ")
        print(f"Do you want to check {subj} again? y/n ", end = '')
        subjd = input()
        while (subjd != 'y' and subjd != 'n'):
            print("Inserted command not recognized, please insert a valid command: ", end ='')
            subjd = input()
        if subjd == 'n':
            print("Please re-insert the subject: ", end = '')

    subj = input()
    if subj == 'math' or subj == 'mathematics':
        subj == 'math'
    elif subj == 'physics' or subj == 'phys':
        subj = 'physics'
    elif subj == 'chem' or subj == 'chemistry' or subj == 'science':
        subj == 'science'

    #truthy or falsy
    if subj:
        current_dict = pdata["subjects"][subj]

    while True:
        print(f"Current subj: {subj.capitalize()}")
        print("Would you like to:\n"
              "\t1) List your votes (l)\n"
              "\t2) Insert new votes (i)\n"
              "\t3) Erase a vote (e)\n"
              "\t4) Erase all vote for the subject (a)\n"
              "\t5) type q to quit  (q)\n"
              "Your choice: ", end = '')
        ans = input()

        if ans not in ('l', 'i', 'e', 'a', 'q'):
            ans = input("Try again: ")
            continue

        if ans == 'q':
            break

        while (ans != 'i' and ans != 'l' and ans != 'e' and ans != 'a'):
            print("Inserted command not recognized, insert a valid command: ", end = '')
            ans = input()
        if (ans == 'e' and (vlver(len(current_dict)) == 1)):
            print("You cannot erase any votes, you haven't inserted any.")
            ans = 'i'

        #Delete votes:
        while (ans == 'e' and (vlver(len(current_dict))) == 0):
            print("Insert the vote you want to delete or quit the function. \n")
            for dele, grade in current_dict.items():
                print("\t", dele, "--->", grade)
            deletor = input("\tvote_name/q: ")
            if (deletor == 'q'):
                break
            try:
                del current_dict[deletor]
                for i, old_key in enumerate(list(current_dict.keys()), start=1):
                    current_dict[f"vote {i}"] = current_dict[old_key]
                    if f'vote {i}' != old_key:
                        del current_dict[old_key]
            except:
                raise TypeError("You did not insert a valid vote name")

        if (ans == 'l' and (vlver(len(current_dict))) == 1):
            print("Grade listing is not available yet as there are no recorded votes inside the program.")
            ans = 'i'

        #vote listing:
        elif (ans == 'l' and (vlver(len(current_dict))) == 0):
            print(f"{subj.capitalize()} votes:")
            for name, grades in current_dict.items():
                print("\t", name, "--->", grades)
            grqs = input("Would you like to visualize a graph of your current progress or quit the function? q/y")
            while (grqs != 'y' and grqs != 'q'):
                print("Input not valid, please re-insert instruction.")
                grqs = input("Re-insert instruction: ")
            if grqs == 'q':
                break
            elif (grqs == 'y'):
                votes = [float(i) for i in current_dict.values()]
                avg = sum(votes) / len(votes)
                x = range(len(votes))
                plt.plot(x, votes, marker="o", label="Votes")
                plt.axhline(y=avg, color="r", linestyle="--", label=f"Average ({avg:.2f})")

                #legend of the graphical environment
                plt.ylabel("Your grades")
                plt.xlabel("Time")
                plt.title("Votes and Average")
                plt.legend()
                plt.show()
            else:
                break
        while (ans == 'i'):
            prompt = input("Please insert a grade or press q to quit the program: ")
            if prompt == 'q':
                break
            try:
                current_dict[f"vote {len(current_dict) + 1}"] = prompt
            except:
                raise ValueError ("You inserted an unacceptable input.")


    with open ('subjects.example.json', 'w') as file: #file is still that as to not get confused and w instead of r because it's write and not read
        json.dump (pdata, file, indent=4)

    print("Do you want to do anything else? y/n", end='')
    dcs = input()
    while (dcs != 'y' and dcs != 'n'):
        print("command not recognized, input another command: ", end='')
        dcs = input()
    if (dcs == 'y'):
        os.execl(sys.executable, sys.executable, *sys.argv)  # restarts the program
    else:
        sys.exit()  # ends the program

def vlver(length):
    if (length == 0 or length == 1):
        return 1
    else:
        return 0

main()