class Car:
    def __init__(self,make,model,year):
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0
    
    def get_descriptive_name(self):
        long_name = f"{self.year} {self.make} {self.model}"
        return long_name.title()
    
    def read_odometer(self):
        print(f"This car has {self.odometer_reading} miles on it.")

    def update_odometer(self,mileage):
        if mileage >= self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print("You can't roll back an odometer!")
    
    def increment_odometer(self,miles):
        self.odometer_reading += miles

# my_new_car = Car('Maybach','a1','2026')
# print(my_new_car.get_descriptive_name())
# my_new_car.read_odometer()

# my_new_car.odometer_reading = 10086
# my_new_car.read_odometer()

# my_new_car.update_odometer(20000)
# my_new_car.read_odometer()

# my_new_car.update_odometer(3)

# my_new_car.update_odometer(100)
# my_new_car.read_odometer()

# my_new_car.increment_odometer(50)
# my_new_car.read_odometer()

# my_new_car.update_odometer(23_500)
# my_new_car.read_odometer()

class ElectricCar(Car):
    def __init__(self, make, model, year):
        super().__init__(make, model, year)
        self.battery_size = 75

    def describe_battery(self):
        print(f"This car has a {self.battery_size}-kwh battery.")
        
my_tesla = ElectricCar("TESLA","MODEL Y",2025)
print(f"{my_tesla.get_descriptive_name()}")
my_tesla.describe_battery()