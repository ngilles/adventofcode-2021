use itertools::izip;
use std::fs::File;
use std::io::BufRead;
use std::io::BufReader;

use recap::Recap;
use serde::Deserialize;

fn read_integers<R: BufRead>(reader: R) -> Vec<i32> {
    let numbers: Vec<i32> = reader
        .lines()
        .map(|line| line.unwrap().parse::<i32>().unwrap())
        .collect();
    return numbers;
}

fn depth_counter(data: &Vec<i32>, window_size: usize) -> i32 {
    let windowed: Vec<i32> = data.windows(window_size).map(|e| e.iter().sum()).collect();
    return izip!(&windowed, &windowed[1..]).map(|(a, b)| if a < b {1} else {0}).sum();
}

fn day1_part1(data: &Vec<i32>) -> i32 {
    return depth_counter(data, 1);
}

fn day1_part2(data: &Vec<i32>) -> i32 {
    return depth_counter(data, 3);
}

fn day1() -> std::io::Result<()> {
    let file = File::open("inputs/day-1-input.txt")?;
    let reader = BufReader::new(file);
    let data = read_integers(reader);

    println!("day 1 part 1 = {}", day1_part1(&data));
    println!("day 2 part 2 = {}", day1_part2(&data));
    Ok(())
}

#[derive(Debug, Deserialize, Recap)]
#[recap(regex=r"(?P<direction>.*) (?P<count>\d+)")]
struct SubmarineControl {
    direction: String,
    count: i32,
}

#[derive(Debug)]
struct Position {
    horizontal: i32,
    depth: i32,
    aim: i32,
}

fn day2() -> std::io::Result<()> {
    let file = File::open("inputs/day-2-example.txt")?;
    let file = File::open("inputs/day-2-input.txt")?;
    let reader = BufReader::new(file);
    let commands: Vec<SubmarineControl> = reader.lines().map(|l| {
        return l.unwrap().parse().unwrap();
     }
    ).collect();

    let position: Position = commands.iter().fold(
        Position {horizontal:0, depth: 0, aim: 0},
        |acc, c| {
            match c.direction.as_ref() {
                "forward" => Position { horizontal: acc.horizontal + c.count, depth: acc.depth + acc.aim * c.count, aim: acc.aim},
                "up" => Position { horizontal: acc.horizontal, depth: acc.depth, aim: acc.aim - c.count},
                "down" => Position { horizontal: acc.horizontal, depth: acc.depth, aim: acc.aim + c.count},
                _ => acc,
            }
    });

    println!("{}", position.horizontal * position.depth);
    Ok(())
}

fn main() -> std::io::Result<()> {
    day1()?;
    day2()?;
    Ok(())
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn day1_example_part1() {
        let input = vec![199, 200, 208, 210, 200, 207, 240, 269, 260, 263];
        assert_eq!(day1_part1(&input), 7);
    }

    #[test]
    fn day1_example_part2() {
        let input = vec![199, 200, 208, 210, 200, 207, 240, 269, 260, 263];
        assert_eq!(day1_part2(&input), 5);
    }
}
