states = {'a', 'b', 'c', 'd', 'e', 'f'}
start_state = 'a'
final_states = {'f'}
transitions = {
    ('a', '0'): 'b',
    ('a', '1'): 'c',
    ('b', '0'): 'b',
    ('b', '1'): 'd',
    ('c', '0'): 'b',
    ('c', '1'): 'e',
    ('d', '0'): 'c',
    ('d', '1'): 'f',
    ('e', '0'): 'c',
    ('e', '1'): 'f',
    ('f', '0'): 'trap',
    ('f', '1'): 'trap',
    ('trap', '0'): 'trap',
    ('trap', '1'): 'trap',
}

alphabet = ['0', '1']

class DFA:
    def __init__(self, states, start_state, final_states, transitions):
        self.states = states
        self.start_state = start_state
        self.final_states = final_states
        self.transitions = transitions

def clean_dfa_nodes(dfa, transitions):
    visited_nodes = set()

    def dfs(node):
        if node in visited_nodes:
            return
        visited_nodes.add(node)
        for symbol in alphabet:
            next_node = transitions.get((node, symbol), None)
            if next_node:
                dfs(next_node)

    dfs(dfa.start_state)

    unreachable_nodes = {node for node in dfa.states if node not in visited_nodes}
    for node in unreachable_nodes:
        dfa.states.remove(node)
        dfa.final_states.discard(node)
        for symbol in alphabet:
            transitions.pop((node, symbol), None)

    pruned_transitions = {}
    for k, v in transitions.items():
        if v not in unreachable_nodes:
            pruned_transitions[k] = v
    return dfa.states, pruned_transitions

def generate_node_pairs(all_nodes, final_states, transitions, alphabet):
    marginal = []
    non_marginal = []
    for node1 in all_nodes:
        for node2 in all_nodes:
            if node1 != node2:
                marginal.append((node1, node2))
                if ((node1 in final_states and node2 not in final_states) or
                   (node1 not in final_states and node2 in final_states)):
                    non_marginal.append((node1, node2))

    new_marginal = []
    new_non_marginal = []

    for pair in marginal:
        node1, node2 = pair
        if (node1 in final_states and node2 not in final_states) or (node1 not in final_states and node2 in final_states):
            continue
        conditions_met = check_conditions(pair, transitions, alphabet, final_states)
        if conditions_met:
            new_marginal.append(pair)
        else:
            new_non_marginal.append(pair)

    return new_marginal, new_non_marginal

def check_conditions(pair, transitions, alphabet, final_states):
    node1, node2 = pair
    if node2 in start_state or node1 in start_state:
            return False

    for symbol in alphabet:

        next_node_1 = transitions.get((node1, symbol), None)
        next_node_2 = transitions.get((node2, symbol), None)

        if (next_node_1 in final_states) != (next_node_2 in final_states):
            return False

    return True

def merge_similar_pairs(pairs):
    merged_pairs = []

    for i, pair1 in enumerate(pairs):
        if pair1:
            merged_pair = set(pair1)
            pairs[i] = None
            for pair2 in pairs[i + 1:]:
                if pair2 and merged_pair.intersection(set(pair2)):
                    merged_pair.update(pair2)
                    pairs[pairs.index(pair2)] = None

            merged_pairs.append(list(merged_pair))

    return merged_pairs

def merge_nodes(dfa, merge_lists):
    new_states = set()
    new_transitions = {}

    merged_final_states = set()
    for merge_list in merge_lists:
        for state in dfa.final_states:
            if state in merge_list:
                merged_final_states.add(state)

    non_merged_final_states = dfa.final_states - merged_final_states

    for state in dfa.states:
        merged = False
        for merge_list in merge_lists:
            if state in merge_list:
                new_state = '_'.join(merge_list)
                merged = True
                break
        if not merged:
            new_state = state
        new_states.add(new_state)

    new_start_state = dfa.start_state
    for merge_list in merge_lists:
        if dfa.start_state in merge_list:
            new_start_state = '_'.join(merge_list)
            break

    new_final_states = set()
    for state in new_states:
        if any(final_state in state for final_state in merged_final_states):
            new_final_states.add(state)
    new_final_states.update(non_merged_final_states)

    for (origin, symbol), destination in dfa.transitions.items():
        new_origin = origin
        for merge_list in merge_lists:
            if origin in merge_list:
                new_origin = '_'.join(merge_list)
                break

        new_destination = destination
        for merge_list in merge_lists:
            if destination in merge_list:
                new_destination = '_'.join(merge_list)
                break

        new_transitions[(new_origin, symbol)] = new_destination

    updated_dfa = DFA(new_states, new_start_state, new_final_states, new_transitions)
    print("Updated DFA:")
    print("States:", updated_dfa.states)
    print("Start State:", updated_dfa.start_state)
    print("Final States:", updated_dfa.final_states)
    print("Transitions:", updated_dfa.transitions)

dfa1 = DFA(states, start_state, final_states, transitions)

all_nodes, new_transitions = clean_dfa_nodes(dfa1, transitions)

result_marginal, result_non_marginal = generate_node_pairs(all_nodes, final_states, new_transitions, alphabet)

merged_pairs = merge_similar_pairs(result_marginal)

dfa = DFA(all_nodes, start_state, final_states, new_transitions)
merge_nodes(dfa, merged_pairs)

print("merged")
print(merged_pairs)
print('non_mrged')
print(result_non_marginal)