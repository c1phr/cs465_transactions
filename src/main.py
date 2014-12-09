from manager import Manager

def main():
    print("Welcome to the Transactions program\n")
    choice = input("Would you like to timeout based on number of transactions or a time limit? (n / t)\n")
    if choice is "n":
        num_time = input("How many transactions do you want to run?\n")
        string = "transactions"
    else:
        num_time = input("How many seconds should the program run?\n")
        string = "time"
    init_val = input("What should the initial cubby value be?\n")
    num_cubby = int(input("How many cubbyholes would you like to create?\n"))
    lock_enabled = input("Enable locking? (y/n)\n")
    if lock_enabled == 'n':
        lock_enabled = False
        lock_str = 'No'
    else:
        lock_enabled = True
        lock_str = "Yes"
    print("Cubbyholes: {0}, Initial Value: {1}, Terminate: {2} {3}, Locking: {4} \n".format(num_cubby, init_val, num_time, string, lock_str))

    start_agent = Manager(num_cubby, init_val, lock_enabled, string, num_time)
    start_agent.run()

main()