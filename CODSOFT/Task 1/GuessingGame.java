import java.util.Random;
import java.util.Scanner;

public class GuessingGame {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();
        boolean playAgain = true;
        int totalScore = 0;

        while (playAgain) {
            int numberToGuess = random.nextInt(100) + 1; 
            int numberOfAttempts = 0;
            final int maxAttempts = 7;
            boolean hasGuessedCorrectly = false;

            System.out.println("Welcome to the Number Guessing Game!");
            System.out.println("I've generated a number between 1 and 100. You have " + maxAttempts + " attempts to guess it.");
            
            while (numberOfAttempts < maxAttempts && !hasGuessedCorrectly) {
                System.out.print("Enter your guess: ");
                try {
                    int userGuess = scanner.nextInt();
                    numberOfAttempts++;

                    if (userGuess == numberToGuess) {
                        System.out.println("Congratulations! You've guessed the correct number!");
                        System.out.println("It took you " + numberOfAttempts + " attempts.");
                        totalScore += (maxAttempts - numberOfAttempts + 1);
                        hasGuessedCorrectly = true;
                    } else if (userGuess < numberToGuess) {
                        System.out.println("Your guess is too low.");
                    } else {
                        System.out.println("Your guess is too high.");
                    }
                } catch (java.util.InputMismatchException e) {
                    System.out.println("Invalid input. Please enter a valid number.");
                    scanner.nextLine(); 
                }
            }

            if (!hasGuessedCorrectly) {
                System.out.println("Sorry, you've run out of attempts. The correct number was " + numberToGuess + ".");
            }

            System.out.println("\nYour current score is: " + totalScore);
            System.out.print("Do you want to play another round? (yes/no): ");
            String playAgainResponse = scanner.next().toLowerCase();
            if (!playAgainResponse.equals("yes")) {
                playAgain = false;
                System.out.println("Thanks for playing! Your final score is: " + totalScore);
            }
        }
        scanner.close();
    }
}