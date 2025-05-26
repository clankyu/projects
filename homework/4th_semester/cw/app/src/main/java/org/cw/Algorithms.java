package org.cw;

public class Algorithms {
    public static int binarySearch(int target, int[] arr) {
        int high = arr.length - 1;
        int mid = arr.length / 2;
        int low = 0;

        while (low <= high) {
            if (arr[mid] == target) {
                return mid;
            }
            if (arr[mid] < target) {
                low = mid + 1;
                mid = low + (high - low) / 2;
            } else {
                high = mid - 1;
                mid /= 2;
            }
        }


        return -1;
    }

    public static int[] bubbleSort(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            for (int j = 0; j < arr.length - 1 - i; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }

        return arr;
    }
}
