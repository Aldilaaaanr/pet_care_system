# Pet Care Management System 🐾

## Inspiration

This application was inspired by my personal experience of taking care of multiple pets and often forgetting their care schedules. As a pet owner, I found myself constantly worried about whether I had fed my cats, when was the last time I walked my dog, or when their next vet appointment should be. I realized that many pet owners face similar challenges in keeping track of their pets' needs, especially when they have multiple pets with different care requirements.

The idea came to me when I almost missed my cat's vaccination appointment and realized I hadn't been keeping proper track of my pets' health records. I wanted to create a simple but effective system that would help pet owners like me stay organized and ensure their furry friends get the best care possible.

## Features

- **Multi-pet Management**: Add and manage different types of pets (Dogs, Cats, Birds)
- **Care Task Tracking**: Keep track of daily tasks like feeding, walking, grooming
- **Health Records**: Maintain a digital health record for each pet
- **Overdue Task Alerts**: Get notified when tasks are overdue
- **Data Persistence**: All data is saved automatically to JSON files
- **User-friendly GUI**: Easy-to-use interface built with tkinter

## Installation & Setup

1. Make sure you have Python 3.6+ installed
2. Clone or download this repository
3. No additional packages required (uses only built-in Python libraries)

## How to Run

1. Navigate to the project directory
2. Run the application:
   ```bash
   python main.py
   ```

## Usage Guide

### Adding a Pet
1. Click "Add Pet" button
2. Select pet type (Dog, Cat, or Bird)
3. Fill in pet details (name, age, breed)
4. Set specific attributes (size for dogs, indoor/outdoor for cats, flight status for birds)
5. Click "Add Pet" to save

### Managing Care Tasks
1. Select a pet from the list
2. View their care schedule in the right panel
3. Mark tasks as done when completed
4. Add custom care tasks as needed
5. Monitor overdue tasks in the bottom panel

### Health Records
1. Select a pet
2. Click "Health Record" button
3. Choose record type (Vaccination, Checkup, Treatment, etc.)
4. Add description and save

### Features Overview
- **Green checkmarks (✅)**: Tasks completed on time
- **Red X marks (❌)**: Overdue tasks that need attention
- **Pet sounds**: Each pet type makes their characteristic sound
- **Auto-save**: All changes are automatically saved to JSON files

## Project Structure

```
pet_care_system/
├── main.py                 # Main application file
├── data/
│   └── pets_data.json     # Pet data storage (created automatically)
├── README.md              # This file
└── demo.mp4               # Video demonstration
```

## Data Storage

The application uses JSON files to store pet data persistently. The data includes:
- Pet information (name, age, breed, type-specific attributes)
- Care schedules with frequencies and last completion dates
- Health records with dates and descriptions

## Sample Data

The application comes with default care tasks for each pet type:
- **Dogs**: Daily walks, feeding, weekly baths, quarterly vet checkups
- **Cats**: Daily feeding, bi-daily litter cleaning, tri-daily brushing, quarterly vet checkups
- **Birds**: Daily feeding, tri-daily cage cleaning, monthly wing care, bi-annual vet checkups

## Video Demo

A video demonstration of the application is available at: [demo.mp4](demo.mp4)

The demo shows:
- Adding different types of pets
- Managing care tasks
- Viewing overdue tasks
- Adding health records
- Data persistence across sessions

## License

This project is created for educational purposes as part of a Python OOP assignment.

---

*Created with ❤️ for pet lovers who want to keep their furry friends happy and healthy!*