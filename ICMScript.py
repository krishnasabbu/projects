import pandas as pd
import os
import zipfile
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def zip_folder(folder_path):
    folder_name = os.path.basename(folder_path)
    zip_name = os.path.join(folder_path, f'{folder_name}.zip')
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for foldername, _, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))


# Read Excel file
df = pd.read_excel('your_excel_file.xlsx')  # Replace 'your_excel_file.xlsx' with the path to your Excel file

# Initialize the webdriver (you need to have ChromeDriver installed)
driver = webdriver.Chrome()

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    number = row['number']
    folder_path = row['folder_path']

    # Open folder with the number found in Excel
    folder_name = os.path.join(folder_path, str(number))
    if os.path.exists(folder_name) and os.path.isdir(folder_name):
        # Zip all files in the folder
        zip_folder(folder_name)
        print(f'Files in folder "{folder_name}" zipped into "{folder_name}.zip"')

        # Open application with Selenium
        driver.get("https://example.com")  # Replace with the URL of the application

        # Find the username and password input fields and enter the credentials
        username_field = driver.find_element_by_id(
            "username")  # Replace "username" with the actual ID of the username input field
        password_field = driver.find_element_by_id(
            "password")  # Replace "password" with the actual ID of the password input field

        username_field.send_keys("your_username")  # Replace "your_username" with your actual username
        password_field.send_keys("your_password")  # Replace "your_password" with your actual password

        # Find and click the sign-in button
        sign_in_button = driver.find_element_by_id(
            "signOnButtonSpan")  # Replace "signOnButtonSpan" with the actual ID of the sign-in button
        sign_in_button.click()

        print("Logged in successfully")

    else:
        print(f'Folder "{folder_name}" not found for number {number}')

# Close the webdriver
driver.quit()
