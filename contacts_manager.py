# Contact Management System
# Week 3 Project - Functions & Dictionaries (Rewritten Version)

import json
import re
from datetime import datetime
import csv

# =========================================================
# STEP 1 & 2: DATA STRUCTURE + VALIDATION FUNCTIONS
# =========================================================

contacts = {}  # Main dictionary to store all contact data

def validate_phone(phone):
    """Validate and clean phone number (10–15 digits allowed)"""
    digits = re.sub(r'\D', '', phone)
    return (10 <= len(digits) <= 15), digits if (10 <= len(digits) <= 15) else None

def validate_email(email):
    """Validate email format using regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


# =========================================================
# STEP 3: CRUD OPERATIONS
# =========================================================

def add_contact():
    print("\n--- ADD NEW CONTACT ---")
    
    # Name input
    while True:
        name = input("Enter contact name: ").strip()
        if name:
            if name in contacts:
                print(f"⚠️ Contact '{name}' already exists!")
                choice = input("Update instead? (y/n): ").lower()
                if choice == 'y':
                    update_contact(name)
                    return
            break
        print("❌ Name cannot be empty!")

    # Phone input
    while True:
        phone = input("Enter phone number: ").strip()
        valid, cleaned = validate_phone(phone)
        if valid:
            break
        print("❌ Invalid phone number! Enter 10–15 digits.")

    # Email input
    while True:
        email = input("Enter email (optional): ").strip()
        if not email or validate_email(email):
            break
        print("❌ Invalid email format!")

    # Additional fields
    address = input("Enter address (optional): ").strip() or None
    group = input("Enter group (Friends/Family/Work/Other): ").strip() or "Other"

    # Save contact
    contacts[name] = {
        "phone": cleaned,
        "email": email if email else None,
        "address": address,
        "group": group,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    print(f"✅ Contact '{name}' added successfully!")

def search_contact():
    """Search by name or phone (Partial Match)"""
    term = input("\nEnter name or phone to search: ").lower()
    results = {name: data for name, data in contacts.items()
               if term in name.lower() or term in data["phone"]}

    display_search_results(results)

def update_contact(name=None):
    """Update existing contact"""
    if not name:
        name = input("Enter name to update: ").strip()

    if name not in contacts:
        print("❌ Contact not found!")
        return

    print("\n--- UPDATE CONTACT (Leave blank to keep old value) ---")
    old = contacts[name]

    phone = input("New phone: ").strip()
    if phone:
        valid, cleaned = validate_phone(phone)
        if valid:
            old["phone"] = cleaned

    email = input("New email: ").strip()
    if email and validate_email(email):
        old["email"] = email

    address = input("New address: ").strip()
    if address:
        old["address"] = address

    group = input("New group: ").strip()
    if group:
        old["group"] = group

    old["updated_at"] = datetime.now().isoformat()
    print("♻️ Contact updated successfully!")

def delete_contact():
    """Delete a contact with confirmation"""
    name = input("Enter name to delete: ").strip()
    if name in contacts:
        if input("Are you sure? (y/n): ").lower() == "y":
            del contacts[name]
            print("🗑️ Contact deleted!")
    else:
        print("❌ Contact not found!")


# =========================================================
# STEP 4: FILE OPERATIONS (JSON + CSV + BACKUP)
# =========================================================

def save_to_file():
    with open("contacts.json", "w") as f:
        json.dump(contacts, f, indent=4)
    print("💾 Contacts saved to contacts.json")

def load_from_file():
    global contacts
    try:
        with open("contacts.json", "r") as f:
            contacts = json.load(f)
            print("📂 Contacts loaded successfully!")
    except FileNotFoundError:
        print("⚠️ No file found. Starting fresh...")

def backup_contacts():
    filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(contacts, f, indent=4)
    print(f"🗄️ Backup saved as {filename}")

def export_to_csv():
    with open("contacts.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone", "Email", "Address", "Group"])
        for name, info in contacts.items():
            writer.writerow([name, info["phone"], info["email"], info["address"], info["group"]])
    print("📤 Exported to contacts.csv!")


# =========================================================
# STEP 5 & 6: DISPLAY, UI & STATISTICS
# =========================================================

def display_search_results(results):
    """Formatted display of search results"""
    if not results:
        print("❌ No contacts found.")
        return

    print(f"\n🔍 Found {len(results)} contact(s):")
    print("-" * 50)

    for i, (name, info) in enumerate(results.items(), 1):
        print(f"\n{i}. {name}")
        print(f"   📞 Phone   : {info['phone']}")
        print(f"   📧 Email   : {info['email'] or 'None'}")
        print(f"   📍 Address : {info['address'] or 'None'}")
        print(f"   👥 Group   : {info['group']}")
        print("-" * 50)

def display_all():
    if not contacts:
        print("📭 No contacts available.")
        return
    print("\n📒 ALL CONTACTS:")
    for name, info in contacts.items():
        print(f"- {name} → {info['phone']} ({info['group']})")

def statistics():
    print("\n📊 Contact Statistics:")
    print(f"Total Contacts: {len(contacts)}")

    groups = {}
    for info in contacts.values():
        g = info["group"]
        groups[g] = groups.get(g, 0) + 1

    print("\n🔹 Group Count:")
    for g, c in groups.items():
        print(f"   {g}: {c}")


# =========================================================
# STEP 7: MAIN MENU
# =========================================================

def main_menu():
    load_from_file()
    
    while True:
        print("""
========== CONTACT MANAGER ==========
1. Add Contact
2. Search Contact
3. Update Contact
4. Delete Contact
5. Display All Contacts
6. Save to File
7. Export to CSV
8. Backup Data
9. Statistics
10. Exit
=====================================
""")

        choice = input("Choose (1-10): ").strip()

        if choice == "1": add_contact()
        elif choice == "2": search_contact()
        elif choice == "3": update_contact()
        elif choice == "4": delete_contact()
        elif choice == "5": display_all()
        elif choice == "6": save_to_file()
        elif choice == "7": export_to_csv()
        elif choice == "8": backup_contacts()
        elif choice == "9": statistics()
        elif choice == "10":
            save_to_file()
            print("👋 Exiting program... Goodbye!")
            break
        else:
            print("❌ Invalid choice, try again!")

# Run Program
main_menu()
