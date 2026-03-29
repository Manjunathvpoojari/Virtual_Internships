import java.util.Scanner;

public class StudentGradeCalculator {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        
        System.out.print("Enter the number of subjects: ");
        int numberOfSubjects = scanner.nextInt();

      
        if (numberOfSubjects <= 0) {
            System.out.println("Invalid number of subjects. Please enter a positive number.");
            return;
        }

        int totalMarks = 0;
        for (int i = 1; i <= numberOfSubjects; i++) {
            System.out.print("Enter marks obtained in subject " + i + " (out of 100): ");
            int marks = scanner.nextInt();

            
            if (marks < 0 || marks > 100) {
                System.out.println("Invalid marks. Marks must be between 0 and 100. Please try again.");
                i--; 
            } else {
                totalMarks += marks;
            }
        }

       
        double averagePercentage = (double) totalMarks / numberOfSubjects;

       
        String grade;
        if (averagePercentage >= 90) {
            grade = "A+";
        } else if (averagePercentage >= 80) {
            grade = "A";
        } else if (averagePercentage >= 70) {
            grade = "B";
        } else if (averagePercentage >= 60) {
            grade = "C";
        } else if (averagePercentage >= 50) {
            grade = "D";
        } else {
            grade = "F";
        }

        System.out.println("\n--- Results ---");
        System.out.println("Total Marks: " + totalMarks + " / " + (numberOfSubjects * 100));
        System.out.printf("Average Percentage: %.2f%%\n", averagePercentage);
        System.out.println("Grade: " + grade);

        scanner.close();
    }
}