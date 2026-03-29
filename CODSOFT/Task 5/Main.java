import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        StudentManagementSystem sms = new StudentManagementSystem();
        int choice;

        do {
            System.out.println("\n--- Student Management System Menu ---");
            System.out.println("1. Add a new student");
            System.out.println("2. Remove a student");
            System.out.println("3. Search for a student");
            System.out.println("4. Display all students");
            System.out.println("5. Edit student information");
            System.out.println("6. Exit");
            System.out.print("Enter your choice: ");

            try {
                choice = scanner.nextInt();
                scanner.nextLine();

                switch (choice) {
                    case 1:
                        addStudent(scanner, sms);
                        break;
                    case 2:
                        removeStudent(scanner, sms);
                        break;
                    case 3:
                        searchStudent(scanner, sms);
                        break;
                    case 4:
                        sms.displayAllStudents();
                        break;
                    case 5:
                        editStudent(scanner, sms);
                        break;
                    case 6:
                        sms.saveStudentsToFile();
                        System.out.println("Exiting the application. Goodbye!");
                        break;
                    default:
                        System.out.println("Invalid choice. Please enter a number between 1 and 6.");
                }
            } catch (java.util.InputMismatchException e) {
                System.out.println("Invalid input. Please enter a number.");
                scanner.nextLine(); 
                choice = 0; 
            }

        } while (choice != 6);

        scanner.close();
    }

    private static void addStudent(Scanner scanner, StudentManagementSystem sms) {
        System.out.print("Enter student name: ");
        String name = scanner.nextLine().trim();
        if (name.isEmpty()) {
            System.out.println("Name cannot be empty.");
            return;
        }

        System.out.print("Enter student roll number: ");
        int rollNumber = scanner.nextInt();
        scanner.nextLine(); 

        System.out.print("Enter student grade: ");
        String grade = scanner.nextLine().trim();
        if (grade.isEmpty()) {
            System.out.println("Grade cannot be empty.");
            return;
        }

        Student newStudent = new Student(name, rollNumber, grade);
        sms.addStudent(newStudent);
    }

    private static void removeStudent(Scanner scanner, StudentManagementSystem sms) {
        System.out.print("Enter roll number of student to remove: ");
        int rollNumber = scanner.nextInt();
        sms.removeStudent(rollNumber);
    }

    private static void searchStudent(Scanner scanner, StudentManagementSystem sms) {
        System.out.print("Enter roll number of student to search: ");
        int rollNumber = scanner.nextInt();
        Student foundStudent = sms.findStudent(rollNumber);
        if (foundStudent != null) {
            System.out.println("Student found: " + foundStudent);
        } else {
            System.out.println("Student with roll number " + rollNumber + " not found.");
        }
    }
    
    private static void editStudent(Scanner scanner, StudentManagementSystem sms) {
        System.out.print("Enter roll number of student to edit: ");
        int rollNumber = scanner.nextInt();
        scanner.nextLine();
        
        Student studentToEdit = sms.findStudent(rollNumber);
        if (studentToEdit != null) {
            System.out.print("Enter new name (current: " + studentToEdit.getName() + "): ");
            String newName = scanner.nextLine().trim();
            
            System.out.print("Enter new grade (current: " + studentToEdit.getGrade() + "): ");
            String newGrade = scanner.nextLine().trim();
            
            if (newName.isEmpty() || newGrade.isEmpty()) {
                System.out.println("Name and Grade cannot be empty. No changes made.");
            } else {
                sms.editStudent(rollNumber, newName, newGrade);
            }
        } else {
            System.out.println("Student with roll number " + rollNumber + " not found.");
        }
    }
} 
    

