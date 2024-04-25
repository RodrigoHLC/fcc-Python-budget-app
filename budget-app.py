class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
    
    # MAKING DEPOSITS
    def deposit(self, amount, description=""):
        self.ledger.append({
            "amount": float(format(amount, ".2f")),
            "description": description
        })

    # GETTING THE BALANCE
    def get_balance(self):
        return sum(list(map(lambda obj: obj["amount"], self.ledger)))

    # CHECKING IF AVAILABLE FUNDS ARE ENOUGH FOR A WITHDRAWAL
    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        else:
            return True

    # WITHDRAWING MONEY
    def withdraw(self, amount, description=""):
        # CHECK AVAILABLE FUNDS
        if self.check_funds(amount):
            # IF THERE'S ENOUGH FUNDS:
            self.ledger.append({
                "amount": float(format(amount * -1, ".2f")),
                "description": description
            })
            return True
        # IF NOT ENOUGH FUNDS:
        else:
            return False
    # MAKING TRANSFERS
    def transfer(self, amount, category):
        # CHECK AVAILABLE FUNDS
        if self.check_funds(amount):
            # IF THERE'S ENOUGH FUNDS:
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        # IF NOT ENOUGH FUNDS
        else:
            return False
    
    # - - - S T R I N G    R E T U R N S  - - -
    # - - - S T R I N G    R E T U R N S  - - -
    items_string = ""

    # FUNCTION FOR CREATING description______amount STRING
    def item_to_string(self, item):

        # 1) CHECK NUMBER OF DECIMAL POINTS
        amount_string = f"{item['amount']}"
        if amount_string[-2] == ".": # ONLY ONE DECIMAL POINT
            amount_string += "0"

        # 2) CHECK HOW MANY SPACES TO ADD
        space_length = 30 - len(item['description'][:23]) - len(amount_string)

        # 3) CREATE STRING
        self.items_string += f"{item['description'][:23]}{' ' * space_length}{amount_string[-7:]}\n"
    # ↑ ↑ ↑ END OF item_to_string FUNCTION ↑ ↑ ↑ 

    # - - - SETUP STRING RETURN FOR CLASS OBJECTS - - -
    def __str__(self):
        # 1) CREATE ******TITLE****** STRING
        name_len = len(self.name)
        star_number = (30 - name_len) // 2
        star_string = f"{'*' * star_number}"
        title_string = f"{star_string}{self.name}{star_string}"

        # 2) CREATE ITEM STRINGS WITH map AND item_to_string() FUNCTION
        # items_string = ""  # UNUSED
        list(map(lambda obj: self.item_to_string(obj), self.ledger))
        # ANOTHER WAY TO DO IT:
        # for obj in self.ledger:
            # self.item_to_string(obj)

        # 3) CREATE Total END-STRING 
        total_string = "Total: "
        total_string += str(self.get_balance())
        
        # 4) ADD EVERYTHING TO FINAL STRING AND RETURN
        return str(f"{title_string}\n{self.items_string}{total_string}")      
    # ↑ ↑ ↑ END OF SETTING STRING RETURN FOR CLASS OBJECTS ↑ ↑ ↑ 

    
# - - - SETUP STRING RETURN FOR EXPENSES CHART - - -
# - - - SETUP STRING RETURN FOR EXPENSES CHART - - -

def create_spend_chart(categories): # categories WILL BE A LIST

    # 1) CALCULATE TOTAL SPENDING FOR ALL CATEGORIES
    exp_per_cat=[]
    # WORK ON EACH CATEGORY'S LEDGER
    for cat in categories:
        # A) FILTER ONLY NEGATIVE NUMBERS (EXPENSES)
        exp_arr = list(filter(lambda spent: spent["amount"] < 0 , cat.ledger))

        # B) CALCULATE TOTAL EXPENSE IN EACH SEPARATE CATEGORY
        exp_per_cat.append(float(format(sum(map(lambda obj: obj["amount"], exp_arr)),".2f") ))

        # C) CALCULATE TOTAL EXPENSE ADDING ALL CATEGORY'S EXPENSE
        total_exp = sum(exp_per_cat)

        # D) CALCULATE PERCENTAGE OF TOTAL SPENDING FOR EACH CATEGORY, ROUNDED DOWN TO NEAREST MULTIPLE OF 10
        exp_percentages = list(map(lambda exp: int(exp / total_exp * 100//10*10), exp_per_cat))
        # ↑ ↑ ↑ exp_percentages WILL BE USED IN mark_row() FUNCTION

    # 2) TITLE STRING
    title = rf"Percentage spent by category"

    # 3) FUNCTION FOR DETERMINING "o" or " "
    def mark(category_percentage, row_percentage):
        # row_percentage WILL GO FROM 100 TO 0 
        if category_percentage >= row_percentage:
            return " o "
        else:
            return "   "

    # 4) FUNCTION FOR BUILDING 1 ROW STRING
    def mark_row(exp_percentages, row_percentage):
        notches_string = f""    
        for category_percentage in exp_percentages:
            notches_string += f"{mark(category_percentage, row_percentage)}"
        return notches_string

    # 5) BUILD EVERY ROW STRING
    bars_string = ""
    per = 100 
    while per >= 0:
        # row_string = ""
        notches = mark_row(exp_percentages, per)
        if per == 100:
            bars_string += f"{per}|{notches} \n"
        elif per == 0:
            bars_string += f"  {per}|{notches} "
        else:
            bars_string += f" {per}|{notches} \n"
        per -= 10

    # 6) BUILD '--------' STRING
    hyphens_string = f"    {'---' * len(exp_percentages)}-"

    # --- CREATE VERTICAL CATEGORY NAMES ---

    # 1) FIND LENGTH OF LONGEST CATEGORY NAME
    longest = max(map(lambda cat: len(cat.name), categories))
    names_array = list(map(lambda cat: cat.name, categories))
    names_string = f""
    
    # 2) CREATE STRINGS
    # LOOP AS MANY TIMES AS LONGEST NAME LENGTH-1
    for letter_index in range(0, longest):
        # ADD LEFT MARGIN TO STRING
        names_string+="    "
        
        # ADD LETTER OR SPACE TO STRING
        for name in range(0, len(names_array)):
            try:
                names_array[name][letter_index]
                names_string += f" {names_array[name][letter_index]} "
            # IF CATEGORY NAME IS SHORTER THAN LONGEST CAT. NAME
            except IndexError:
                names_string += f"   "                

        # ADD BREAK SPACE AT END OF EVERY STRING
        if letter_index < longest-1:
            names_string += f" \n"
        # DON'T ADD BREAK SPACE AFTER LAST STRING
        else:
            names_string += f" "
            
    # CREATE FINAL STRING
    final_string = f"{title}\n{bars_string}\n{hyphens_string}\n{names_string}"
    return final_string


# food = Category("Food")
# food.deposit(1000, "deposit")
# food.withdraw(10.15, "groceries")
# food.withdraw(15.89, "restaurant and more food for dessert")
# clothing = Category("Clothing")
# auto = Category("Auto")
# food.transfer(60, clothing)
# clothing.withdraw(35, "anything")
# auto.deposit(200, "Depo")
# auto.withdraw(20, "Whatever")
# print(food)
# print(create_spend_chart([food, clothing,auto]))

# TEST
food = Category("Food")
entertainment = Category("Entertainment")
business = Category("Business")
food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")
food.withdraw(105.55, "Groceries")
food.withdraw(5.00, "Hot dog")
food.transfer(1, business)
entertainment.withdraw(33.40)
business.withdraw(10.99)
print("\n",food)
print("\n",create_spend_chart([business, food, entertainment]))
# print("Percentage spent by category\n100|          \n 90|          \n 80|          \n 70|    o     \n 60|    o     \n 50|    o     \n 40|    o     \n 30|    o     \n 20|    o  o  \n 10|    o  o  \n  0| o  o  o  \n    ----------\n     B  F  E  \n     u  o  n  \n     s  o  t  \n     i  d  e  \n     n     r  \n     e     t  \n     s     a  \n     s     i  \n           n  \n           m  \n           e  \n           n  \n           t  ")
# TEST STRING:
# print(r"Percentage spent by category\\n100|          \\n 90|          \\n 80|          \\n 70|    o     \\n 60|    o     \\n 50|    o     \\n 40|    o     \\n 30|    o     \\n 20|    o  o  \\n 10|    o  o  \\n  0| o  o  o  \\n    ----------\\n     B  F  E  \\n     u  o  n  \\n     s  o  t  \\n     i  d  e  \\n     n     r  \\n     e     t  \\n     s     a  \\n     s     i  \\n           n  \\n           m  \\n           e  \\n           n  \\n           t  ")
# print(sum(list(map(lambda obj: obj["amount"], comida.ledger))))
# print(comida.check_funds(60))
# <map object at 0x10ddca0>
# <boundmethod Category.get_balance of <__main__.Category object at 0xc7fd90>>
