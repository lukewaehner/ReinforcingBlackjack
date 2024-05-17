# Reinforcing Blackjack

## Directory Structure

- **backend/**: Root directory for your backend.
  - **app.py**: Entry point for your Flask application.
  - **blackjack/**: Package for Blackjack-related modules.
    - `__init__.py`: Makes this directory a Python package.
    - `blackjackenv.py`: Contains the Blackjack environment.
    - `models.py`: Contains any data models you might have.
    - `qlearningagent.py`: Contains the Q-Learning agent.
  - **data/**: Directory for storing data files like Q-tables.
    - `q_table_best.pkl`: Best Q-table.
    - `q_table.pkl`: Current Q-table.
  - **scripts/**: Directory for various scripts used for training and validation.
    - `incrementaltraining.py`: Script for incremental training.
    - `randomsearch.py`: Script for hyperparameter random search.
    - `trainagent.py`: Script for training the agent.
    - `validateagent.py`: Script for validating the agent.

## Usage

### Running the Flask App

```bash
python backend/app.py
```
