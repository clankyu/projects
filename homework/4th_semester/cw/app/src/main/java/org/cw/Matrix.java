package org.cw;

public class Matrix {
    public static int[][] enumeratedMat3() {
        int[][] mat = new int[3][3];
        int sum = 1;

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                mat[i][j] = sum;
                sum++;
            }
        }

        return mat;
    }

    public static int matSum(int[][] mat) {
        int sum = 0;

        for (int i = 0; i < mat.length; i++) {
            for (int j = 0; j < mat.length; j++) {
                sum += mat[i][j];
            }
        }

        return sum;
    }

    public static void test() {
        int[][] mat = enumeratedMat3();
        int mat_sum = matSum(mat);

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (j % 3 == 0) {
                    System.out.println();
                }

                System.out.print(mat[i][j] + " ");
            }
        }

        System.out.println();
        System.out.println("mat_sum: " + mat_sum);
    }
}
