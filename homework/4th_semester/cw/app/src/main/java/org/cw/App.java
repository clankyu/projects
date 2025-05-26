package org.cw;

import java.util.Random;

public class App {
    public static void main(String[] args) {
        int[] list = new int[] {3, 4, 4, 5, 8, 9, 9, 10, 12, 20, 200, 300};
        for (int i = 0; i < list.length; i++) {
            int index = Algorithms.binarySearch(list[i], list);
            System.out.println("target = " + list[i] + " | index = " + index);
        }
        for (int i : list) {
            System.out.print(i + ", ");
        }
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
