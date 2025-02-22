# Kelly Criterion strategy

import random
import matplotlib.pyplot as plt

def kelly_criterion(bankroll, win_probability, multiplier):
    edge = (win_probability * (multiplier - 1)) - (1 - win_probability)
    return max(0, edge / (multiplier - 1)) * bankroll  # Kelly fraction of bankroll

def simulate_betting(strategy, initial_bankroll=1000, bet_size=10, rounds=100, win_probability=0.5, multiplier=1.8):
    bankroll = initial_bankroll
    bankroll_history = [bankroll]
    bet = bet_size
    
    for _ in range(rounds):
        win = random.random() < win_probability  # Simulate win/loss
        
        if strategy == 'kelly':
            bet = min(bankroll, kelly_criterion(bankroll, win_probability, multiplier))
        
        if win:
            bankroll += bet * (multiplier - 1)
            if strategy == 'martingale':
                bet = bet_size  # Reset to initial bet
            elif strategy == 'anti-martingale':
                bet = min(bankroll, bet * 2)  # Double bet on win
        else:
            bankroll -= bet
            if strategy == 'martingale':
                bet = min(bankroll, bet * 2)  # Double bet on loss
            elif strategy == 'anti-martingale':
                bet = bet_size  # Reset to initial bet
        
        bet = max(bet_size, bet)  # Ensure minimum bet size
        bankroll_history.append(bankroll)
        
        if bankroll <= 0:
            break  # Stop if bankrupt
    
    return bankroll_history

# Simulation parameters
rounds = 100  # Number of betting rounds
strategies = ["martingale", "anti-martingale", "fixed", "kelly"]
initial_bankroll = 1000
bet_size = 10

# Run simulations
results = {strategy: simulate_betting(strategy, initial_bankroll, bet_size, rounds) for strategy in strategies}

# Plot results
plt.figure(figsize=(10, 5))
for strategy, history in results.items():
    plt.plot(history, label=strategy)
plt.axhline(y=initial_bankroll, color='gray', linestyle='--', label='Starting Bankroll')
plt.xlabel("Rounds")
plt.ylabel("Bankroll")
plt.legend()
plt.title("Betting Strategy Simulation")
plt.show()
