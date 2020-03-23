from random import uniform
import math


def exponential(lamda=1/2):
    u = uniform(0, 1)
    e = - (1 / lamda) * math.log(u)
    return e


class Customer():
    def __init__(self):
        self.arrive = None
        self.departure = None
        self.attended = None

    def arrive(self):
        return self.arrive

    def departure(self):
        return self.departure

    def attended(self):
        return self.attended

    def set_arrive(self, value):
        self.arrive = value

    def set_departure(self, value):
        self.departure = value

    def set_attended(self, value):
        self.attended = value

    def service_time(self):
        return self.departure - self.arrive


def prepare_sandwich():
    return uniform(3, 5)


def prepare_sushi():
    return uniform(5, 8)


def attend_customer_time():
    x = uniform(0, 1)
    if x < 1 / 2:
        return prepare_sandwich()
    return prepare_sushi()


def get_free_worker(workers):
    for i, worker in enumerate(workers):
        if not worker:
            return i
    return -1


def is_rush_hour(t):
    """
    10: 00 AM (0 min) - 11: 30 AM (90 min) -> no
    11: 30 AM (90 min) - 01: 30 PM (210 min) -> yes
    01: 30 PM (210 min) - 05: 00 PM (420 min)-> no
    05: 00 PM (420 min) - 07: 00 PM (540 min)-> yes
    07: 00 PM (540 min) - 09: 00 PM (660 min)-> no
    """
    first = t >= 90 and t <= 210
    second = t >= 420 and t <= 540
    return first or second


def simulate_day_in_Kojos_Kitchen(duration, n=2, rush_hour_worker=False):
    elapsed_time = 0
    number_arrives = 0
    number_customers = 0
    workers = [0 for _ in range(n)]  # 0-> empty i-> busy attending customer i
    service_time = [math.inf for _ in range(n)]

    if rush_hour_worker:
        workers.append(math.inf)  # it is gonna be unavailable until rush hours
        service_time.append(math.inf)

    customers = {}
    customers_to_attend = []

    t_a = exponential()

    while True:
        if rush_hour_worker:
            if is_rush_hour(elapsed_time):
                # activate rush hour worker
                if math.isinf(workers[-1]):
                    workers[-1] = 0
            elif workers[-1] == 0:
                # deactivate rush hour worker
                workers[-1] = math.inf
                service_time[-1] = math.inf

        if t_a <= min(service_time) and t_a <= duration:
            # new arrival
            elapsed_time = t_a
            number_arrives += 1
            number_customers += 1
            customer = customers[number_arrives] = Customer()
            customer.set_arrive(t_a)
            t_a += exponential()

            free_worker = get_free_worker(workers)

            if free_worker != -1:
                # assign worker to attend customer
                customer.set_attended(elapsed_time)
                workers[free_worker] = number_arrives
                service_time[free_worker] = elapsed_time + \
                    attend_customer_time()
            else:
                customers_to_attend.append(number_arrives)
        else:
            if t_a > duration and not number_customers:
                overtime = max(elapsed_time - duration, 0)
                break

            # attend customers
            t_i = min(service_time)
            elapsed_time = t_i
            i = service_time.index(t_i)
            customer = workers[i]
            customers[customer].set_departure(t_i)
            number_customers -= 1

            if customers_to_attend:
                # attend first customer in queue
                customer_id = customers_to_attend.pop(0)
                workers[i] = customer_id
                customers[customer_id].set_attended(t_i)
                service_time[i] = elapsed_time + attend_customer_time()
            else:
                # release worker
                workers[i] = 0
                service_time[i] = math.inf

    return customers


customers = simulate_day_in_Kojos_Kitchen(660, rush_hour_worker=False)
customers_extra = simulate_day_in_Kojos_Kitchen(660, rush_hour_worker=True)


a = [(customer.departure - customer.attended)
     for customer in customers.values()]
b = [(customer.departure - customer.attended)
     for customer in customers_extra.values()]
print("Sin extra:")
print(a)
print("------------------------------------------------------")
print("Con extra:")
print(b)
