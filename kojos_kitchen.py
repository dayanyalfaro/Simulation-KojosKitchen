from random import uniform
import math


def exponential(lamda=1/4):
    u = uniform(0, 1)
    e = - (1 / lamda) * math.log(u)
    return e


class Customer():
    def __init__(self, id):
        self.id = id
        self.arrive = None
        self.departure = None
        self.attended = None
        self.order = 0 if uniform(0, 1) > 1/2 else 1  # 0: sushi # 1: sandwich

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


def attend_customer_time(order):
    if order:
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
    attended_by_worker = [0 for _ in range(n)]

    if rush_hour_worker:
        workers.append(math.inf)  # it is gonna be unavailable until rush hours
        service_time.append(math.inf)
        attended_by_worker.append(0)

    customers = {}
    customers_to_attend = []

    t_a = exponential()

    while True:
        if rush_hour_worker:
            rush_hour = is_rush_hour(elapsed_time)
            # is rush hour and extra worker is not working
            rush_hour_start = rush_hour and math.isinf(workers[-1])
            # rush hour ended and extra worker is empty
            rush_hour_finish = not rush_hour and workers[-1] == 0
            if rush_hour_start:
                # activate rush hour worker
                workers[-1] = 0
            if rush_hour_finish:
                # deactivate rush hour worker
                workers[-1] = math.inf
                service_time[-1] = math.inf

        if t_a <= min(service_time) and t_a <= duration:
            # new arrival
            elapsed_time = t_a
            number_arrives += 1
            number_customers += 1
            customer = customers[number_arrives] = Customer(number_arrives)
            customer.set_arrive(t_a)
            t_a += exponential()

            free_worker = get_free_worker(workers)

            if free_worker != -1:
                # assign worker to attend customer
                customer.set_attended(elapsed_time)
                workers[free_worker] = number_arrives
                service_time[free_worker] = elapsed_time + \
                    attend_customer_time(customer.order)
                attended_by_worker[free_worker] += 1
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
                service_time[i] = elapsed_time + \
                    attend_customer_time(customers[customer_id].order)
                attended_by_worker[i] += 1
            else:
                # release worker
                workers[i] = 0
                service_time[i] = math.inf

    return customers


def estimate_customers_overfive(n, rush_hour_worker):
    total_overfive = 0
    total_customers = 0
    for i in range(n):
        customers = simulate_day_in_Kojos_Kitchen(660, 2, rush_hour_worker)
        overfive = [1 if (customer.attended - customer.arrive) > 5 else 0
                    for customer in customers.values()]

        total_overfive += sum(overfive)
        total_customers += len(customers)
    customers = total_customers / n
    overfive = total_overfive / n
    percent = (overfive / customers) * 100
    return percent


print("Sin extra:")
print(estimate_customers_overfive(1000, False))
# print(attended)
print("------------------------------------------------------")
print("Con extra:")
# print(attended_extra)
print(estimate_customers_overfive(1000, True))
