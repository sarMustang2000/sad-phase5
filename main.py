from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from typing import ItemsView, Literal

DB_ROOT_PATH = "./dbs/"

STATS = ["EMPTY", "IN_PROGRESS", "PAYED", "ON_THE_WAY", "CLOSED"]
DRIVERS_STAT = ["ready", "busy"]
DATE_FORMAT = "%d/%m/%y %H:%M:%S"


class DateTime:
    def __init__(self, date: str) -> None:
        self.__date = date

    def getDate(self):
        return datetime.strptime(self.date, DATE_FORMAT)

    def __str__(self) -> str:
        return self.__date


class Address:
    def __init__(self, address: str) -> None:
        self.__address = address

    def getAddress(self):
        return self.__address

    def __str__(self) -> str:
        return self.__address


class Person:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        username: str,
        password: str,
        phone_number: str,
        address: str,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.address = address


class User(Person):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        username: str,
        password: str,
        phone_number: str,
        address: str,
    ) -> None:
        super().__init__(
            first_name, last_name, username, password, phone_number, address
        )
        self.requests = []
        self.credit = 0

    def addCredit(self):
        pass

    def is_me(self, username: str, password: str) -> bool:
        if username == self.username and password == self.password:
            return True
        return False


@dataclass
class Worker(Person):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        username: str,
        password: str,
        phone_number: str,
        address: str,
        status: str = "ready",
    ) -> None:
        super().__init__(
            first_name, last_name, username, password, phone_number, address
        )
        self.status = status

    def getStatus(self):
        return self.status

    def changeStatus(self):
        self.status = "ready" if self.status == "busy" else "busy"


@dataclass
class Expert(Worker):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        username: str,
        password: str,
        phone_number: str,
        address: str,
        status: str,
    ) -> None:
        super().__init__(
            first_name, last_name, username, password, phone_number, address, status
        )


@dataclass
class Driver(Worker):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        username: str,
        password: str,
        phone_number: str,
        address: str,
        status: str,
    ) -> None:
        super().__init__(
            first_name, last_name, username, password, phone_number, address, status
        )

    def getSched(self):
        pass

    def updateSched(self):
        pass


class Request:
    def __init__(self) -> None:
        self.status = "EMPTY"
        self.price = None
        self.__req_type = type(self).__name__
        self.user = None

    def setStatus(
        self,
        status: Literal["EMPTY", "IN_PROGRESS", "PREPAYED", "ON_THE_WAY", "CLOSED"],
    ):
        self.status = status

    def setUser(self, user: User):
        self.user = user

    def getStatus(self):
        return self.status

    def getPrice(self):
        return self.price

    def __str__(self) -> str:
        return ",".join(
            [self.status, self.__req_type, str(self.price), self.user.username]
        )


@dataclass
class Transfer(Request):
    def __init__(self) -> None:
        super().__init__()
        self.__src_address = None
        self.__dest_address = None
        self.driver = None
        self.__value = 0
        self.__type = None
        self.__date_time = None

    def calcPrice(self):
        self.price = 1000

    def setValue(self, value: str):
        self.__value == value

    def setAddress(self, src_addr: Address, dest_addr: Address):
        self.__src_address = src_addr
        self.__dest_address = dest_addr

    def setType(self, itmeType: str):
        self.__type = itmeType
        self.calcPrice()

    def setDriver(self, driver: Driver):
        self.driver = driver

    def setExpert(self, expert: Expert):
        pass

    def setDateTime(self, date_time: str):
        self.__date_time = DateTime(date_time)

    def getValue(self):
        return self.__value

    def getAddress(self):
        return (self.__src_address, self.__dest_address)

    def getDate(self):
        return self.__date

    def setDriver(self, driver: Driver):
        self.driver = driver

    def getType(self):
        return self.__type

    def __str__(self) -> str:
        return ",".join(
            [
                super().__str__(),
                str(self.__src_address),
                str(self.__dest_address),
                self.driver.username,
                str(self.__value),
            ]
        )


@dataclass
class OnlinePayment:
    def pay(self, amount: str) -> bool:
        return True


@dataclass
class TransferSystemRunner:
    def __enter__(self):
        print(f"Welcome to {type(self).__name__}")
        self.dal = DataAccessLayer()
        self.users = self.dal.getUsers()
        self.workers = self.dal.getWorkers()
        self.entered_user = None
        self.requests = self.dal.getRequests()
        return self

    def __exit__(self, *exceptions):
        print(f"Goodbye")

    def getFreeDateTimes(self):
        pass

    def getFreeExpertsTimes(self):
        pass

    def setBestDriver(self, request: Request):
        request.setDriver(self.workers["reza"])
        self.workers["reza"].changeStatus()

    def run(self, command: str) -> None:
        if command == "login":
            username = input("Username: ")
            password = input("Password: ")
            if username in self.users.keys():
                if self.users[username].is_me(username, password):
                    self.entered_user = self.users[username]
                    print("You loggedin successfully")
            else:
                raise ValueError("User doesn't exist")
        elif command == "create_transfer_request":
            new_transfer_request = Transfer()
            self.requests.append(new_transfer_request)
            new_transfer_request.setUser(self.entered_user)
            self.getFreeDateTimes()
            date_time = input("date and time: ")
            new_transfer_request.setDateTime(date_time)
            new_transfer_request.setStatus("IN_PROGRESS")
            src_addr = input("source address: ")
            dest_addr = input("destination address: ")
            new_transfer_request.setAddress(src_addr, dest_addr)
            is_non_residential = input("is_non_residential(yes/no): ") == "yes"
            if not is_non_residential:
                is_expert_needed = input("is_expert_needed: ") == "yes"
                if not is_expert_needed:
                    value = input("value in KG: ")
                    new_transfer_request.setValue(value)

            if is_non_residential or is_expert_needed:
                self.getFreeExpertsTimes()
                expertise_time = input("expertise_time: ")
                pass

            items_type = input("Items type: ")
            new_transfer_request.setType(items_type)

            prepayment = new_transfer_request.getPrice() * 0.3
            print(f"Prepayment value is: {prepayment}")
            if input("Do you do the prepayment(or Cancel): ") == "yes":
                op = OnlinePayment()
                payment_result = op.pay(prepayment)
                if payment_result:
                    new_transfer_request.setStatus("PREPAYED")

                self.setBestDriver(new_transfer_request)

                new_transfer_request.setStatus("ON_THE_WAY")

                new_transfer_request.setStatus("CLOSED")

                payment_result = op.pay(prepayment)
                while not payment_result:
                    payment_result = op.pay(prepayment)

                new_transfer_request.setStatus("CLOSED")
                new_transfer_request.driver.changeStatus()

            self.dal.add_new_transfer_request(new_transfer_request)

        else:
            raise ValueError("Bad command")


@dataclass
class DataAccessLayer:
    db_file_path = DB_ROOT_PATH

    def __init__(self) -> None:
        self._load_dbs()

    def add_new_transfer_request(self, request: Request):
        with open(self.db_file_path + "requests.csv", "a") as requests_file:
            requests_file.write("\n" + str(request))

    def add_new_user(self, user: User):
        pass

    def add_new_worker(self, worker: Worker):
        pass

    def _load_dbs(self):
        users = {}
        workers = {}
        requests = []
        if Path(self.db_file_path + "users.csv").is_file():
            with open(self.db_file_path + "users.csv") as users_db:
                lines = users_db.readlines()
                for line_ind in range(1, len(lines)):
                    (
                        first_name,
                        last_name,
                        user_name,
                        password,
                        phone_number,
                        address,
                    ) = lines[line_ind].split(",")
                    users[user_name] = User(
                        first_name,
                        last_name,
                        user_name,
                        password,
                        phone_number,
                        address,
                    )

            self.users = users
        if Path(self.db_file_path + "workers.csv").is_file():
            with open(self.db_file_path + "workers.csv") as workers_db:
                lines = workers_db.readlines()
                for line_ind in range(1, len(lines)):
                    (
                        first_name,
                        last_name,
                        user_name,
                        password,
                        phone_number,
                        address,
                        role,
                        status,
                    ) = lines[line_ind].split(",")
                    if role == "driver":
                        workers[user_name] = Driver(
                            first_name,
                            last_name,
                            user_name,
                            password,
                            phone_number,
                            address,
                            status,
                        )
            self.workers = workers
        if Path(self.db_file_path + "requests.csv").is_file():
            with open(self.db_file_path + "requests.csv") as requests_db:
                lines = requests_db.readlines()
                for line_ind in range(1, len(lines)):
                    (
                        status,
                        req_type,
                        price,
                        username,
                        src_addr,
                        dest_addr,
                        driver,
                        value,
                    ) = lines[line_ind].split(",")
                    if req_type == "transfer":
                        requests.append(
                            Transfer(
                                status,
                                type,
                                price,
                                username,
                                src_addr,
                                dest_addr,
                                driver,
                                value,
                            )
                        )
            self.requests = requests

    def getUsers(self):
        return self.users

    def getWorkers(self):
        return self.workers

    def getRequests(self):
        return self.requests


if __name__ == "__main__":
    with TransferSystemRunner() as tsr:
        while True:
            print(">> ", end="")
            command = input()
            if command == "quit":
                break
            try:
                tsr.run(command)
            except Exception as msg:
                print(msg)
