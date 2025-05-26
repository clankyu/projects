package org.cw;

import java.util.Scanner;
import java.util.Random;

public class Student {
    public String name;
    public int grade;

    public Student(String name, int grade) {
        this.name = name;
        this.grade = grade;
    }

    public static int studentGrade(Student[] students) {
        Scanner scan = new Scanner(System.in);
        System.out.print("Input a student name: ");
        String name = scan.nextLine();
        System.out.println();

        for (int i = 0; i < students.length; i++) {
            if (students[i].name.equals(name)) {
                System.out.println(students[i].name + "'s grade: " + students[i].grade);
                scan.close();

                return students[i].grade;
            }
        }

        System.out.println("Student not found");
        scan.close();

        return 0;
    }

    public static Student[] studentCW() {
        Student[] s = new Student[10];
        Random rand = new Random();

        for (int i = 0; i < s.length; i++) {
            s[i] = new Student("Juan Pablo" + (i + 1), rand.nextInt(100));
            System.out.println("name: " + s[i].name);
            System.out.println("grade: " + s[i].grade);
        }

        return s;
    }
}
