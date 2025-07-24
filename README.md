# DFA Minimizer

This project was developed as part of the **Formal Languages and Automata Theory** course in the 4th semester of the Computer Science / Computer Engineering undergraduate program. Its main goal is to implement a **Deterministic Finite Automaton (DFA) minimization algorithm** using Python.

---

## 🧠 About the Project

In deterministic finite automata, some states may be unreachable or behave identically to others. This project simplifies a DFA by:

- Removing unreachable states
- Merging equivalent (indistinguishable) states

It applies theoretical concepts from automata to create a cleaner, more efficient DFA.

---

## ✨ Features

- Identifies and removes unreachable states
- Compares state pairs to find indistinguishable (equivalent) ones
- Merges equivalent states into a new minimized DFA
- Uses standard Python data structures for clean implementation

---

## 🧮 Algorithm Used

This project implements the basic **Minimization Table Filling Method**, which works as follows:

1. Generate all pairs of DFA states  
2. Mark pairs where one is final and the other is not (they are distinguishable)  
3. Check remaining pairs for equivalent transitions  
4. Merge indistinguishable pairs  
5. Build a new minimized DFA from merged states  

---

## 🗂️ Code Structure

- `DFA`: Main class to represent the DFA (states, start state, final states, transitions)
- `clean_dfa_nodes`: Removes unreachable states from the DFA
- `generate_node_pairs`: Generates state pairs for equivalence checking
- `check_conditions`: Checks if a state pair is equivalent
- `merge_similar_pairs`: Groups equivalent state pairs together
- `merge_nodes`: Builds the new minimized DFA with merged states

---

## ▶️ How to Run

Make sure Python is installed on your system. Then simply run the script:

```bash
python dfa_minimizer.py
