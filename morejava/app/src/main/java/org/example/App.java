package org.example;

import java.util.Scanner;

public class App {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Enter a string:");
        String userInput = scanner.nextLine();

        String specifiedString = "HelloWorld";

        if (isStringEqual(userInput, specifiedString)) {
            System.out.println("The input matches the specified string.");
        } else {
            System.out.println("The input does not match the specified string.");
        }

        scanner.close();
    }

    public static boolean isStringEqual(String input, String specifiedString) {
        return input.equals(specifiedString);
    }
}
