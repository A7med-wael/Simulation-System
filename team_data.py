import pandas as pd

# Example data (assuming EMAILS, NAMES, and GITHUPS contain some sample data)
EMAILS = ["mohamed.hamdey.hafez@gmail.com", "ahmed.7wael.77@gmail.com", "michealhany991@gmail.com", "beshoyfarouk645@gmail.com","Mohamedalielshafei7@gmail.com"]
NAMES = ["Mohamed Hamdey Mohamed Hafez", "Ahmed Wael Hamed", "Michal Hany Kamal", "Bishoy Farouk","Mohamed Ali Mohamed Al-Shafei"]
GITHUPS = ["https://github.com/Mohamed-Hamdey", "https://github.com/A7med-wael", "https://github.com/Micheal-Hany","https://github.com/BF-BALE11","https://github.com/shafei2004"]

# Define the file path for output
file_path = "team_data.txt"

# Open the file in write mode
with open(file_path, 'w') as file:
    # Write header to the file
    file.write("Team Data:\n\n")
    
    # Loop through each team member's data and write to the file
    for name, email, github in zip(NAMES, EMAILS, GITHUPS):
        file.write(f"Name: {name}\n")
        file.write(f"Email: {email}\n")
        file.write(f"GitHub: {github}\n")
        file.write("\n")  # Add a newline between each member's data

print(f"Team data has been written to {file_path}")

    

