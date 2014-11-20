

def main():
    print("Welcome to the Transactions program\n")
    print("Would you like to timeout based on number of transactions or a time limit? (n / t)\n")
    choice = input()

    if choice is "n":
        print("How many transactions do you want to run?\n")
        string = "transaction(s)"
    else:
        print("How many seconds should the program run?\n")
        string = "second(s)"

    num_time = input()
    print("How many cubbyholes would you like to create?\n")
    num_cubby = input()
    print("Creating {0} cubbyholes and terminating after {1}{2}. \n".format(num_cubby, num_time, string))

main()