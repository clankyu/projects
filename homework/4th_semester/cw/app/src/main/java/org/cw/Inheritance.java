package org.cw;

public class Inheritance {
    public class Entity {
        public String name;
        public String weapon;
        public int hp;
        public int stength;
        public int dexterity;
        public int intelligence;

        public void attack() {
            System.out.println(name + " is attacking.");
        }
        public void info() {
            System.out.println(name + " info:");
            System.out.println("Weapon: " + weapon);
            System.out.println("HP: " + hp);
            System.out.println("Strength: " + strength);
            System.out.println("Dexterity: " + dexterity);
            System.out.println("Intelligence: " + intelligence);
        }
    }

    public class Skeleton extends Entity {
        @Override
        public void attack() {
            System.out.println(name + " is shooting arrows.");
        }
    }
}
