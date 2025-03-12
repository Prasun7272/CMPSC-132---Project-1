from abc import ABC, abstractmethod 

# Base Product class
class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def update_quantity(self, new_quantity):
        self.quantity = new_quantity  # Updates product quantity

    def get_product_info(self):
        return (f"Product ID: {self.product_id}, Name: {self.name}, Price: {self.price}, Quantity: {self.quantity}") # Returns product details as a formatted string

# Digital product subclass
class DigitalProduct(Product):
    def __init__(self, product_id, name, price, quantity, file_size, download_link):
        super().__init__(product_id, name, price, quantity)
        self.file_size = file_size
        self.download_link = download_link  # Additional attributes for digital products

    def get_product_info(self):
        return super().get_product_info() + (f", File Size: {self.file_size}, Download Link: {self.download_link}") # Extends the product info with digital product details

# Physical product subclass
class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, quantity, weight, manufacturer):
        super().__init__(product_id, name, price, quantity)
        self.weight = weight
        self.manufacturer = manufacturer  

    def get_product_info(self):
        return super().get_product_info() + (f", Weight: {self.weight}, Manufacturer: {self.manufacturer}") # Extends the product info with physical product details

# Shopping cart class
class Cart:
    def __init__(self):
        self.__items = [] 

    def add_product(self, product):
        self.__items.append(product)  # Adds a product to the cart

    def remove_product(self, product_id): # Removes a product from the cart by product ID
        new_items = []
        for item in self.__items:
            if item.product_id != product_id:
                new_items.append(item)
        self.__items = new_items

    def view_cart(self): # Returns a list of product details in the cart
        cart_info = []
        for item in self.__items:
            cart_info.append(item.get_product_info())
        return cart_info

    def calculate_total(self): # Calculates the total price of all products in the cart
        total = 0
        for item in self.__items:
            total += item.price
        return total

    def apply_discount(self, discount): # Applies a discount strategy to the total price
        total = self.calculate_total()
        return discount.apply_discount(total)

# User class with a shopping cart
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.cart = Cart()  # Each user has their own cart

    def add_to_cart(self, product):
        self.cart.add_product(product) # Adds a product to the user's cart

    def remove_from_cart(self, product_id):
        self.cart.remove_product(product_id) # Removes a product from the user's cart

    def checkout(self, discount=None): # Calculates the total and applies a discount if provided
        total = self.cart.calculate_total()
        if discount:
            total = self.cart.apply_discount(discount)
        self.cart = Cart()  # Clears the cart after checkout
        return total

# Abstract discount class
class Discount(ABC):
    @abstractmethod
    def apply_discount(self, total_amount):
        pass  # Defines an abstract method for discount calculation

# Percentage-based discount class
class PercentDiscount(Discount):
    def __init__(self, percentage):
        self.percentage = percentage 

    def apply_discount(self, total_amount):
        return total_amount * (1 - self.percentage / 100) # Applies a percentage discount to the total amount

# Fixed amount discount class
class FixedAmountDiscount(Discount):
    def __init__(self, amount):
        self.amount = amount

    def apply_discount(self, total_amount): # Applies a fixed discount, ensuring the total isn't negative
        if (total_amount - self.amount) < 0:
          return 0
        return total_amount - self.amount 


# Testing
product = Product(1, "Test Product", 100, 10)
print(product.get_product_info())
product.update_quantity(5)
print(product.get_product_info())

digital_product = DigitalProduct(2, "Test Digital Product", 100, 1, "Test File Size", "Test Download Link")
print(digital_product.get_product_info())

physical_product = PhysicalProduct(3, "Test Physical Product", 100, 1, "Test Weight", "Test Manufacturer")
print(physical_product.get_product_info())

cart = Cart()
cart.add_product(product)
cart.add_product(digital_product)
print(cart.view_cart())
print("Total:", cart.calculate_total())
cart.remove_product(1)
print(cart.view_cart())

user = User(1, "User 1")
user.add_to_cart(physical_product)
print(user.cart.view_cart())
user.remove_from_cart(3)
print(user.cart.view_cart())

percent_discount = PercentDiscount(10)
fixed_discount = FixedAmountDiscount(10)

user.add_to_cart(digital_product)
print("Total after 10% discount:", user.checkout(percent_discount))
user.add_to_cart(digital_product)
print("Total after $10 discount:", user.checkout(fixed_discount))
