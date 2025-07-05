import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import json
import os
from abc import ABC, abstractmethod

class Pet(ABC):
    """Abstract base class for all pets"""
    def __init__(self, name, age, breed="Unknown"):
        self.name = name
        self.age = age
        self.breed = breed
        self.care_schedule = []
        self.health_records = []
    
    @abstractmethod
    def get_care_requirements(self):
        """Abstract method to get specific care requirements for each pet type"""
        pass
    
    @abstractmethod
    def get_sound(self):
        """Abstract method to get the sound the pet makes"""
        pass
    
    def add_care_task(self, task, frequency_days, last_done=None):
        """Add a care task to the pet's schedule"""
        if last_done is None:
            last_done = datetime.now().strftime("%Y-%m-%d")
        
        self.care_schedule.append({
            'task': task,
            'frequency_days': frequency_days,
            'last_done': last_done
        })
    
    def add_health_record(self, record_type, description, date=None):
        """Add a health record for the pet"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        self.health_records.append({
            'type': record_type,
            'description': description,
            'date': date
        })
    
    def get_overdue_tasks(self):
        """Get tasks that are overdue"""
        overdue = []
        current_date = datetime.now()
        
        for task in self.care_schedule:
            last_done = datetime.strptime(task['last_done'], "%Y-%m-%d")
            days_since = (current_date - last_done).days
            
            if days_since >= task['frequency_days']:
                overdue.append({
                    'task': task['task'],
                    'days_overdue': days_since - task['frequency_days'] + 1
                })
        
        return overdue
    
    def to_dict(self):
        """Convert pet object to dictionary for JSON serialization"""
        return {
            'type': self.__class__.__name__,
            'name': self.name,
            'age': self.age,
            'breed': self.breed,
            'care_schedule': self.care_schedule,
            'health_records': self.health_records
        }

class Dog(Pet):
    """Dog class inheriting from Pet"""
    def __init__(self, name, age, breed="Mixed", size="Medium"):
        super().__init__(name, age, breed)
        self.size = size
        # Default care tasks for dogs
        self.add_care_task("Walk", 1)
        self.add_care_task("Feed", 1)
        self.add_care_task("Bath", 7)
        self.add_care_task("Vet Checkup", 90)
    
    def get_care_requirements(self):
        return f"Dogs need daily walks, feeding, weekly baths, and regular vet checkups. Size: {self.size}"
    
    def get_sound(self):
        return "Woof! 🐕"
    
    def to_dict(self):
        data = super().to_dict()
        data['size'] = self.size
        return data

class Cat(Pet):
    """Cat class inheriting from Pet"""
    def __init__(self, name, age, breed="Mixed", indoor=True):
        super().__init__(name, age, breed)
        self.indoor = indoor
        # Default care tasks for cats
        self.add_care_task("Feed", 1)
        self.add_care_task("Litter Box Clean", 2)
        self.add_care_task("Brush", 3)
        self.add_care_task("Vet Checkup", 90)
    
    def get_care_requirements(self):
        location = "Indoor" if self.indoor else "Outdoor"
        return f"Cats need daily feeding, litter maintenance, brushing, and vet checkups. Type: {location}"
    
    def get_sound(self):
        return "Meow! 🐱"
    
    def to_dict(self):
        data = super().to_dict()
        data['indoor'] = self.indoor
        return data

class Bird(Pet):
    """Bird class inheriting from Pet"""
    def __init__(self, name, age, breed="Unknown", can_fly=True):
        super().__init__(name, age, breed)
        self.can_fly = can_fly
        # Default care tasks for birds
        self.add_care_task("Feed", 1)
        self.add_care_task("Cage Clean", 3)
        self.add_care_task("Wing Trim", 60)
        self.add_care_task("Vet Checkup", 180)
    
    def get_care_requirements(self):
        flight = "Can fly" if self.can_fly else "Cannot fly"
        return f"Birds need daily feeding, cage cleaning, wing care, and vet checkups. Status: {flight}"
    
    def get_sound(self):
        return "Tweet! 🐦"
    
    def to_dict(self):
        data = super().to_dict()
        data['can_fly'] = self.can_fly
        return data

class PetCareManager:
    """Main manager class for handling all pets and data persistence"""
    def __init__(self):
        self.pets = []
        self.data_file = "data/pets_data.json"
        self.ensure_data_directory()
        self.load_data()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists("data"):
            os.makedirs("data")
    
    def add_pet(self, pet):
        """Add a new pet to the manager"""
        self.pets.append(pet)
        self.save_data()
    
    def remove_pet(self, pet_name):
        """Remove a pet by name"""
        self.pets = [pet for pet in self.pets if pet.name != pet_name]
        self.save_data()
    
    def get_pet_by_name(self, name):
        """Get a pet by name"""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None
    
    def get_all_overdue_tasks(self):
        """Get all overdue tasks from all pets"""
        all_overdue = []
        for pet in self.pets:
            overdue = pet.get_overdue_tasks()
            for task in overdue:
                all_overdue.append({
                    'pet_name': pet.name,
                    'task': task['task'],
                    'days_overdue': task['days_overdue']
                })
        return all_overdue
    
    def save_data(self):
        """Save all pets data to JSON file"""
        try:
            data = [pet.to_dict() for pet in self.pets]
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        """Load pets data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                for pet_data in data:
                    pet = self.create_pet_from_data(pet_data)
                    if pet:
                        self.pets.append(pet)
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def create_pet_from_data(self, data):
        """Create a pet object from dictionary data"""
        try:
            pet_type = data['type']
            name = data['name']
            age = data['age']
            breed = data['breed']
            
            if pet_type == 'Dog':
                size = data.get('size', 'Medium')
                pet = Dog(name, age, breed, size)
            elif pet_type == 'Cat':
                indoor = data.get('indoor', True)
                pet = Cat(name, age, breed, indoor)
            elif pet_type == 'Bird':
                can_fly = data.get('can_fly', True)
                pet = Bird(name, age, breed, can_fly)
            else:
                return None
            
            # Load care schedule and health records
            pet.care_schedule = data.get('care_schedule', [])
            pet.health_records = data.get('health_records', [])
            
            return pet
        except Exception as e:
            print(f"Error creating pet from data: {e}")
            return None

class PetCareGUI:
    """GUI class for the Pet Care Management System"""
    def __init__(self, root):
        self.root = root
        self.root.title("Pet Care Management System")
        self.root.geometry("800x600")
        
        self.manager = PetCareManager()
        
        self.create_widgets()
        self.refresh_pet_list()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🐾 Pet Care Management System 🐾", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Pet list frame
        pet_frame = ttk.LabelFrame(main_frame, text="My Pets", padding="10")
        pet_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Pet listbox
        self.pet_listbox = tk.Listbox(pet_frame, height=10)
        self.pet_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.pet_listbox.bind('<<ListboxSelect>>', self.on_pet_select)
        
        # Pet buttons
        pet_buttons_frame = ttk.Frame(pet_frame)
        pet_buttons_frame.grid(row=1, column=0, pady=5)
        
        ttk.Button(pet_buttons_frame, text="Add Pet", 
                  command=self.add_pet_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(pet_buttons_frame, text="Remove Pet", 
                  command=self.remove_pet).pack(side=tk.LEFT, padx=2)
        ttk.Button(pet_buttons_frame, text="Pet Details", 
                  command=self.show_pet_details).pack(side=tk.LEFT, padx=2)
        
        # Care tasks frame
        care_frame = ttk.LabelFrame(main_frame, text="Care Tasks", padding="10")
        care_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Tasks text area
        self.tasks_text = tk.Text(care_frame, height=15, width=40)
        self.tasks_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Task buttons
        task_buttons_frame = ttk.Frame(care_frame)
        task_buttons_frame.grid(row=1, column=0, pady=5)
        
        ttk.Button(task_buttons_frame, text="Mark Task Done", 
                  command=self.mark_task_done).pack(side=tk.LEFT, padx=2)
        ttk.Button(task_buttons_frame, text="Add Task", 
                  command=self.add_task_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(task_buttons_frame, text="Health Record", 
                  command=self.add_health_record_dialog).pack(side=tk.LEFT, padx=2)
        
        # Overdue tasks frame
        overdue_frame = ttk.LabelFrame(main_frame, text="⚠️ Overdue Tasks", padding="10")
        overdue_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.overdue_text = tk.Text(overdue_frame, height=4)
        self.overdue_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Refresh button
        ttk.Button(main_frame, text="Refresh All", 
                  command=self.refresh_all).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        pet_frame.columnconfigure(0, weight=1)
        pet_frame.rowconfigure(0, weight=1)
        care_frame.columnconfigure(0, weight=1)
        care_frame.rowconfigure(0, weight=1)
        overdue_frame.columnconfigure(0, weight=1)
    
    def refresh_pet_list(self):
        """Refresh the pet list display"""
        self.pet_listbox.delete(0, tk.END)
        for pet in self.manager.pets:
            self.pet_listbox.insert(tk.END, f"{pet.name} ({pet.__class__.__name__}) - {pet.get_sound()}")
    
    def refresh_all(self):
        """Refresh all displays"""
        self.refresh_pet_list()
        self.refresh_overdue_tasks()
        self.refresh_care_tasks()
    
    def refresh_overdue_tasks(self):
        """Refresh overdue tasks display"""
        self.overdue_text.delete(1.0, tk.END)
        overdue_tasks = self.manager.get_all_overdue_tasks()
        
        if not overdue_tasks:
            self.overdue_text.insert(tk.END, "No overdue tasks! Great job taking care of your pets! 🎉")
        else:
            for task in overdue_tasks:
                self.overdue_text.insert(tk.END, 
                    f"🚨 {task['pet_name']}: {task['task']} (overdue by {task['days_overdue']} days)\n")
    
    def refresh_care_tasks(self):
        """Refresh care tasks for selected pet"""
        selection = self.pet_listbox.curselection()
        if not selection:
            self.tasks_text.delete(1.0, tk.END)
            return
        
        pet_index = selection[0]
        pet = self.manager.pets[pet_index]
        
        self.tasks_text.delete(1.0, tk.END)
        self.tasks_text.insert(tk.END, f"Care Tasks for {pet.name}:\n")
        self.tasks_text.insert(tk.END, f"Care Requirements: {pet.get_care_requirements()}\n\n")
        
        for i, task in enumerate(pet.care_schedule):
            last_done = datetime.strptime(task['last_done'], "%Y-%m-%d")
            days_since = (datetime.now() - last_done).days
            status = "✅ Done" if days_since < task['frequency_days'] else "❌ Overdue"
            
            self.tasks_text.insert(tk.END, 
                f"{i+1}. {task['task']} (every {task['frequency_days']} days) - {status}\n")
            self.tasks_text.insert(tk.END, f"   Last done: {task['last_done']} ({days_since} days ago)\n\n")
        
        # Health records
        if pet.health_records:
            self.tasks_text.insert(tk.END, "\n--- Health Records ---\n")
            for record in pet.health_records[-3:]:  # Show last 3 records
                self.tasks_text.insert(tk.END, 
                    f"📋 {record['date']}: {record['type']} - {record['description']}\n")
    
    def on_pet_select(self, event):
        """Handle pet selection"""
        self.refresh_care_tasks()
    
    def add_pet_dialog(self):
        """Show add pet dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Pet")
        dialog.geometry("400x300")
        
        # Pet type
        ttk.Label(dialog, text="Pet Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        pet_type = ttk.Combobox(dialog, values=["Dog", "Cat", "Bird"])
        pet_type.grid(row=0, column=1, padx=5, pady=5)
        pet_type.set("Dog")
        
        # Name
        ttk.Label(dialog, text="Name:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Age
        ttk.Label(dialog, text="Age:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        age_entry = ttk.Entry(dialog)
        age_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Breed
        ttk.Label(dialog, text="Breed:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        breed_entry = ttk.Entry(dialog)
        breed_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Extra field frame
        extra_frame = ttk.Frame(dialog)
        extra_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
        # Extra field (changes based on pet type)
        extra_label = ttk.Label(extra_frame, text="Size:")
        extra_label.grid(row=0, column=0, sticky=tk.W)
        extra_entry = ttk.Combobox(extra_frame, values=["Small", "Medium", "Large"])
        extra_entry.grid(row=0, column=1, padx=5)
        extra_entry.set("Medium")
        
        def update_extra_field():
            selected_type = pet_type.get()
            if selected_type == "Dog":
                extra_label.config(text="Size:")
                extra_entry.config(values=["Small", "Medium", "Large"])
                extra_entry.set("Medium")
            elif selected_type == "Cat":
                extra_label.config(text="Location:")
                extra_entry.config(values=["Indoor", "Outdoor"])
                extra_entry.set("Indoor")
            elif selected_type == "Bird":
                extra_label.config(text="Flight Status:")
                extra_entry.config(values=["Can fly", "Cannot fly"])
                extra_entry.set("Can fly")
        
        pet_type.bind('<<ComboboxSelected>>', lambda e: update_extra_field())
        
        def save_pet():
            try:
                name = name_entry.get().strip()
                age = int(age_entry.get())
                breed = breed_entry.get().strip() or "Unknown"
                
                if not name:
                    messagebox.showerror("Error", "Please enter a name")
                    return
                
                selected_type = pet_type.get()
                extra_value = extra_entry.get()
                
                if selected_type == "Dog":
                    pet = Dog(name, age, breed, extra_value)
                elif selected_type == "Cat":
                    indoor = extra_value == "Indoor"
                    pet = Cat(name, age, breed, indoor)
                elif selected_type == "Bird":
                    can_fly = extra_value == "Can fly"
                    pet = Bird(name, age, breed, can_fly)
                
                self.manager.add_pet(pet)
                self.refresh_all()
                dialog.destroy()
                messagebox.showinfo("Success", f"{name} has been added to your pets!")
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid age")
            except Exception as e:
                messagebox.showerror("Error", f"Error adding pet: {e}")
        
        ttk.Button(dialog, text="Add Pet", command=save_pet).grid(row=5, column=0, columnspan=2, pady=10)
    
    def remove_pet(self):
        """Remove selected pet"""
        selection = self.pet_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a pet to remove")
            return
        
        pet_index = selection[0]
        pet = self.manager.pets[pet_index]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove {pet.name}?"):
            self.manager.remove_pet(pet.name)
            self.refresh_all()
            messagebox.showinfo("Success", f"{pet.name} has been removed")
    
    def show_pet_details(self):
        """Show detailed information about selected pet"""
        selection = self.pet_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a pet to view details")
            return
        
        pet_index = selection[0]
        pet = self.manager.pets[pet_index]
        
        details = f"Name: {pet.name}\n"
        details += f"Type: {pet.__class__.__name__}\n"
        details += f"Age: {pet.age}\n"
        details += f"Breed: {pet.breed}\n"
        details += f"Sound: {pet.get_sound()}\n"
        details += f"Care Requirements: {pet.get_care_requirements()}\n"
        
        messagebox.showinfo(f"Details for {pet.name}", details)
    
    def mark_task_done(self):
        """Mark a task as done"""
        selection = self.pet_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a pet first")
            return
        
        pet_index = selection[0]
        pet = self.manager.pets[pet_index]
        
        if not pet.care_schedule:
            messagebox.showinfo("Info", "No tasks available for this pet")
            return
        
        # Create task selection dialog
        task_dialog = tk.Toplevel(self.root)
        task_dialog.title("Mark Task as Done")
        task_dialog.geometry("300x200")
        
        ttk.Label(task_dialog, text="Select task to mark as done:").pack(pady=10)
        
        task_listbox = tk.Listbox(task_dialog)
        task_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        for i, task in enumerate(pet.care_schedule):
            task_listbox.insert(tk.END, f"{task['task']} (every {task['frequency_days']} days)")
        
        def mark_done():
            task_selection = task_listbox.curselection()
            if not task_selection:
                messagebox.showwarning("Warning", "Please select a task")
                return
            
            task_index = task_selection[0]
            pet.care_schedule[task_index]['last_done'] = datetime.now().strftime("%Y-%m-%d")
            self.manager.save_data()
            self.refresh_all()
            task_dialog.destroy()
            messagebox.showinfo("Success", "Task marked as done!")
        
        ttk.Button(task_dialog, text="Mark Done", command=mark_done).pack(pady=10)
    
    def add_task_dialog(self):
        """Add a new care task"""
        selection = self.pet_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a pet first")
            return
        
        pet_index = selection[0]
        pet = self.manager.pets[pet_index]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Care Task")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="Task Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        task_entry = ttk.Entry(dialog)
        task_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Frequency (days):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        freq_entry = ttk.Entry(dialog)
        freq_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def save_task():
            try:
                task = task_entry.get().strip()
                frequency = int(freq_entry.get())
                
                if not task:
                    messagebox.showerror("Error", "Please enter a task name")
                    return
                
                pet.add_care_task(task, frequency)
                self.manager.save_data()
                self.refresh_all()
                dialog.destroy()
                messagebox.showinfo("Success", f"Task '{task}' added successfully!")
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid frequency")
        
        ttk.Button(dialog, text="Add Task", command=save_task).grid(row=2, column=0, columnspan=2, pady=10)
    
    def add_health_record_dialog(self):
        """Add a health record"""
        selection = self.pet_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a pet first")
            return
        
        pet_index = selection[0]
        pet = self.manager.pets[pet_index]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Health Record")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Record Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        type_combo = ttk.Combobox(dialog, values=["Vaccination", "Checkup", "Treatment", "Medication", "Other"])
        type_combo.grid(row=0, column=1, padx=5, pady=5)
        type_combo.set("Checkup")
        
        ttk.Label(dialog, text="Description:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        desc_text = tk.Text(dialog, height=5, width=30)
        desc_text.grid(row=1, column=1, padx=5, pady=5)
        
        def save_record():
            record_type = type_combo.get()
            description = desc_text.get(1.0, tk.END).strip()
            
            if not description:
                messagebox.showerror("Error", "Please enter a description")
                return
            
            pet.add_health_record(record_type, description)
            self.manager.save_data()
            self.refresh_all()
            dialog.destroy()
            messagebox.showinfo("Success", "Health record added successfully!")
        
        ttk.Button(dialog, text="Add Record", command=save_record).grid(row=2, column=0, columnspan=2, pady=10)

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = PetCareGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()