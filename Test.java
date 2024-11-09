import java.util.*;

public class Test {
    public static void main(String[] args) {
        System.out.println("Try programiz.pro");

        Queue<String> myQ = new LinkedList<>();
        myQ.add("hey");
        myQ.add("bye");
        myQ.add("car");
        System.out.println(myQ);
        myQ.poll();
        System.out.println(myQ);

        System.out.println("STACK");


        Deque<String> myS = new ArrayDeque<>();
        myS.addFirst(e);
        myS.push("hey");
        myS.push("bye");
        myS.push("car");
        System.out.println(myS);
        myS.pop();
        System.out.println(myS);
    }
}
