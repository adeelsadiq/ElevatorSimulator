'''Author Adeel Sadiq D18125723

Elevator simulator with two methods, one default method (defaultRun) where the elevator starts from Ground floor
and moves to top floor and back, picking customers from each floor and dropping them to their destination on the way.

The second run method, (customRun) takes the first input from the client in the elevator and takes the elevator to
that floor using the customMove function, disembarking any clients that share the destination floor and moves on to
the next destination for client in the elevator, if there is no one in the elevator, it moves floor by floor
using the default move method.


'''

import random

class Building:

    ''''The building class has numbers of floors the elevator list of customers and list of finished customers
    as attribute'''

    def __init__(self, numFloors=0):
        self.numFloors = numFloors
        self.elevator = Elevator(numFloors)
        self.custList = []
        self.finishedCustomers = []

    def __str__(self):
        retStr = '=' + str(80)
        retStr += '\n ' + str(self.elevator)
        retStr += '\n Waiting: ' + str(self.custList)
        retStr += '\n in elevator:' + str(self.elevator.registeredList)
        retStr += '\n Finished: ' + str(self.finishedCustomers)

    def __repr__(self):
        return self.__str__()

    def defaultRun(self):

        '''This run method will start at ground floor and go to the top and come back to the ground floor.
        Picking and dropping all the customers on the way'''

        print("\nthe elevator is on floor number: ", self.elevator.curFloor, '\n')

        for cust in reversed(self.custList):  # reverse reading the list so altering the list does not skip entries

            if self.elevator.curFloor == cust.curFloor and cust not in self.elevator.registeredList:
                self.elevator.registerCust(cust)
                print("| |<--- Customer number", cust.custId, "is in the elevator | |<--- ")
                self.custList.remove(cust)  # Customer is removed form customer list

        for cust in reversed(self.elevator.registeredList):
            if self.elevator.curFloor == cust.destFloor and cust.inElevator is True:

                self.elevator.cancelCust(cust)  # Customer is removed form the elevator registered list
                self.finishedCustomers.append(cust)

        print('\n')
        print("customers waiting:\n ", self.custList, '\n')
        print("customers in elevator:\n ", self.elevator.registeredList, '\n')
        self.elevator.defaultMove()
        print('*-+' * 40)

    def CustomRun(self):

        '''This run method  takes the first input from the client in the elevator and takes the elevator to
that floor using the customMove function, disembarking any clients that share the destination floor and moves on to
the next destination for client in the elevator list, if there is no one in the elevator, it moves floor by floor
using the default move method.'''

        print("the elevator is on floor number: ", self.elevator.curFloor)
        for cust in reversed(self.custList):
            if cust.curFloor == self.elevator.curFloor:
                self.elevator.registerCust(cust)
                print("| |<--- Customer number", cust.custId, "is in the elevator | |<--- ")
                self.custList.remove(cust)

        for cust in self.elevator.registeredList:
            # check if the customers destination is the same as the current floor the elevator is on,
            # if it is cancel the customer
            if self.elevator.curFloor == cust.destFloor:
                self.elevator.cancelCust(cust)

        try:
            # the first customer in the elevator registered list is the one used
            # for the destination of the elevator
            cust = self.elevator.registeredList[0]
            print(cust.custId , ' is the first/next in line, the elevator will now move to their destination floor ',
                  cust.destFloor)
            self.elevator.customMove(cust.destFloor)
        except IndexError:  # to ensure that the elevator doesnt just get stuck at a floor if everyone gets off
            print('elevator empty, moving on\n')
            self.elevator.defaultMove()
        for Customer in reversed(self.elevator.registeredList):

            if self.elevator.curFloor == Customer.destFloor:
                self.finishedCustomers.append(Customer)
                self.elevator.cancelCust(Customer)

        print("customers waiting ", self.custList)
        print("customers in elevator ", self.elevator.registeredList)



class Elevator:

    ''' The Elevator class has number of floors, list of clients in the elevator (registered list), the elevator's
     current floor, direction the elevator is moving (up 1 or down 0) '''

    def __init__(self, floors=0):

        self.numFloors = floors  # The number of floors
        self.registeredList = []  # The list of customers in the elvator
        self.curFloor = 0  # The self floor of the elvator
        # self.direction = random.randint(0, 1)  # The direction of the elevator => -1 = down, 1 = up
        randomMove = [-1, 1]
        self.direction = random.choice(randomMove)
        self.moved = 0

    def __str__(self):

        if self.direction == 1:
            direction = "up"
        else:
            direction = "down"
        '''Output the self state of the elevator'''
        return 'The elevator is on Floor number ' + str(self.curFloor) + ', it is going ' + direction + \
               ' next, it moved ' + str(self.moved) + ' time/s in total'

    def __repr__(self):
        '''This just returns __str__'''
        return self.__str__()

    def defaultMove(self):
        '''The Method to move the elevator by 1 floor'''

        if self.curFloor == self.numFloors - 1:
            self.direction = -1  # if the elevator is at the top floor, direction must be down
        elif self.curFloor == 0:
            self.direction = 1  # if the elvator is at the bottom floor, direction must be up

        self.curFloor = self.curFloor + self.direction
        self.moved += 1
        # print('*******from def move')

    def customMove(self, dest):
        '''The Method to move the elevator to the floor of the first client that comes in the elevator and picks up
        clients from that floor, then moving to the next client's destination floor, also offloads any clients that are
         bound to the same floor, if there are no clients on the destination floor, the elevator will continue moving
         by default method'''

        if dest != self.curFloor or dest is None:
            print("Elevator's next destination is floor number : ", dest)
            self.curFloor = dest
            self.moved += 1
            # print('+++++++from custom move ')
        else:
            self.defaultMove()
        print("the elevator moved to floor number: ", self.curFloor)

    def registerCust(self, customer):
        '''A customer goes into the elevator'''
        self.registeredList.append(customer)
        customer.inElevator = True

    def cancelCust(self, customer):
        '''A customer goes out of the elevator'''
        customer.inElevator = False
        customer.finished = True
        self.registeredList.remove(customer)
        print("| |---> Customer number", customer.custId, "is currently in the elevator on floor", self.curFloor,
              " and their destination is floor number", customer.destFloor, "They are going off the elevator | |---> ")


class Customer(object):
    '''The customer object will be generated using 3 parameters, the current floor, the destination floor and ID'''

    def __init__(self, curFloor, destFloor, custId):
        self.curFloor = curFloor
        self.destFloor = destFloor
        self.custId = custId
        self.inElevator = False
        self.finished = False

    def __str__(self):
        '''A string representation of the customer'''
        return f"Customer ID: {self.custId} Current floor: {self.curFloor}, Destination floor: " \
            f"{self.destFloor}"

    def __repr__(self):
        '''This just returns __str__'''
        return self.__str__()


def main():
    try:
        floors = int(input("Enter number of floors in the building: "))
        # floors = random.randint(2, 15) #this to check the simulator multiple times
        if floors <= 0:
            raise ValueError

    except ValueError:
        print('Number of floors must be a positive number: Exiting!')
        quit()

    try:
        customers = int(input("Enter number of Users in the building: "))
        # customers = random.randint(10, 50)
        if customers <= 0:
            raise ValueError
    except:
        print('Number of customers must be a positive number: Exiting!')
        quit()
    print('+' * 80)
    print('The building has', floors, 'floors and', customers, 'customers')

    my_building = Building(floors)
    # adding customers with random current and destination floor and ID from 1 to the total number of customers

    for cust in range(customers):

        newCustomer = Customer(random.randint(0, floors - 1), random.randint(0, floors - 1), cust + 1)

        # ignore customers where self floors = destination floor as these don't need to use the elevator

        if newCustomer.curFloor != newCustomer.destFloor:
            my_building.custList.append(newCustomer)
            print(newCustomer)

        else:
            # if the customer is already on the destination floor, they are treated as already finsihed.
            my_building.finishedCustomers.append(newCustomer)
            newCustomer.finished = True
            print('****', newCustomer, 'I am already on my floor, dont need the lift ****')

    '''The simulation will run until there are no more customers waiting AND no more customers in the elevator'''

    # Please comment out the function that you do not need to use.

    while not (len(my_building.custList) == 0 and len(my_building.elevator.registeredList) == 0):
        # my_building.defaultRun()
        my_building.CustomRun()

    print("the elevator moved a total ", my_building.elevator.moved, " times")
    print('\n' + ('=' * 80))
    print('Thank you, the simulation has ended')
    print('=' * 80)


if __name__ == '__main__':
    main()
