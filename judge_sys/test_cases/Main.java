import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        for (int i = 0; i < 4; i++) {
            int l = scanner.nextInt();
            int ans = 2 * l + 1;
            System.out.println(ans);
        }
        
        scanner.close();
    }
}

