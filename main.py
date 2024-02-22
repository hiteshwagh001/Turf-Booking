import json
import sys
from datetime import datetime, timedelta

from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class WelcomePage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Welcome Page")
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)  # Remove window frame
        screen =QDesktopWidget().screenGeometry()
        self.setGeometry(screen)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setStyleSheet("background-color:#cef8a7;")

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(200, 100, 200, 100)  # Set margins to center the widget

        app_name_label = QLabel("<center><h1 style='color: black; font-family: Kode Mono; font-weight: bold;'>Book My Turf</h1></center>")
        font = QFont("Impact", 72)  # Create a QFont object with desired font size
        app_name_label.setFont(font)  # Set the font for the QLabel
        layout.addWidget(app_name_label, alignment=Qt.AlignCenter)

        # Create stacked widget to hold images
        self.image_stack = QStackedWidget()
        width = int(self.width() * 0.8)
        height = int(self.height() * 0.4)
        self.image_stack.setFixedSize(width, height)  # Set fixed size
        layout.addWidget(self.image_stack, alignment=Qt.AlignCenter)

        # Add images to stacked widget
        self.add_images_to_stack(["assets/team.jpg", "assets/hr1.jpg", "assets/hr3.jpg", "assets/hr2.jpg"])

        # Get Started button with style
        get_started_button = QPushButton("Get Started")
        get_started_button.setStyleSheet("""
            QPushButton {
                padding: 15px 30px;
                font-size: 24px;
                background-color: #4CAF50; /* Background color */
                color: white;
                border: none;
                border-radius: 25px; /* Border radius */
            }
            QPushButton:hover {
                background-color: #45a049; /* Darker green on hover */
            }
        """)
        get_started_button.clicked.connect(self.show_login_page)
        layout.addWidget(get_started_button, alignment=Qt.AlignCenter)

        # Set up timer to automatically slide images
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_image)
        self.timer.start(3000)  # Change image every 3 seconds

    def show_login_page(self):
        login_page = LoginPage(self)
        login_page.show()
        self.hide()

    def add_images_to_stack(self, image_paths):
        for path in image_paths:
            image_label = QLabel()
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(self.image_stack.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            self.image_stack.addWidget(image_label)

    def next_image(self):
        current_index = self.image_stack.currentIndex()
        next_index = (current_index + 1) % self.image_stack.count()
        self.image_stack.setCurrentIndex(next_index)
        
class LoginPage(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Login Page")
        screen =QDesktopWidget().screenGeometry()
        self.setGeometry(screen)  # Set window size to fullscreen

        self.welcome_page = parent  # Store the reference to the WelcomePage instance

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(200, 100, 200, 100)  # Set margins to center the widget
        # self.setStyleSheet("background-image: url(assets/team.jpg); background-repeat: no-repeat; background-position: center; background-size: cover;")

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        self.login_widget = QWidget()
        self.stacked_widget.addWidget(self.login_widget)
        self.setup_login_page()

        self.signup_widget = QWidget()
        self.stacked_widget.addWidget(self.signup_widget)
        self.setup_signup_page()
        self.stacked_widget.setCurrentWidget(self.login_widget)

    def setup_login_page(self):
        # Create the sign-in card widget
        sign_in_layout = QVBoxLayout(self.login_widget)
        

        self.login_widget.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; padding: 20px; max-width: 400px;")

        title_label = QLabel("<center><h1 style='color: #333;'> Login Form</h1></center>")
        sign_in_layout.addWidget(title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        self.username_input.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 15px;")
        sign_in_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 15px;")
        self.password_input.setEchoMode(QLineEdit.Password)
        sign_in_layout.addWidget(self.password_input)

        login_button = QPushButton("Login")
        login_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px;")
        login_button.clicked.connect(self.check_login)
        sign_in_layout.addWidget(login_button)

        remember_me_checkbox = QCheckBox("Terms and Condition*")
        remember_me_checkbox.setStyleSheet("color: #333;")
        sign_in_layout.addWidget(remember_me_checkbox)

        cancel_button = QPushButton("Signup")
        cancel_button.setStyleSheet("background-color: #f44336; color: white; border: none; padding: 10px;")
        cancel_button.clicked.connect(self.show_signup_page)
        sign_in_layout.addWidget(cancel_button)

        forgot_password_label = QLabel("<center><a href='#' style='color: #333;'>Forgot password?</a></center>")
        sign_in_layout.addWidget(forgot_password_label)
    
        # Create the sign-up card widget
    def setup_signup_page(self):
        signup_layout = QVBoxLayout(self.signup_widget)
        signup_layout.setContentsMargins(10,10,10 ,300)
        signup_layout.setSpacing(10)

        # signup_layout
        self.signup_widget.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; padding: 20px; max-width: 400px;")

        # Add vertical spacer item to push the sign-up form to the top
        signup_layout.addSpacerItem(QSpacerItem(0, 20))
        title_label = QLabel("<center><h1 style='color: #333;'> Signup Form</h1></center>")
        signup_layout.addWidget(title_label)

        self.signup_username_input = QLineEdit()
        self.signup_username_input.setPlaceholderText("Enter Username")
        self.signup_username_input.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 15px;")
        signup_layout.addWidget(self.signup_username_input)

        self.signup_email_input = QLineEdit()
        self.signup_email_input.setPlaceholderText("Enter Email")
        self.signup_email_input.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 15px;")
        signup_layout.addWidget(self.signup_email_input)

        self.signup_password_input = QLineEdit()
        self.signup_password_input.setPlaceholderText("Enter Password")
        self.signup_password_input.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 15px;")
        self.signup_password_input.setEchoMode(QLineEdit.Password)
        signup_layout.addWidget(self.signup_password_input)

        signup_button = QPushButton("Sign Up")
        signup_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px;")
        signup_button.clicked.connect(self.save_signup_data)
        signup_layout.addWidget(signup_button)

        signin_button = QPushButton("Sign In")
        signin_button.setStyleSheet("background-color: #f44336; color: white; border: none; padding: 10px;")
        signin_button.clicked.connect(self.welcome_page.show_login_page)  # Use the reference to WelcomePage
        signup_layout.addWidget(signin_button)

    def show_signup_page(self):
        self.stacked_widget.setCurrentWidget(self.signup_widget)

    def save_signup_data(self):
        signup_data = {
            "username": self.signup_username_input.text(),
            "email": self.signup_email_input.text(),
            "password": self.signup_password_input.text()
        }
        with open("signup_data.json", "a") as file:
            json.dump(signup_data, file)
            file.write("\n")  # Add a new line for each entry

        self.welcome_page.show_login_page()  # Use the reference to WelcomePage

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        found = False
        with open("signup_data.json", "r") as file:
            for line in file:
                data = json.loads(line)
                if data["username"] == username and data["password"] == password:
                    print("Login Successful")
                    self.show_game_selection_page(username)
                    found = True
                    break

        if not found:
            QMessageBox.warning(self, "Invalid Login", "Invalid username or password. Please try again.")

    def show_game_selection_page(self, username):
        game_selection_page = GameSelectionPage(self, username)
        self.stacked_widget.addWidget(game_selection_page)
        self.stacked_widget.setCurrentWidget(game_selection_page)

class GameSelectionPage(QWidget):
    def __init__(self, parent=None, username=None):
        super().__init__(parent)
        self.setWindowTitle("Game Selection")
        self.parent = parent
        self.username = username

        layout = QGridLayout(self)
        layout.setContentsMargins(200, 100, 200, 100)
        
        # Add heading
        choose_game_label = QLabel("<h1>Choose the Game</h1>")
        layout.addWidget(choose_game_label, 0, 0, 1, 3, Qt.AlignCenter)  # Span 1 row, 3 columns

        # Dictionary containing game names and corresponding image paths
        games = {
            "Cricket": "assets/cricket.jpg",
            "Football": "assets/football.jpg",
            "Tennis": "assets/tennis.jpg",
            "Basketball": "assets/basketball.jpg",
            "Golf": "assets/golf.jpg",
            "Baseball": "assets/baseball.jpg"
        }

        # Iterate over games and add buttons with images and game names
        row, col = 1, 0  # Start from the second row
        for game, image_path in games.items():
            # Create button
            button = QPushButton()
            button.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    padding: 20px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)
            button.setIcon(QIcon(image_path))  # Set icon/image
            button.setIconSize(QSize(200, 200))  # Set icon size
            button.clicked.connect(lambda checked, game=game: self.select_game_slot(game))  # Connect slot
            layout.addWidget(button, row, col, Qt.AlignCenter)  # Add button to layout
            layout.addWidget(QLabel(game), row + 1, col, Qt.AlignCenter)  # Add game name label
            col += 1
            if col > 2:
                col = 0
                row += 2

    def select_game_slot(self, game):
        game_details_page = GameDetailsPage(self.parent, self.username, game)
        self.parent.stacked_widget.addWidget(game_details_page)
        self.parent.stacked_widget.setCurrentWidget(game_details_page)
        
class GameDetailsPage(QWidget):
    def __init__(self, parent=None, username=None, game=None):
        super().__init__(parent)
        self.setWindowTitle("Game Details")
        self.parent = parent
        self.username = username
        self.game = game
        self.selected_slots = set()  # Set to store selected slots

        layout = QVBoxLayout(self)
        layout.setContentsMargins(200, 100, 200, 100)

        title_label = QLabel(f"<center><h1 style='color: #333;'>{game} Slot Details</h1></center>")
        layout.addWidget(title_label)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        # Define available time slots starting from 6:00 AM to 11:00 PM (24-hour format)
        start_time = 6
        end_time = 23
        time_slots = [f"{str(hour).zfill(2)}:00 -  {str(hour+1).zfill(2)}:00" for hour in range(start_time, end_time + 1)]

        # Read existing bookings from JSON file
        existing_bookings = []
        try:
            with open("booking_data.json", "r") as file:
                for line in file:
                    booking = json.loads(line)
                    if booking["game"] == self.game:
                        existing_bookings.append(booking)
        except FileNotFoundError:
            pass

        # Create slots boxes with checkboxes
        for i, time_slot in enumerate(time_slots):
            slot_frame = QFrame()
            slot_frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            slot_frame.setFixedSize(120, 40)  # Set fixed size

            checkbox = QCheckBox(time_slot)
            checkbox.setStyleSheet("margin-left: 5px;")  # Add margin to checkbox text
            checkbox.setChecked(self.is_slot_booked(time_slot, existing_bookings))
            checkbox.stateChanged.connect(lambda state, slot=time_slot: self.toggle_slot(state, slot))
            
            frame_layout = QHBoxLayout(slot_frame)
            frame_layout.addWidget(checkbox, alignment=Qt.AlignCenter)
            grid_layout.addWidget(slot_frame, i // 6, i % 6)

            # Set background color based on slot availability
            if checkbox.isChecked():
                slot_frame.setStyleSheet("background-color: #f44336;")  # Red color if booked
                checkbox.setEnabled(False)  # Disable checkbox if slot is booked
            else:
                slot_frame.setStyleSheet("background-color: #4CAF50;")  # Green color if available

        layout.addLayout(grid_layout)
        # Add button to book selected slots
        book_button = QPushButton("Book Selected Slots")
        book_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px;")
        book_button.clicked.connect(self.book_selected_slots)
        layout.addWidget(book_button, alignment=Qt.AlignCenter)

        # Add button to redirect to game selection page
        back_button = QPushButton("Back to Game Selection")
        back_button.setStyleSheet("background-color: #f44336; color: white; border: none; padding: 10px;")
        back_button.clicked.connect(self.back_to_game_selection)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

    def is_slot_booked(self, selected_slot, existing_bookings):
        current_date = datetime.now().strftime("%Y-%m-%d")
        for booking in existing_bookings:
            if (booking["date"] == current_date and
                booking["from"] <= selected_slot < booking["to"]):
                return True
        return False

    def toggle_slot(self, state, selected_slot):
        if state == Qt.Checked:
            self.selected_slots.add(selected_slot)
        else:
            self.selected_slots.discard(selected_slot)

    def book_selected_slots(self):
        if not self.selected_slots:
            QMessageBox.warning(self, "No Slots Selected", "Please select at least one slot to book.")
        else:
            for slot in self.selected_slots:
                self.book_slot(slot)

    def book_slot(self, selected_slot):
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Extract start time from selected_slot
        start_time_str = selected_slot.split(" - ")[0]
        
        booking_data = {
            "game": self.game,
            "from": start_time_str,  # Use extracted start time
            "to": (datetime.strptime(start_time_str, "%H:%M") + timedelta(hours=1)).strftime("%H:%M"),
            "user": self.username,
            "date": current_date
        }
    
        # Write the new booking data to the JSON file
        with open("booking_data.json", "a") as file:
            json.dump(booking_data, file)
            file.write("\n")
        QMessageBox.information(self, "Slot Booked", "Slot booked successfully!")
        self.parent.stacked_widget.setCurrentWidget(GameSelectionPage(self.parent, self.username))


    def back_to_game_selection(self):
        game_selection_page = GameSelectionPage(self.parent, self.username)
        self.parent.stacked_widget.addWidget(game_selection_page)
        self.parent.stacked_widget.setCurrentWidget(game_selection_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_page = WelcomePage()
    welcome_page.show()
    sys.exit(app.exec_())