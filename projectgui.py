
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QComboBox)
from PySide6.QtCore import Slot


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        menu_label = QLabel("CST-205 Smart Recipe Project")
        menu1_label = QLabel("Choose a food category")

        self.food_input = QLineEdit()
        self.food_input.setPlaceholderText("For Example: Breakfast, Lunch, or Dinner")

        btn = QPushButton('Next')
        btn.clicked.connect(self.open_win)

        layout = QVBoxLayout()
        layout.addWidget(menu_label)
        layout.addWidget(menu1_label)
        layout.addWidget(self.food_input)
        layout.addWidget(btn)
        self.setLayout(layout)
        self.show()

    @Slot()
    def open_win(self):
        food_category = self.food_input.text()
        # In order for it to go through, you need to make sure the first letter is capitalized
        # So if you type in breakfast It should be with capital B.

        if food_category in ['Breakfast', 'Lunch', 'Dinner']:
            choose_type = {
                'Breakfast': ['Most Nutrition', 'Balanced', 'Least Nutrition'],
                'Lunch': ['Most Nutrition', 'Balanced', 'Least Nutrition'],
                'Dinner': ['Most Nutrition', 'Balanced', 'Least Nutrition']
            }
            self.new_win = NewWindow(food_category, choose_type[food_category])
            self.new_win.show()


class NewWindow(QWidget):
    def __init__(self, category_name, options):
        super().__init__()
        self.category_name = category_name

        category_label = QLabel(f"Category: {category_name}")

        self.options_dropdown = QComboBox()
        self.options_dropdown.addItems(options)

        btn = QPushButton('Show me recipes')
        btn.clicked.connect(self.show_recipes)

        layout = QVBoxLayout()
        layout.addWidget(category_label)
        layout.addWidget(self.options_dropdown)
        layout.addWidget(btn)
        self.setLayout(layout)

    @Slot()
    def show_recipes(self):
        selected_option = self.options_dropdown.currentText()
        self.new_win = NewWindow1(self.category_name, selected_option)
        self.new_win.show()


class NewWindow1(QWidget):
    def __init__(self, category_name, selected_option):
        super().__init__()
        self.setWindowTitle(f"Recipes for {category_name} - {selected_option}")

# these are temporary just to get the functionality working, eventually will implement it using an API
        recipes = {
            'Breakfast': {
                'Most Nutrition': ['Oatmeal', 'Omelette', 'Smoothie'],
                'Balanced': ['Avocado Toast', 'Yogurt with Granola', 'Pancakes'],
                'Least Nutrition': ['Bacon and Eggs', 'Cereal', 'Doughnut']
            },
            'Lunch': {
                'Most Nutrition': ['Chicken Salad', 'Veggie Bowl', 'Soup'],
                'Balanced': ['Turkey Sandwich', 'Chicken Wrap', 'Tuna Sandwich'],
                'Least Nutrition': ['Cheeseburger', 'Hot Dog', 'Pizza']
            },
            'Dinner': {
                'Most Nutrition': ['Grilled Salmon', 'Chicken and Rice', 'Steak and Veggies'],
                'Balanced': ['Spaghetti', 'Grilled Chicken', 'Fajitas'],
                'Least Nutrition': ['Fried Chicken', 'Mac and Cheese', 'Burrito']
            }
        }

        category_recipes = recipes.get(category_name, {})
        recipe_text = "Recipes: "
        for recipe in category_recipes.get(selected_option):
            recipe_text += recipe + ", "
            
        recipe_label = QLabel(recipe_text)

        layout = QVBoxLayout()
        layout.addWidget(recipe_label)
        self.setLayout(layout)



app = QApplication([])
my_win = MyWindow()
sys.exit(app.exec())