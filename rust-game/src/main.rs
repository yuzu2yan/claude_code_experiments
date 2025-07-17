use std::io;
use std::cmp::Ordering;
use rand::Rng;
use colored::*;

fn main() {
    println!("{}", "=================================".bright_blue());
    println!("{}", "🎮 数当てゲームへようこそ！🎮".bright_yellow().bold());
    println!("{}", "=================================".bright_blue());
    
    let mut play_again = true;
    let mut total_games = 0;
    let mut total_attempts = 0;
    let mut best_score = u32::MAX;
    
    while play_again {
        total_games += 1;
        println!("\n{}", format!("--- ゲーム {} ---", total_games).bright_cyan());
        
        let attempts = play_game();
        total_attempts += attempts;
        
        if attempts < best_score {
            best_score = attempts;
            println!("{}", "🏆 新記録！🏆".bright_yellow().bold());
        }
        
        println!("\n{}", "もう一度プレイしますか？ (y/n)".green());
        
        let mut play_again_input = String::new();
        io::stdin()
            .read_line(&mut play_again_input)
            .expect("入力の読み込みに失敗しました");
        
        play_again = play_again_input.trim().to_lowercase() == "y";
    }
    
    println!("\n{}", "=== ゲーム統計 ===".bright_magenta().bold());
    println!("総ゲーム数: {}", total_games.to_string().bright_white());
    println!("平均試行回数: {:.1}", (total_attempts as f64 / total_games as f64).to_string().bright_white());
    println!("ベストスコア: {} 回", best_score.to_string().bright_yellow());
    println!("\n{}", "プレイしてくれてありがとう！👋".bright_green().bold());
}

fn play_game() -> u32 {
    let secret_number = rand::thread_rng().gen_range(1..=100);
    let mut attempts = 0;
    
    println!("{}", "1から100までの数を当ててください！".bright_white());
    
    loop {
        attempts += 1;
        println!("\n{}", format!("試行 {}: 予想を入力してください", attempts).cyan());
        
        let mut guess = String::new();
        io::stdin()
            .read_line(&mut guess)
            .expect("入力の読み込みに失敗しました");
        
        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => {
                println!("{}", "❌ 有効な数字を入力してください！".red());
                continue;
            }
        };
        
        if guess < 1 || guess > 100 {
            println!("{}", "⚠️  1から100の間の数を入力してください！".yellow());
            continue;
        }
        
        match guess.cmp(&secret_number) {
            Ordering::Less => {
                println!("{} {}", "📉".red(), "もっと大きい数です！".red());
                give_hint(&secret_number, &guess);
            }
            Ordering::Greater => {
                println!("{} {}", "📈".blue(), "もっと小さい数です！".blue());
                give_hint(&secret_number, &guess);
            }
            Ordering::Equal => {
                println!("{}", "🎉 正解！🎉".bright_green().bold());
                println!("{}", format!("{} 回で当たりました！", attempts).bright_white());
                return attempts;
            }
        }
    }
}

fn give_hint(secret: &u32, guess: &u32) {
    let diff = (*secret as i32 - *guess as i32).abs();
    
    let hint = if diff <= 5 {
        "🔥 とても近い！".bright_red()
    } else if diff <= 10 {
        "♨️  近い！".red()
    } else if diff <= 20 {
        "🌡️  まあまあ近い".yellow()
    } else {
        "❄️  まだ遠い".blue()
    };
    
    println!("{}", hint);
}