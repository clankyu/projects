use std::io::Write;

fn main() {
    loop {
        // let mut stdout = std::io::stdout();
        // stdout.write_all(b">> Please enter a valid number: ").unwrap();
        println!(">> Please enter a valid number: ");

        let mut input = String::new();
        std::io::stdin().read_line(&mut input).unwrap();

        let mut num: f64 = match input.trim().parse() {
            Ok(num) => num,
            Err(_) => continue
        };
        let mut count = 0;

        while num >= 10.0 {
            num /= 10.0;
            count += 1;
        }
        while num < 1.0 {
            num *= 10.0;
            count -= 1;
        }

        let result = format!("{num}e{count}");
        println!(">> Result: {result}");
    }
}
