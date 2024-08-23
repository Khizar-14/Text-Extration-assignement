import easyocr
import pandas as pd
import re

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Path to your image file
image_path = "C:\\Users\\Khiza\\Downloads\\Sample Problem.pdf"

# Extract text from the image
results = reader.readtext(image_path)

# Process the extracted data
data = []
for res in results:
    text = res[1]
    if isinstance(text, str) and "TXK" in text:  # Filter entries based on expected format
        data.append(text)

# Debugging: Print out the extracted data to understand the structure
print("Extracted Data:")
for entry in data:
    print(entry)

# Creating lists to store structured data
structured_data = {
    "ID": [],
    "Name": [],
    "Relative Name": [],
    "Relative Type": [],
    "House Number": [],
    "Age": [],
    "Gender": [],
    "Photo Available": []
}

# Regular expression patterns
id_pattern = r"TXK\d+"
name_pattern = r"Name:\s*(.*?)\s*(Father|Husband)"
relative_name_pattern = r"(Father|Husband)'s\s*Name:\s*(.*?)\s*House"
house_pattern = r"House Number:\s*(\d+)?"
age_pattern = r"Age:\s*(\d+)"
gender_pattern = r"Gender:\s*(Male|Female)"
photo_pattern = r"(Available)"

# Parsing the extracted data into structured format
for entry in data:
    try:
        # Extracting ID
        id_match = re.search(id_pattern, entry)
        id_ = id_match.group(0) if id_match else ""

        # Extracting Name
        name_match = re.search(name_pattern, entry)
        name = name_match.group(1) if name_match else ""

        # Extracting Relative Name and Type
        relative_match = re.search(relative_name_pattern, entry)
        relative_name = relative_match.group(2) if relative_match else ""
        relative_type = relative_match.group(1) if relative_match else ""

        # Extracting House Number
        house_match = re.search(house_pattern, entry)
        house_number = house_match.group(1) if house_match else ""

        # Extracting Age
        age_match = re.search(age_pattern, entry)
        age = age_match.group(1) if age_match else ""

        # Extracting Gender
        gender_match = re.search(gender_pattern, entry)
        gender = gender_match.group(1) if gender_match else ""

        # Extracting Photo Availability
        photo_match = re.search(photo_pattern, entry)
        photo_available = "Available" if photo_match else "Not Available"

        # Append extracted fields to the structured data
        structured_data["ID"].append(id_)
        structured_data["Name"].append(name)
        structured_data["Relative Name"].append(relative_name)
        structured_data["Relative Type"].append(relative_type)
        structured_data["House Number"].append(house_number)
        structured_data["Age"].append(age)
        structured_data["Gender"].append(gender)
        structured_data["Photo Available"].append(photo_available)

    except Exception as e:
        print(f"Skipping entry due to error: {entry} - {e}")
        continue

# Convert structured data into a DataFrame
df_structured = pd.DataFrame(structured_data)

# Save DataFrame to an Excel file
excel_path = 'extracted_data.xlsx'
df_structured.to_excel(excel_path, index=False)

print(f"Data saved to {excel_path}")
