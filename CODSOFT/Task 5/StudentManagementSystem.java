import java.io.*;
import java.util.ArrayList;

public class StudentManagementSystem {
    private ArrayList<Student> students;
    private final String FILENAME = "students.dat";

    public StudentManagementSystem() {
        this.students = new ArrayList<>();
        loadStudentsFromFile();
    }

    public void addStudent(Student student) {
        if (findStudent(student.getRollNumber()) == null) {
            this.students.add(student);
            System.out.println("Student added successfully.");
        } else {
            System.out.println("Error: Student with roll number " + student.getRollNumber() + " already exists.");
        }
    }

    public void removeStudent(int rollNumber) {
        Student studentToRemove = findStudent(rollNumber);
        if (studentToRemove != null) {
            students.remove(studentToRemove);
            System.out.println("Student removed successfully.");
        } else {
            System.out.println("Error: Student with roll number " + rollNumber + " not found.");
        }
    }

    public Student findStudent(int rollNumber) {
        for (Student student : students) {
            if (student.getRollNumber() == rollNumber) {
                return student;
            }
        }
        return null; 
    }

    public void displayAllStudents() {
        if (students.isEmpty()) {
            System.out.println("No students found in the system.");
        } else {
            System.out.println("\n--- All Students ---");
            for (Student student : students) {
                System.out.println(student);
            }
        }
    }
    
    public void editStudent(int rollNumber, String newName, String newGrade) {
        Student studentToEdit = findStudent(rollNumber);
        if (studentToEdit != null) {
            studentToEdit.setName(newName);
            studentToEdit.setGrade(newGrade);
            System.out.println("Student information updated successfully.");
        } else {
            System.out.println("Error: Student with roll number " + rollNumber + " not found.");
        }
    }

    
    public void saveStudentsToFile() {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(FILENAME))) {
            oos.writeObject(students);
            System.out.println("Student data saved to " + FILENAME);
        } catch (IOException e) {
            System.out.println("Error saving student data: " + e.getMessage());
        }
    }

   
    private void loadStudentsFromFile() {
        File file = new File(FILENAME);
        if (file.exists()) {
            try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(file))) {
                students = (ArrayList<Student>) ois.readObject();
                System.out.println("Student data loaded from " + FILENAME);
            } catch (IOException | ClassNotFoundException e) {
                System.out.println("Error loading student data: " + e.getMessage());
            }
        }
    }
}