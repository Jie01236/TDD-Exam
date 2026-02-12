# Texas Hold'em Hand Evaluator (TDD)

This project implements a **Texas Hold'em poker hand evaluator** using **Test-Driven Development (TDD)**.

---

## Implemented Features

### 1. Card Model
- Parse cards from string notation (e.g. `AS`, `10H`, `QD`)
- Validate invalid inputs
- Rank comparison independent of suit

### 2. Five-Card Hand Evaluation (`rank5`)
All **9 poker hand categories** are supported with correct ordering and tie-break rules:

- HIGH_CARD  
- ONE_PAIR  
- TWO_PAIR  
- THREE_OF_A_KIND  
- STRAIGHT (including A2345 wheel)  
- FLUSH  
- FULL_HOUSE  
- FOUR_OF_A_KIND  
- STRAIGHT_FLUSH  

Each evaluation returns:
- `category`
- `chosen5` 
- `tiebreak` tuple used for comparisons

### 3. Best-of-7 Evaluation
- Selects the best possible 5-card hand from 7 cards
- Fully supports Texas Hold'em rules
- Allows **board plays** (0, 1, or 2 hole cards)

### 4. Multi-Player Winner Determination
- Evaluates multiple players against the same board
- Supports ties and split pots
- Returns all winning players when hands are equal

---

## Project Structure

```
poker/
  card.py
  evaluator.py

tests/
  test_card.py
  test_rank5.py
  test_best_of_7.py
  test_holdem_best.py
  test_winners.py
```

---

## Running the Tests

From the project root, run:

```bash
python -m pytest
```

All tests should pass.

---

## Development Approach

This project was developed using **Test-Driven Development (TDD)**:

- Tests were written before implementations
- Functionality was added incrementally
- Commit history reflects the red → green → refactor cycle

---

## Author

- Name: Jie Fan
