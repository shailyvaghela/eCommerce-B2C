from datetime import datetime
import os
from datetime import datetime, timedelta
import random
import string
import re
import sys 

class Admin:
    def __init__(self):
        self.admin_username = "admin"
        self.admin_password = "admin123"

    def admin_login(self):
        try:
            username = input("Enter Admin Username: ")
            password = input("Enter Admin Password: ")
        except Exception as e:
            print("An error occurred while getting input:", e)
            return False

        try:
            if username == self.admin_username and password == self.admin_password:
                print("Admin login successful.")
                return True
            else:
                print(self.admin_username)
                print("Invalid username or password.")
                return False
        except Exception as e:
            print("An error occurred during login validation:", e)
            return False

    def admin_menu(self):
        while True:
            print("\n")
            print_line_2()
            print("Admin Menu:")
            print_line_2()
            print("1. Add Product")
            print("2. Delete Product")
            print("3. Update Stock")
            print("4. Logout")
            print_line_2()

            try:
                choice = input("Enter your choice: ")
            except Exception as e:
                print("An error occurred while getting input:", e)
                continue

            try:
                if choice == '1':
                    category = input("Enter product category: ")
                    if self.check_category_exists(category):
                        product_file = os.path.join(
                            "Categories", f"{category}.txt")
                        self.add_product(product_file)
                    else:
                        print("Category not found.")
                elif choice == '2':
                    self.delete_product()
                elif choice == '3':
                    self.update_stock()
                elif choice == '4':
                    print("Logging out...")
                    sys.exit(1)
                else:
                    print("Invalid choice.")
            except Exception as e:
                print("An error occurred:", e)

    def add_product(self, product_file):
        try:
            if os.path.exists(product_file) and os.path.getsize(product_file) > 0:
                with open(product_file, "r") as file:
                    lines = file.readlines()
                    last_line = lines[-1].strip()
                    if last_line.startswith("{") and last_line.endswith("}"):
                        try:
                            last_product = eval(last_line)  # Evaluate the last line as a dictionary
                            last_product_id = last_product.get("id", 0)  # Get the ID of the last product
                            product_id = last_product_id + 1  # Increment the ID for the new product
                        except Exception as e:
                            print("Error reading the ID of the last product:", e)
                            return
                    else:
                        print("Error: Invalid format for the last product in the file.")
                        return
            else:
                # If the file is empty or doesn't exist, start from ID 1
                product_id = 1

            while True:
                try:
                    product_name = input("Enter product name: ")
                    product_price = int(input("Enter product price: "))
                    product_stock = int(input("Enter product stock: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            product_info = f"\n{{'id': {product_id}, 'name': '{product_name}', 'price': {product_price}, 'stock': {product_stock}}}"

            with open(product_file, "a") as file:
                file.write(product_info)

            print("Stock added successfully.")
            log_activity(f"Added product '{product_name}' in '{product_file}' Category with Price of Rs. '{product_price}' in '{product_stock}' quantity.")
        except Exception as e:
            print("An error occurred:", e)


    def delete_product(self):
        try:
            category = input("Enter product category: ")
            filename = os.path.join("Categories", f"{category}.txt")

            if os.path.exists(filename):
                with open(filename, "r") as file:
                    products = file.readlines()
                    for i, product in enumerate(products, 1):
                        print(f"{i}. {product.strip()}")

                while True:
                    try:
                        choice = int(input("Enter the number of the product to delete: "))
                        if 1 <= choice <= len(products):
                            
                            product_id = products[choice - 1].split(",")[0].split(":")[1].strip().replace("'", "")
                            del products[choice - 1]
                            with open(filename, "w") as file:
                                file.writelines(products)
                            print("Product deleted successfully.")
                            log_activity(f"Deleted product with ID {product_id} from {filename} Category.")
                            break 
                        else:
                            print("Invalid choice. Please enter a number within the range.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            else:
                print("Category not found.")
        except Exception as e:
            print("An error occurred:", e)

    def update_stock(self):
        try:
            category = input("Enter product category: ")
            filename = os.path.join("Categories", f"{category}.txt")

            if os.path.exists(filename):
                with open(filename, "r") as file:
                    products = file.readlines()
                    for i, product in enumerate(products, 1):
                        print(f"{i}. {product.strip()}")

                while True:
                    try:
                        choice = int(input("Enter the number of the product to update: "))
                        if 1 <= choice <= len(products):
                            
                            product_id = products[choice - 1].split(",")[0].split(":")[1].strip().replace("'", "")
                            try:
                                new_stock = int(input("Enter new stock quantity: "))
                            
                                parts = products[choice - 1].strip().split(",")
                                parts[-1] = f"'Stock': {new_stock}\n"
                                updated_product = ",".join(parts)
                                products[choice - 1] = updated_product
                                with open(filename, "w") as file:
                                    file.writelines(products)
                                print("Stock updated successfully.")
                                log_activity(f"Updated stock for product with ID {product_id} to {new_stock} from {filename} Category.")
                                break
                            except ValueError:
                                print("Invalid input. Please enter a valid integer.")
                        else:
                            print("Invalid choice.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            else:
                print("Category not found.")
        except Exception as e:
            print("An error occurred:", e)

    def check_category_exists(self, category):
        try:
            categories_folder = "Categories"
            if os.path.exists(os.path.join(categories_folder, f"{category}.txt")):
                return True
            return False
        except Exception as e:
            print("An error occurred:", e)
            return False

def log_activity(activity):
    try:
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        with open("admin_activity_log.txt", "a") as log_file:
            log_file.write(f"{formatted_time}: {activity}\n")
        print("Activity logged successfully.")
    except Exception as e:
        print("An error occurred while logging activity:", e)


class Register:
    userDetails = []
    is_member = False
    membership_level = ''

    def __init__(self, userName, password, security_question=None, security_answer=None, mobile=None, email=None, age=None, is_member=False):
        self.userName = userName
        self.password = password
        self.security_question = security_question
        self.security_answer = security_answer
        self.mobile = mobile
        self.email = email
        self.age = age
        self.is_member = is_member
        self.member_file_path = "registeredUsers\\members.txt"

    def generate_membership_id(self):
        # Generate a random alphanumeric ID of length 6
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def registerUser(self, userName, password, mobile, email, age, is_member):
        try:
            print("Registration Successful")

            # Randomly select a security question from a list
            security_questions = [
                "What is your mother's maiden name?",
                "What city were you born in?",
                "What is the name of your first pet?",
                "What is your favorite movie?",
                "What is the name of your favorite teacher?"
            ]
            security_question = random.choice(security_questions)

            security_answer = input(f"Security Question: {security_question}\nEnter your answer: ")

            while True:
                is_member = input("Do you want to become a member? (yes/no): ").lower()
                if is_member == "yes":
                    while True:
                        
                        print("Choose a membership plan:")
                        print_line()
                        print('''\nPlan 1: Normal Plan (Rs. 500)
    Price: Rs. 500
    Duration: 3 months
    Discount: 10%
    Benefits:
    Access to member-exclusive deals and discounts.
    Priority customer support.
    Special promotions and offers tailored for members.
    Ability to accumulate reward points on purchases.
    ------------------------------------------------------                         
Plan 2: Average Plan (Rs. 1000)
    Price: Rs. 1000
    Duration: 6 months
    Discount: 15%
    Benefits:
    All benefits of the Normal Plan.
    Higher discount rate of 15% on all purchases.
    Extended membership duration of 6 months.
    Access to premium customer support services.
    ------------------------------------------------------
Plan 3: Premium Plan (Rs. 1500)
    Price: Rs. 1500
    Duration: 1 year
    Discount: 20%
    Benefits:
    All benefits of the Average Plan.
    Highest discount rate of 20% on all purchases.
    Extended membership duration of 1 year.
    Exclusive early access to new products and services.
    Personalized recommendations based on purchase history.
    Priority access to limited-stock items.
                              
    ''')
                        plan_choice = input("Enter the number corresponding to your chosen plan: ")
                        plan_amount = 0
                        if plan_choice == '1':
                            plan_amount = 500
                        elif plan_choice == '2':
                            plan_amount = 1000
                        elif plan_choice == '3':
                            plan_amount = 1500
                        else:
                            print("Invalid choice. Please choose a valid plan.")
                            continue

                        if plan_choice == '1':
                            membership_file = "registeredUsers/members_500.txt" 
                            membership_duration = 90  # 3 months
                        elif plan_choice == '2':
                            membership_file = "registeredUsers/members_1000.txt"
                            membership_duration = 180  # 6 months
                        elif plan_choice == '3':
                            membership_file = "registeredUsers/members_1500.txt"
                            membership_duration = 365  # 1 year

                        payment = input(f"To become a member, you need to pay Rs. {plan_amount}. Proceed with payment? (yes/no): ").lower()
                        if payment == "yes":
                            while True:
                                try:
                                    print_line()
                                    print("Payment method:")
                                    print_line()
                                    print("1. Credit card")
                                    print("2. Debit card")
                                    print("3. Change Plan")

                                    payment_method = int(input("\nSelect payment method: "))

                                    if payment_method == 1 or payment_method == 2:
                                        card_number = input("Enter 12 digit card number: ")
                                        if validate_card_number(card_number):
                                            cvv = input("Enter 3 digit CVV: ")
                                            if validate_cvv(cvv):
                                                print("Payment Successful!")

                                                is_member = True

                                                start_date = datetime.now()
                                                end_date = start_date + \
                                                    timedelta(days=membership_duration)

                                                membership_id = self.generate_membership_id()

                                                member_data_str = f"ID: {membership_id}, Start Date: {start_date.strftime('%Y-%m-%d')}, End Date: {end_date.strftime('%Y-%m-%d')}, Username: {userName}"

                                                with open(f"registeredUsers/members_{plan_amount}.txt", "a") as member_amount_file:
                                                    member_amount_file.write(
                                                        member_data_str + "\n")

                                                bill_filename = f"{userName}_membership_bill.txt"
                                                bill_folder = userName  
                                                bill_filepath = os.path.join(
                                                    bill_folder, bill_filename)

                                                if not os.path.exists(bill_folder):
                                                    os.makedirs(bill_folder)

                                                with open(bill_filepath, "w") as bill_file:
                                                    bill_file.write(
                                                        "=====================================\n")
                                                    bill_file.write(
                                                        "           MEMBERSHIP BILL\n")
                                                    bill_file.write(
                                                        "=====================================\n")
                                                    bill_file.write(
                                                        f"Membership Plan: {plan_choice}\n")
                                                    bill_file.write(f"Plan {plan_choice}: {'Normal' if plan_choice == '1' else ('Average' if plan_choice == '2' else 'Premium')} Plan (Rs. {plan_amount})\n")
                                                    bill_file.write(
                                                        f"Price: Rs. {plan_amount}\n")
                                                    bill_file.write(
                                                        f"Duration: {membership_duration} days\n")
                                                    bill_file.write(f"Discount: {'10%' if plan_choice == '1' else ('15%' if plan_choice == '2' else '20%')}\n")
                                                    bill_file.write("Benefits:\n")
                                                    if plan_choice == '1':
                                                        bill_file.write(
                                                            "- Access to member-exclusive deals and discounts.\n")
                                                        bill_file.write(
                                                            "- Priority customer support.\n")
                                                        bill_file.write(
                                                            "- Special promotions and offers tailored for members.\n")
                                                        bill_file.write(
                                                            "- Ability to accumulate reward points on purchases.\n")
                                                    elif plan_choice == '2':
                                                        bill_file.write(
                                                            "- All benefits of the Normal Plan.\n")
                                                        bill_file.write(
                                                            "- Higher discount rate of 15% on all purchases.\n")
                                                        bill_file.write(
                                                            "- Extended membership duration of 6 months.\n")
                                                        bill_file.write(
                                                            "- Access to premium customer support services.\n")
                                                    elif plan_choice == '3':
                                                        bill_file.write(
                                                            "- All benefits of the Average Plan.\n")
                                                        bill_file.write(
                                                            "- Highest discount rate of 20% on all purchases.\n")
                                                        bill_file.write(
                                                            "- Extended membership duration of 1 year.\n")
                                                        bill_file.write(
                                                            "- Exclusive early access to new products and services.\n")
                                                        bill_file.write(
                                                            "- Personalized recommendations based on purchase history.\n")
                                                        bill_file.write(
                                                            "- Priority access to limited-stock items.\n")
                                                    bill_file.write(
                                                        f"Start Date: {start_date.strftime('%Y-%m-%d')}\n")
                                                    bill_file.write(
                                                        f"End Date: {end_date.strftime('%Y-%m-%d')}\n")
                                                    bill_file.write(f"Membership ID: {membership_id}\n")
                                                    bill_file.write(f"Payment Method: {'Credit Card' if payment_method == 1 else 'Debit Card'}\n")
                                                    bill_file.write(
                                                        f"Card Number: {card_number}\n")
                                                    bill_file.write(f"CVV: {cvv}\n")
                                                    bill_file.write(
                                                        "=====================================\n")

                                                print("Bill generated successfully!")
                                                user_details = {
                                                    'username': userName,
                                                    'password': password,
                                                    'security_question': security_question,
                                                    'security_answer': security_answer,
                                                    'mobile': mobile,
                                                    'email': email,
                                                    'age': age,
                                                    'isMember': is_member
                                                }
                                                self.userDetails.append(user_details)

                                                with open("registeredUsers\\userDetails.txt", "a") as user_details_file:
                                                    user_details_file.write(
                                                        str(user_details) + "\n")
                                                return
                                            else:
                                                print(
                                                    "Invalid CVV. Please enter a valid CVV.")
                                        else:
                                            print(
                                                "Invalid card number. Please enter a valid card number.")
                                    elif payment_method == 3:
                                        break
                                    else:
                                        print("Invalid payment method. Please choose a valid payment method.")
                                except ValueError:
                                    print("Invalid input. Please enter a valid option.")
                        else:
                            print("Membership not activated.")
                            is_member = False
                            break
                elif is_member == "no":
                    is_member = False
                    break
                else:
                    print("Invalid choice. Please enter 'yes' or 'no'.")
        except Exception as e:
            print("An error occurred while registering user:", e)

def generate_bill(user, purchased_items, total_amount, payment_method, card_number):
    try:
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        bill_file_name = f"{user}\\{user}_BILL_{formatted_time}.txt"

        with open(bill_file_name, "w") as bill_file:
            bill_file.write("\n")
            bill_file.write("**************************************\n")
            bill_file.write("              Invoice                \n")
            bill_file.write("**************************************\n")
            bill_file.write(f"User: {user}\n")
            bill_file.write(f"Date: {formatted_time}\n")
            bill_file.write("--------------------------------------\n")
            bill_file.write("Product Details:\n")
            for item in purchased_items:
                bill_file.write(f"- {item}\n")
            bill_file.write("--------------------------------------\n")
            bill_file.write(f"Total Amount: Rs.{total_amount}\n")
            bill_file.write(f"Payment Method: {payment_method}\n")
            if payment_method in ['Credit Card', 'Debit Card']:
                bill_file.write(f"Card Number: {card_number}\n")
            bill_file.write("**************************************\n")

        print("Bill generated successfully.")
    except Exception as e:
        print("An error occurred while generating bill:", e)

def show_my_bills(user):
    try:
        user_bills = [bill for bill in os.listdir(user) if (bill.startswith(
            f"{user}_BILL_") or bill.startswith(f"{user}_membership_bill"))]
        if user_bills:
            user_bills.sort()
            print("Your bills:")
            for bill_file in user_bills:
                with open(os.path.join(user, bill_file), "r") as file:
                    print(f"\n{bill_file}:")
                    print(file.read())
        else:
            print("You have no bills yet.")
    except Exception as e:
        print("An error occurred while showing bills:", e)

def view_profile(user_name):
    try:
        with open("registeredUsers\\userDetails.txt", "r") as user_details_file:
            for line in user_details_file:
                user_details = eval(line)
                if user_details['username'] == user_name:
                    print("User Profile:")
                    print(f"Username: {user_details['username']}")
                    print(f"Password: {user_details['password']}")
                    print(f"Mobile: {user_details.get('mobile')}")
                    print(f"Email: {user_details.get('email')}")
                    print(f"Age: {user_details.get('age')}")
                    return
            print("User not found.")
    except FileNotFoundError:
        try:
            with open("..\\registeredUsers\\userDetails.txt", "r") as user_details_file:
                for line in user_details_file:
                    user_details = eval(line)
                    if user_details['username'] == user_name:
                        print("User Profile:")
                        print(f"Username: {user_details['username']}")
                        print(f"Password: {user_details['password']}")
                        print(f"Mobile: {user_details.get('mobile')}")
                        print(f"Email: {user_details.get('email')}")
                        print(f"Age: {user_details.get('age')}")
                        return
                print("User not found.")
        except Exception as e:
            print("An error occurred while viewing profile:", e)

def update_profile(user_name):
    updated_details = []
    
    try:
        with open("registeredUsers\\userDetails.txt", "r") as user_details_file:
            lines = user_details_file.readlines()
            found = False
            for line in lines:
                user_details = eval(line)
                if user_details['username'] == user_name:
                    found = True
                    print("Update Profile:")
                    print_line()
                    print("1. Change Password")
                    print("2. Update Mobile Number")
                    print("3. Update Email Address")
                    print("4. Update Age")
                    print("5. Back to Main Menu")
                    choice = input("Enter your choice: ")
                    if choice == '1':
                        security_question = user_details.get(
                            'security_question', '')
                        security_answer = user_details.get('security_answer', '')

                        if security_question:
                            print(f"Security Question: {security_question}")
                            answer = input(
                                "Enter your answer to the security question: ")

                            if answer == security_answer:
                                new_password = input("Enter new password: ")

                                new_password = validatePassword(new_password)
                                if new_password:
                                    user_details['password'] = new_password
                                    print("Password updated successfully!")
                                else:
                                    print(
                                        "Password does not meet the requirements. Password update failed.")
                            else:
                                print(
                                    "Incorrect answer to the security question. Password update failed.")
                        else:
                            print("Security question not set. Please contact support.")
                    elif choice == '2':
                        while True:
                            new_mobile = input("Enter Mobile Number: ")
                            if len(new_mobile) == 10 and new_mobile.isdigit() and new_mobile[0] in ['7', '8', '9']:
                                break
                            else:
                                print("Invalid mobile number. Mobile number should be 10 digits and start with 7, 8, or 9.")
                        user_details['mobile'] = new_mobile
                        print("Mobile number updated successfully!")
                    elif choice == '3':
                        new_email = input("Enter new email address: ")
                        new_email=validateEmail(new_email)
                        user_details['email'] = new_email
                        print("Email address updated successfully!")
                    elif choice == '4':
                        new_age = input("Enter new age: ")
                        if new_age.isdigit() and int(new_age) > 0:
                            user_details['age'] = int(new_age)
                            print("Age updated successfully!")
                            break
                        else:
                            print("Invalid input. Age should be a positive integer.")
                    elif choice == '5':
                        print("Returning to main menu.")
                    else:
                        print("Invalid choice. Please enter a valid option.")
                updated_details.append(user_details)
    except FileNotFoundError:
        with open("..\\registeredUsers\\userDetails.txt", "r") as user_details_file:
            lines = user_details_file.readlines()
            found = False
            for line in lines:
                user_details = eval(line)
                if user_details['username'] == user_name:
                    found = True
                    print_line()
                    print("Update Profile:")
                    print_line()
                    print("1. Change Password")
                    print("2. Update Mobile Number")
                    print("3. Update Email Address")
                    print("4. Update Age")
                    print("5. Back to Main Menu")
                    choice = input("\nEnter your choice: ")
                    if choice == '1':
                        security_question = user_details.get(
                            'security_question', '')
                        security_answer = user_details.get('security_answer', '')

                        if security_question:
                            print(f"Security Question: {security_question}")
                            answer = input(
                                "Enter your answer to the security question: ")

                            if answer == security_answer:
                                new_password = input("Enter new password: ")

                                new_password = validatePassword(new_password)
                                if new_password:
                                    user_details['password'] = new_password
                                    print("Password updated successfully!")
                                else:
                                    print(
                                        "Password does not meet the requirements. Password update failed.")
                            else:
                                print(
                                    "Incorrect answer to the security question. Password update failed.")
                        else:
                            print("Security question not set. Please contact support.")
                    elif choice == '2':
                        while True:
                            new_mobile = input("Enter Mobile Number: ")
                            if len(new_mobile) == 10 and new_mobile.isdigit() and new_mobile[0] in ['7', '8', '9']:
                                break
                            else:
                                print("Invalid mobile number. Mobile number should be 10 digits and start with 7, 8, or 9.")
                        user_details['mobile'] = new_mobile
                        print("Mobile number updated successfully!")
                    elif choice == '3':
                        new_email = input("Enter new email address: ")
                        new_email=validateEmail(new_email)
                        user_details['email'] = new_email
                        print("Email address updated successfully!")
                    elif choice == '4':
                        new_age = input("Enter new age: ")
                        user_details['age'] = new_age
                        print("Age updated successfully!")
                    elif choice == '5':
                        print("Returning to main menu.")
                    else:
                        print("Invalid choice. Please enter a valid option.")
                updated_details.append(user_details)
    if found:
        try:
            with open("registeredUsers\\userDetails.txt", "w") as user_details_file:
                for line in updated_details:
                    user_details_file.write(str(line) + "\n")
        except FileNotFoundError:
            with open("..\\registeredUsers\\userDetails.txt", "w") as user_details_file:
                for line in updated_details:
                    user_details_file.write(str(line) + "\n")
    else:
        print("User not found.")


def show_cart(user):
    cart_file_path = os.path.join(user, f"{user}_cart.txt")
    print("Your Cart:")
    try:
        with open(cart_file_path, "r") as cart_file:
            cart_items = cart_file.readlines()
            if cart_items:
                for item in cart_items:
                    print(item.strip())
            else:
                print("Your cart is empty.")
    except FileNotFoundError:
        with open("..\\"+cart_file_path, "r") as cart_file:
            cart_items = cart_file.readlines()
            if cart_items:
                for item in cart_items:
                    print(item.strip())
            else:
                print("Your cart is empty.")

    while True:
        print_line()
        print("Cart Menu:")
        print_line()
        print("1. Add Product")
        print("2. Delete Product")
        print("3. Shop All")
        print("4. Buy Particular Product")
        print("5. Back to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            print("Redirecting to categories options...")
            menu(user)
        elif choice == '2':
            delete_product(user)
            show_cart(user)
        elif choice == '3':
            shop_all(user)
            show_cart(user)  
        elif choice == '4':
            buy_particular_product(user)
            show_cart(user)
        elif choice == '5':
            print("Returning to main menu.")
            menu(user)
            break
        else:
            print("Invalid choice. Please enter a valid option.")


def delete_product(user):
    cart_file_path = f"{user}\\{user}_cart.txt"
    try:
        with open(cart_file_path, "r") as cart_file:
            cart_items = cart_file.readlines()
            if cart_items:
                id_to_delete = input(
                    "Enter the 6-digit ID of the product you want to delete: ")
                with open(cart_file_path, "w") as cart_file:
                    deleted = False
                    for item in cart_items:
                        if f"Id: {id_to_delete}" in item:
                            print("Product deleted from cart.")
                            deleted = True
                        else:
                            cart_file.write(item)
                    if not deleted:
                        print("Product with specified ID not found in cart.")
            else:
                print("Your cart is empty.")
    except FileNotFoundError:
        print("Your cart is empty.")


def shop_all(user):
    cart_file_path = os.path.join(user, f"{user}_cart.txt")
    membership_level = Register.membership_level
    try:
        with open(cart_file_path, "r") as cart_file:
            cart_items = cart_file.readlines()
            total_price = 0
            purchased_items = []
            if cart_items:
                for item in cart_items:
                    price_index = item.find("Total Price: Rs.")
                    total_price += int(item[price_index +
                                       len("Total Price: Rs."):].strip())
                   
                    purchased_items.append(item.strip())
                print(f"Total price of all items in your cart: Rs.{total_price}")
                choice = input(
                    "Do you want to buy all items? (yes/no): ").lower()
                if choice == 'yes':
                   
                    print(f"Total Price: Rs.{total_price}")
                  
                    if membership_level == '500':
                        print("You have recieved 10% Discount as Normal Plan benifit")
                        total_price *= 0.9  # Apply 10% discount
                    elif membership_level == '1000':
                        print(
                            "You have recieved 15% Discount as Average Plan benifit")
                        total_price *= 0.85  # Apply 15% discount
                    elif membership_level == '1500':
                        print(
                            "You have recieved 20% Discount as Premium Plan benifit")
                        total_price *= 0.8  # Apply 20% discount
                    print(f"Total Price after discount: Rs.{total_price}")
                    while True:
                        print("Payment method:")
                        print("1. Credit card")
                        print("2. Debit card")

                        payment_method = int(input("Select payment method: "))

                        if payment_method == 1 or payment_method == 2:
                            card_number = input("Enter 12 digit card number: ")
                            if validate_card_number(card_number):
                                cvv = input("Enter 3 digit CVV: ")
                                if validate_cvv(cvv):
                                    print("Payment successful! All items purchased.")
                                    if payment_method == 1:
                                        pay_method = "Credit Card"
                                    elif payment_method == 2:
                                        pay_method = "Debit Card"
                                   
                                    generate_bill(user, purchased_items, total_price, pay_method, card_number)
                                   
                                    with open(cart_file_path, "w") as cart_file:
                                        pass
                                    break
                                else:
                                    print("Invalid CVV. Payment failed.")
                            else:
                                print("Invalid card number. Payment failed.")
                        else:
                            print("Invalid payment method. Payment failed.")
                elif choice == 'no':
                    print("Purchase canceled.")
                else:
                    print("Invalid choice.")
            else:
                print("Your cart is empty.")
    except FileNotFoundError:
        print("Your cart is empty.")


def buy_particular_product(user):
    cart_file_path = os.path.join(user, f"{user}_cart.txt")
    membership_level = Register.membership_level
    try:
        with open(cart_file_path, "r") as cart_file:
            cart_items = cart_file.readlines()
            purchased_items = []
            if cart_items:
                id_to_buy = input(
                    "Enter the 6-digit ID of the product you want to buy: ")
                for item in cart_items:
                    if f"Id: {id_to_buy}" in item:
                        print("Product found in cart.")
                        print(item.strip())
                        price_index = item.find("Total Price: Rs.")
                        total_price = int(
                            item[price_index + len("Total Price: Rs."):].strip())
                        confirm = input("Confirm purchase? (yes/no): ").lower()
                        if confirm == 'yes':
                            if membership_level == '500':
                                print(
                                    "You have recieved 10% Discount as Normal Plan benifit")
                                total_price *= 0.9  # Apply 10% discount
                            elif membership_level == '1000':
                                print(
                                    "You have recieved 15% Discount as Average Plan benifit")
                                total_price *= 0.85  # Apply 15% discount
                            elif membership_level == '1500':
                                print(
                                    "You have recieved 20% Discount as Premium Plan benifit")
                                total_price *= 0.8  # Apply 20% discount
                            print(f"Total Price after discount: Rs.{total_price}")
                            while True:
                                try:
                                    print_line()
                                    print("Payment method:")
                                    print_line()
                                    print("1. Credit card")
                                    print("2. Debit card")

                                    payment_method = int(
                                        input("\nSelect payment method: "))

                                    if payment_method == 1 or payment_method == 2:
                                        card_number = input(
                                            "Enter 12 digit card number: ")
                                        if validate_card_number(card_number):
                                            cvv = input("Enter 3 digit CVV: ")
                                            if validate_cvv(cvv):
                                                if payment_method == 1:
                                                    pay_method = "Credit Card"
                                                elif payment_method == 2:
                                                    pay_method = "Debit Card"
                                                print(
                                                    "Payment successful! Product purchased.")
                                             
                                                price_index = item.find(
                                                    "Total Price: Rs.")
                                                purchased_items.append(
                                                    item.strip())
                                                generate_bill(user, purchased_items, int(
                                                    item[price_index + len("Total Price: Rs."):].strip()), pay_method, card_number)
                                               
                                                with open(cart_file_path, "w") as cart_file:
                                                    for line in cart_items:
                                                        if f"Id: {id_to_buy}" not in line:
                                                            cart_file.write(line)
                                                break
                                            else:
                                                print(
                                                    "Invalid CVV. Payment failed.")
                                        else:
                                            print(
                                                "Invalid card number. Payment failed.")
                                    else:
                                        print(
                                            "Invalid payment method. Payment failed.")
                                except ValueError:
                                    print("Invalid input. Please enter a valid option.")
                        elif confirm == 'no':
                            print("Purchase canceled.")
                        else:
                            print("Invalid choice.")
                        break
                else:
                    print("Product with specified ID not found in cart.")
            else:
                print("Your cart is empty.")
    except FileNotFoundError:
        print("Your cart is empty.")

def purchase_product(product, quantity, user, membership_level):
    try:
        print_line()
        print("You chose to purchase this product.")
        print(f"Product: {product['name']}")
        print(f"Quantity: {quantity}")
        total_price = product['price'] * quantity
        print(f"Total Price: Rs.{total_price}")
       
        if membership_level == '500':
            print("You have received 10% Discount as Normal Plan benefit")
            total_price *= 0.9  # Apply 10% discount
        elif membership_level == '1000':
            print("You have received 15% Discount as Average Plan benefit")
            total_price *= 0.85  # Apply 15% discount
        elif membership_level == '1500':
            print("You have received 20% Discount as Premium Plan benefit")
            total_price *= 0.8  # Apply 20% discount
        print(f"Total Price after discount: Rs.{total_price}")
        print_line_2()
        confirm = input("Confirm purchase? (yes/no): ").lower()
        if confirm == 'yes':
            while True:
                try:
                    print_line()
                    print("Payment method:")
                    print_line()
                    print("1. Credit card")
                    print("2. Debit card")

                    payment_method = int(input("\nSelect payment method: "))

                    if payment_method == 1 or payment_method == 2:
                        card_number = input("Enter 12 digit card number: ")
                        if validate_card_number(card_number):
                            cvv = input("Enter 3 digit CVV: ")
                            if validate_cvv(cvv):
                                if payment_method == 1:
                                    pay_method = "Credit Card"
                                elif payment_method == 2:
                                    pay_method = "Debit Card"
                                print_line_2()
                                print("Payment Successful. Product purchased.")
                                purchased_items = [f"Product: {product['name']}\nQuantity: {quantity}\nTotal Price: Rs.{total_price}"]
                                generate_bill(user, purchased_items,
                                            total_price, pay_method, card_number)
                                break
                            else:
                                print("Invalid CVV. Payment failed.")
                        else:
                            print("Invalid card number. Payment failed.")
                    else:
                        print("Invalid payment method. Payment failed.")
                except ValueError:
                    print("Invalid input. Please enter a valid option.")
        else:
            print("Purchase canceled.")
    except Exception as e:
        print("An error occurred during purchase:", e)

def validate_card_number(card_number):
    try:
        if len(card_number) == 12 and card_number.isdigit():
            return True
        else:
            return False
    except Exception as e:
        print("An error occurred while validating card number:", e)
        return False

def validate_cvv(cvv):
    try:
        if len(cvv) == 3 and cvv.isdigit():
            return True
        else:
            return False
    except Exception as e:
        print("An error occurred while validating CVV:", e)
        return False



def print_products(file_path, user):
    category_folder = "Categories"

    full_file_path = os.path.join(category_folder, file_path)

    membership_level = Register.membership_level
    while True:
        products = []
        try:
            with open(full_file_path, 'r+') as file:
                for line in file:
                    product_info = line.strip().split(",")
                    try:
                        product_id = int(product_info[0].split(":")[1].strip())
                        product_name = product_info[1].split(
                            ":")[1].strip().strip('"')
                        product_price = int(
                            product_info[2].split(":")[1].strip())
                        product_stock = int(product_info[3].split(":")[
                                            1].strip().strip('}'))
                        product = {'id': product_id, 'name': product_name,
                                   'price': product_price, 'stock': product_stock}
                        products.append(product)
                        print(f"ID: {product_id}, Name: {product_name}, Price: Rs.{product_price}, Stock: {product_stock}")
                        print_line_2()
                    except (IndexError, ValueError) as e:
                        print(f"Error parsing product info: {e}")

                while True:
                    try:
                        product_id = int(
                            input("Enter the ID of the product you want to purchase (0 to exit): "))
                        if product_id == 0:
                            return 

                        product = next(
                            (p for p in products if p['id'] == product_id), None)
                        if product:
                            quantity = int(
                                input(f"Enter the quantity of '{product['name']}': "))
                            if quantity <= product['stock']:
                                add_to_cart = input(
                                    "Do you want to add this product to your cart? (yes/no): ").lower()
                                if add_to_cart == 'yes':
                                    
                                    code = ''.join(random.choice(string.digits) if i % 2 == 0 else random.choice(
                                        string.ascii_letters) for i in range(6))
                                    total_price = product['price'] * quantity
                                    
                                    try:
                                        with open(os.path.join(user, f"{user}_cart.txt"), "a") as cart_file:
                                            cart_file.write(f"Id: {code}, Name: {product['name']}, Qty: {quantity}, Total Price: Rs.{total_price}\n")
                                        print("Product added to cart.")
                                    except (FileNotFoundError):
                                        with open(os.path.join("..//"+user, f"{user}_cart.txt"), "a") as cart_file:
                                            cart_file.write(f"Id: {code}, Name: {product['name']}, Qty: {quantity}, Total Price: Rs.{total_price}\n")
                                        print("Product added to cart.")
                                elif add_to_cart == 'no':
                                    print("Product not added to cart.")
                                else:
                                    print(
                                        "Invalid option. Please enter 'yes' or 'no'.")
                                product['stock'] -= quantity
                                file.seek(0)
                                for p in products:
                                    file.write(
                                        f"{{'id': {p['id']}, 'name': {p['name']}, 'price': {p['price']}, 'stock': {p['stock']}}}\n")
                                
                                while True:
                                    print_line()
                                    print("1. Purchase this product")
                                    print("2. Show my cart")
                                    print("3. Continue shopping")
                                    print("4. Go back to categories")

                                    cart_choice = input("\nEnter your choice: ")
                                    if cart_choice == '1':
                                        purchase_product(
                                            product, quantity, user, membership_level)
                                        break
                                    elif cart_choice == '2':
                                        show_cart(user)
                                        break
                                    elif cart_choice == '3':
                                        break
                                    elif cart_choice == '4':
                                        return
                                    else:
                                        print(
                                            "Invalid choice. Please enter a valid option.")
                            else:
                                print()
                                print(f"Sorry, '{product['name']}' is out of stock. Available stock: {product['stock']}")
                        else:
                            print("Invalid product ID. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                    choice = input(
                        "Do you want to continue shopping in the same category? (yes/no): ").lower()
                    if choice == 'yes':
                        continue
                    elif choice != 'yes':
                        return
        except FileNotFoundError:
            full_file_path = f"..\\{category_folder}\\{file_path}"
            with open(full_file_path, 'r+') as file:
                for line in file:
                    product_info = line.strip().split(",")
                    try:
                        product_id = int(product_info[0].split(":")[1].strip())
                        product_name = product_info[1].split(
                            ":")[1].strip().strip('"')
                        product_price = int(
                            product_info[2].split(":")[1].strip())
                        product_stock = int(product_info[3].split(":")[
                                            1].strip().strip('}'))
                        product = {'id': product_id, 'name': product_name,
                                   'price': product_price, 'stock': product_stock}
                        products.append(product)
                        print(f"ID: {product_id}, Name: {product_name}, Price: Rs.{product_price}, Stock: {product_stock}")
                    except (IndexError, ValueError) as e:
                        print(f"Error parsing product info: {e}")

                while True:
                    try:
                        product_id = int(
                            input("Enter the ID of the product you want to purchase (0 to exit): "))
                        if product_id == 0:
                            return 

                        product = next(
                            (p for p in products if p['id'] == product_id), None)
                        if product:
                            quantity = int(
                                input(f"Enter the quantity of '{product['name']}': "))
                            if quantity <= product['stock']:
                                add_to_cart = input(
                                    "Do you want to add this product to your cart? (yes/no): ").lower()
                                if add_to_cart == 'yes':
                                    
                                    code = ''.join(random.choice(string.digits) if i % 2 == 0 else random.choice(
                                        string.ascii_letters) for i in range(6))
                                    total_price = product['price'] * quantity
                                    
                                    try:
                                        with open(os.path.join(user, f"{user}_cart.txt"), "a") as cart_file:
                                            cart_file.write(f"Id: {code}, Name: {product['name']}, Qty: {quantity}, Total Price: Rs.{total_price}\n")
                                        print("Product added to cart.")
                                    except (FileNotFoundError):
                                        with open(os.path.join("..//"+user, f"{user}_cart.txt"), "a") as cart_file:
                                            cart_file.write(f"Id: {code}, Name: {product['name']}, Qty: {quantity}, Total Price: Rs.{total_price}\n")
                                        print("Product added to cart.")
                                elif add_to_cart == 'no':
                                    print("Product not added to cart.")
                                else:
                                    print(
                                        "Invalid option. Please enter 'yes' or 'no'.")
                                product['stock'] -= quantity
                               
                                file.seek(0)
                                
                                for p in products:
                                    file.write(
                                        f"{{'id': {p['id']}, 'name': {p['name']}, 'price': {p['price']}, 'stock': {p['stock']}}}\n")

                                while True:
                                    print_line()
                                    print("1. Purchase this product")
                                    print("2. Show my cart")
                                    print("3. Continue shopping")
                                    print("4. Go back to categories")

                                    cart_choice = input("\nEnter your choice: ")
                                    if cart_choice == '1':
                                        purchase_product(
                                            product, quantity, user, membership_level)
                                        break
                                    elif cart_choice == '2':
                                        show_cart(user)
                                        break
                                    elif cart_choice == '3':
                                        break
                                    elif cart_choice == '4':
                                        return
                                    else:
                                        print(
                                            "Invalid choice. Please enter a valid option.")
                            else:
                                print(f"Sorry, '{product['name']}' is out of stock. Available stock: {product['stock']}")
                        else:
                            print("Invalid product ID. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                    choice = input(
                        "Do you want to continue shopping in the same category? (yes/no): ").lower()
                    if choice == 'yes':
                        continue
                    elif choice != 'yes':
                        return


def show_my_plan(user):
    membership_duration = None
    current_date = datetime.now()
    remaining_days = None
    membership_level=None
    membership_levels = ['registeredUsers//members_500.txt',
                         'registeredUsers//members_1000.txt', 'registeredUsers//members_1500.txt']

    for level_file in membership_levels:
        try:
            with open(level_file, 'r') as file:
                for line in file:
                    membership_info = line.strip().split(", ")
                    start_date_str = membership_info[1].split(": ")[1]
                    end_date_str = membership_info[2].split(": ")[1]
                    username_str = membership_info[3].split(": ")[1]

                    if username_str == user:
                        start_date = datetime.strptime(
                            start_date_str, "%Y-%m-%d")
                        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                        if start_date <= current_date <= end_date:
                            if level_file.endswith('members_500.txt'):
                                membership_level = '500'
                                membership_duration = 90  # 3 months
                            elif level_file.endswith('members_1000.txt'):
                                membership_level = '1000'
                                membership_duration = 180  # 6 months
                            elif level_file.endswith('members_1500.txt'):
                                membership_level = '1500'
                                membership_duration = 365  # 1 year

                            remaining_days = (end_date - current_date).days
                            break 
                if membership_level:
                    break 
        except FileNotFoundError:
            with open("..\\"+level_file, 'r') as file:
                for line in file:
                    membership_info = line.strip().split(", ")
                    start_date_str = membership_info[1].split(": ")[1]
                    end_date_str = membership_info[2].split(": ")[1]
                    username_str = membership_info[3].split(": ")[1]

                    if username_str == user:
                        start_date = datetime.strptime(
                            start_date_str, "%Y-%m-%d")
                        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                        if start_date <= current_date <= end_date:
                            if level_file.endswith('members_500.txt'):
                                membership_level = '500'
                                membership_duration = 90  # 3 months
                            elif level_file.endswith('members_1000.txt'):
                                membership_level = '1000'
                                membership_duration = 180  # 6 months
                            elif level_file.endswith('members_1500.txt'):
                                membership_level = '1500'
                                membership_duration = 365  # 1 year

                            remaining_days = (end_date - current_date).days
                            break  
                if membership_level: 
                    break  
    if membership_level:
        print(f"You are currently subscribed to the {membership_level} membership plan.")
        print("Benefits:")
        if membership_level == '500':
            print_line_2()
            print("- Access to member-exclusive deals and discounts.")
            print("- Priority customer support.")
            print("- Special promotions and offers tailored for members.")
            print("- Ability to accumulate reward points on purchases.")
        elif membership_level == '1000':
            print_line_2()
            print("- All benefits of the Normal Plan.")
            print("- Higher discount rate of 15% on all purchases.")
            print("- Extended membership duration of 6 months.")
            print("- Access to premium customer support services.")
        elif membership_level == '1500':
            print_line_2()
            print("- All benefits of the Average Plan.")
            print("- Highest discount rate of 20% on all purchases.")
            print("- Extended membership duration of 1 year.")
            print("- Exclusive early access to new products and services.")
            print("- Personalized recommendations based on purchase history.")
            print("- Priority access to limited-stock items.")

        print()
        print(f"Start Date: {start_date.strftime('%Y-%m-%d')}")
        print(f"Expiration Date: {end_date.strftime('%Y-%m-%d')}")
        print(f"Your plan is expiring in {remaining_days} days.")
    else:
        print("You don't have an active membership plan.")
        is_member = input("Do you want to become a member? (yes/no): ").lower()
        if is_member == "yes":
            while True:
               
                print("Choose a membership plan:")
                print('''Plan 1: Normal Plan (Rs. 500)
    Price: Rs. 500
    Duration: 3 months
    Discount: 10%
    Benefits:
    Access to member-exclusive deals and discounts.
    Priority customer support.
    Special promotions and offers tailored for members.
    Ability to accumulate reward points on purchases.
    Plan 2: Average Plan (Rs. 1000)
    Price: Rs. 1000
    Duration: 6 months
    Discount: 15%
    Benefits:
    All benefits of the Normal Plan.
    Higher discount rate of 15% on all purchases.
    Extended membership duration of 6 months.
    Access to premium customer support services.
    Plan 3: Premium Plan (Rs. 1500)
    Price: Rs. 1500
    Duration: 1 year
    Discount: 20%
    Benefits:
    All benefits of the Average Plan.
    Highest discount rate of 20% on all purchases.
    Extended membership duration of 1 year.
    Exclusive early access to new products and services.
    Personalized recommendations based on purchase history.
    Priority access to limited-stock items.
    ''')
                plan_choice = input(
                    "Enter the number corresponding to your chosen plan: ")
                plan_amount = 0
                if plan_choice == '1':
                    plan_amount = 500
                elif plan_choice == '2':
                    plan_amount = 1000
                elif plan_choice == '3':
                    plan_amount = 1500
                else:
                    print("Invalid choice. Please choose a valid plan.")
                    continue

                if plan_choice == '1':
                    membership_file = "registeredUsers/members_500.txt" 
                    membership_duration = 90  # 3 months
                elif plan_choice == '2':
                    membership_file = "registeredUsers/members_1000.txt"
                    membership_duration = 180  # 6 months
                elif plan_choice == '3':
                    membership_file = "registeredUsers/members_1500.txt"
                    membership_duration = 365  # 1 year

                payment = input(f"To become a member, you need to pay Rs. {plan_amount}. Proceed with payment? (yes/no): ").lower()
                if payment == "yes":
                    payment_method = input(
                        "Select payment method (credit_card/debit_card): ").lower()
                    if payment_method in ['credit_card', 'debit_card']:
                        card_number = input("Enter 12-digit card number: ")
                        if len(card_number) == 12 and card_number.isdigit():
                            cvv = input("Enter 3-digit CVV: ")
                            if len(cvv) == 3 and cvv.isdigit():
                                print("Payment successful!")
                                Register.is_member = True

                                start_date = datetime.now()
                                
                                end_date = start_date + \
                                    timedelta(days=membership_duration)

                                membership_id = membership_id = ''.join(
                                    random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))

                                member_data_str = f"ID: {membership_id}, Start Date: {start_date.strftime('%Y-%m-%d')}, End Date: {end_date.strftime('%Y-%m-%d')}, Username: {user}"

                                with open(f"registeredUsers//members_{plan_amount}.txt", "a") as member_amount_file:
                                    member_amount_file.write(
                                        member_data_str + "\n")

                                bill_filename = f"{user}_membership_bill.txt"
                                bill_folder = user 
                                bill_filepath = os.path.join(
                                    bill_folder, bill_filename)

                                with open(bill_filepath, "w") as bill_file:
                                    bill_file.write(
                                        "=====================================\n")
                                    bill_file.write(
                                        "           MEMBERSHIP BILL\n")
                                    bill_file.write(
                                        "=====================================\n")
                                    bill_file.write(
                                        f"Membership Plan: {plan_choice}\n")
                                    bill_file.write(f"Plan {plan_choice}: {'Normal' if plan_choice == '1' else ('Average' if plan_choice == '2' else 'Premium')} Plan (Rs. {plan_amount})\n")
                                    bill_file.write(
                                        f"Price: Rs. {plan_amount}\n")
                                    bill_file.write(
                                        f"Duration: {membership_duration} days\n")
                                    bill_file.write(f"Discount: {'10%' if plan_choice == '1' else ('15%' if plan_choice == '2' else '20%')}\n")
                                    bill_file.write("Benefits:\n")
                                    if plan_choice == '1':
                                        bill_file.write(
                                            "- Access to member-exclusive deals and discounts.\n")
                                        bill_file.write(
                                            "- Priority customer support.\n")
                                        bill_file.write(
                                            "- Special promotions and offers tailored for members.\n")
                                        bill_file.write(
                                            "- Ability to accumulate reward points on purchases.\n")
                                    elif plan_choice == '2':
                                        bill_file.write(
                                            "- All benefits of the Normal Plan.\n")
                                        bill_file.write(
                                            "- Higher discount rate of 15% on all purchases.\n")
                                        bill_file.write(
                                            "- Extended membership duration of 6 months.\n")
                                        bill_file.write(
                                            "- Access to premium customer support services.\n")
                                    elif plan_choice == '3':
                                        bill_file.write(
                                            "- All benefits of the Average Plan.\n")
                                        bill_file.write(
                                            "- Highest discount rate of 20% on all purchases.\n")
                                        bill_file.write(
                                            "- Extended membership duration of 1 year.\n")
                                        bill_file.write(
                                            "- Exclusive early access to new products and services.\n")
                                        bill_file.write(
                                            "- Personalized recommendations based on purchase history.\n")
                                        bill_file.write(
                                            "- Priority access to limited-stock items.\n")
                                    bill_file.write(
                                        f"Start Date: {start_date.strftime('%Y-%m-%d')}\n")
                                    bill_file.write(
                                        f"End Date: {end_date.strftime('%Y-%m-%d')}\n")
                                    bill_file.write(f"Membership ID: { membership_id}\n")
                                    bill_file.write(f"Payment Method: {payment_method}\n")
                                    bill_file.write(
                                        f"Card Number: {card_number}\n")
                                    bill_file.write(f"CVV: {cvv}\n")
                                    bill_file.write(
                                        "=====================================\n")

                                print("Bill generated successfully!")
                                break
                            else:
                                print("Invalid CVV. Please enter a valid CVV.")
                        else:
                            print(
                                "Invalid card number. Please enter a valid card number.")
                    else:
                        print(
                            "Invalid payment method. Please choose a valid payment method.")
                else:
                    print("No problem. You can always purchase a plan later.")
                    is_member = False
                    break

def menu(user):
    try:
        current_time = datetime.now()
        global formatted_time
        formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        if os.path.isdir(user):
            file_cart = open(user+"\\"+user+"_cart.txt", "a+")
        else:
            if os.path.isdir("..\\"+user):
                file_cart = open("..\\"+user+"\\"+user+"_cart.txt", "a+")
            else:
                file_cart = open("..\\"+user+"_cart.txt", "a+")
        global total
        total = 0
        while True:
            print_line_2()
            print("1. Shop Now")
            print("2. Show My Cart")
            print("3. View My Profile")
            print("4. Update My Profile")
            print("5. Show My Bills")
            print("6. Show My Plan")
            print("7. Log Out")

            try:
                choice = int(input("\nEnter your choice: "))
            except ValueError:
                print("Invalid input. Please enter a valid option.")
                continue

            if choice == 1:
                view_categories(user)
                continue
            elif choice == 2:
                show_cart(user)
                continue
            elif choice == 3:
                view_profile(user)
                continue
            elif choice == 4:
                update_profile(user)
                continue
            elif choice == 5:
                show_my_bills(user)
                continue
            elif choice == 6:
                show_my_plan(user)
                continue
            elif choice == 7:
                print("Logging out...")
                sys.exit(1)
            else:
                print("Invalid choice. Please enter a valid option.")
    except Exception as e:
        print("An error occurred during menu execution:", e)

def view_categories(user):
    print_line_2()
    print("Categories:-")
    print_line_2()
    print("1.Electronics")
    print("2.Clothing")
    print("3.Home decor and Furniture")
    print("4.Skincare")
    print("5.Toys and Games")
    print("6.Fitness equipment")
    print("7.Jewelry and accessories")
    print("8.Books and media")
    print("9.Art supplies")
    print("10.Groceries")
    print("11.Travel tools")
    print("12.Pet supplies")

    try:
        choice = int(input("\nEnter your choice:-"))
        if choice == 1:
            print_products("Electronics.txt", user)
        elif choice == 2:
            print_products("Clothing.txt", user)
        elif choice == 3:
            print_products("Home_decor_and_Furniture.txt", user)
        elif choice == 4:
            print_products("Skincare.txt", user)
        elif choice == 5:
            print_products("Toys_and_Games.txt", user)
        elif choice == 6:
            print_products("Fitness_equipment.txt", user)
        elif choice == 7:
            print_products("Jewelry_and_accessories.txt", user)
        elif choice == 8:
            print_products("Books_and_media.txt", user)
        elif choice == 9:
            print_products("Art_supplies.txt", user)
        elif choice == 10:
            print_products("Groceries.txt", user)
        elif choice == 11:
            print_products("Travel_tools.txt", user)
        elif choice == 12:
            print_products("Pet_supplies.txt", user)
        else:
            print("Invalid choice. Please enter a number between 1 and 12.")
            view_categories(user)  
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        view_categories(user)  

def validateUserName(userName):
    try:
        while True:
            if userName[0].isalpha():
                return userName
            else:
                userName = input("First Letter Must be an Alphabet. Retry: ")
    except Exception as e:
        print("An error occurred during username validation:", e)



def validatePassword(password):
    small, cap, dig, sp = 0, 0, 0, 0
    while True:
        if len(password) >= 8:
            for i in password:
                if i.isupper():
                    cap += 1
                if i.islower():
                    small += 1
                if i.isdigit():
                    dig += 1
                if i == "@" or i == "$":
                    sp += 1
            if cap >= 1 and small >= 1 and dig >= 1 and sp >= 1:
                return password
            else:
                print('''
Requirements of Password :
1) Minimum 8 Characters
2) At least 1 Upper Case
3) At least 1 Lower Case
4) At least 1 Digit Case
5) At least 1 Special Character from "@" and "$"
                ''')
                password = input("Retry: ")
        else:
            print('''
Requirements of Password :
1) Minimum 8 Characters
2) At least 1 Upper Case
3) At least 1 Lower Case
4) At least 1 Digit Case
5) At least 1 Special Character from "@" and "$"
                ''')
            password = input("Retry: ")

def login():
    while True:
        userName = input("Enter UserName: ")
        with open("registeredUsers\\registeredUserNames.txt", "r") as usernm_file:
            if userName in usernm_file.read():
                while True:
                    password = input("Enter Password: ")
                    user = validateLogin(userName, password)
                    if user:
                        print("Login Successfull")
                        if user.is_member:
                            Register.membership_level = check_membership_level(
                                userName)
                            if Register.membership_level:
                                print(f"Welcome {userName}! You are a {Register.membership_level} member.")
                        menu(userName)
                        break
                    else:
                        print("Invalid Password.")
                        continue
                break
            else:
                print("Username not found. Please try again.")

def check_membership_level(username):
    try:
        membership_levels = ['members_500.txt',
                             'members_1000.txt', 'members_1500.txt']
        current_date = datetime.now()
        for level_file in membership_levels:
            file_path = os.path.join('registeredUsers', level_file)
            print("Checking file path:", file_path)
            with open(file_path, 'r') as file:
                for line in file:
                    membership_info = line.strip().split(", ")
                    start_date_str = membership_info[1].split(": ")[1]
                    end_date_str = membership_info[2].split(": ")[1]
                    username_str = membership_info[3].split(": ")[1]

                    if username_str == username:
                        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                        if start_date <= current_date <= end_date:
                            if '500' in level_file:
                                return '500'
                            elif '1000' in level_file:
                                return '1000'
                            elif '1500' in level_file:
                                return '1500'
        return None
    except Exception as e:
        print("An error occurred during membership level check:", e)
        return None

def validateLogin(userName, entered_password):
    with open("registeredUsers\\userDetails.txt", "r") as user_details_file:
        for line in user_details_file:
            user_details = eval(line)
            if user_details['username'] == userName and user_details['password'] == entered_password:
               
                user_instance = Register(
                    user_details['username'],
                    user_details['password'],
                    user_details.get('mobile'),
                    user_details.get('email'),
                    user_details.get('age')
                )
                return user_instance  
        return None



def register():
    try:
        flag_username = 0
        userName = input("Enter UserName: ")
        userName = validateUserName(userName)

        with open("registeredUsers\\registeredUserNames.txt", "a+") as usernm:
            usernm.seek(0)
            data = usernm.read()

            while flag_username != 1:
                if userName in data:
                    print("Username already taken. Please try another username.")
                    userName = input("Enter UserName: ")
                    userName = validateUserName(userName)
                else:
                    usernm.write(userName + "\n")
                    usernm.flush()
                    flag_username = 1

        password = input('''
    Enter Password.
    Requirements of Password :
    1) Minimum 8 Characters
    2) At least 1 Upper Case
    3) At least 1 Lower Case
    4) At least 1 Digit Case
    5) At least 1 Special Character from "@" and "$"
        ''')
        password = validatePassword(password)

        while True:
            mobile = input("Enter Mobile Number: ")
            if len(mobile) == 10 and mobile.isdigit() and mobile[0] in ['7', '8', '9']:
                break
            else:
                print("Invalid mobile number. Mobile number should be 10 digits and start with 7, 8, or 9.")

        email = input("Enter Email: ")
        email = validateEmail(email)
        while True:
            age = input("Enter Age: ")
            if age.isdigit() and int(age) >= 0:
                break
            else:
                print("Invalid input. Age should be a non-negative integer.")

        is_member = False
        ob = Register(userName, password, mobile, email, age, is_member)
        ob.registerUser(userName, password, mobile, email, age, is_member)
    except Exception as e:
        print("An error occurred during registration:", e)
        
def validateEmail(email):
    while True:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(pattern, email):
            print("Valid email address: ")
            return email
        else:
            print("Invalid email address. Please enter a valid email address.")
            email=input("Enter correct Email Id: ")

def print_line():
    print("=" * 40)
def print_line_2():
    print("-"*40)

def mainMenu():
    while True:
        print("\nWelcome!")
        print_line()
        print(" " * 14 + "MAIN MENU" + " " * 14) 
        print_line()
        print("Are you a User or an Admin?")
        user_choice = input("Enter 'user' or 'admin': ")

        if user_choice.lower() == 'user':
            while True:
                print_line_2()
                print("1 - Login")
                print("2 - Register")
                print("3 - About-us")
                print("4 - Exit")
                print_line_2()
                try:
                    choice = int(input("Enter Choice: "))
                except ValueError:
                    print("Invalid Choice.")
                    continue

                if choice == 1:
                    login()
                elif choice == 2:
                    register()
                elif choice == 3:
                    
                    pass
                elif choice == 4:
                    print("Thank You!!")
                    break
            break
        elif user_choice.lower() == 'admin':
            admin = Admin()
            while True:
                print("\nWelcome to Admin Portal")
                if admin.admin_login():
                    admin.admin_menu()
                    break
                else:
                    print("Invalid admin credentials. Please try again.")
            break
        else:
            print("Invalid choice. Please enter 'user' or 'admin'.")

mainMenu()
