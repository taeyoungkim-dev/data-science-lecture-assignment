#Reading input.txt
def read_input_file(file_name):
    with open(file_name, 'r') as f:
        #There is no same item in one transaction, so set is the best data structure to store the transaction
        transactions = [set(line.strip().split('\t')) for line in f]
    return transactions

def count_item_set_in_transaction(transactions,candidate_itemset):
    count = 0
    for transaction in transactions:
        if candidate_itemset.issubset(transaction):
            count += 1
    return count

#Finding frequent itemsets with apriori algorithm
def get_frequent_itemsets_with_apriori(transactions, min_support):
    from itertools import combinations
    from collections import defaultdict
#---1. Making 1_size_frequent_item_sets_dictionary---
    item_count = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_count[item] += 1
    size_1_frequent_item_sets_dict = {frozenset({item}):count for item,count in item_count.items() if count>=min_support}
#---2. Making all_frequent_item_sets_dictionary_list
    #Index means size of set
    all_frequent_item_sets_dict_list = [{}]
    all_frequent_item_sets_dict_list.append(size_1_frequent_item_sets_dict)
#---3. Looping to search all frequent item sets
    size_of_set = 2
    while True:
#-------3.1 Joining
        #Loading post loop sets
        post_loop_item_sets_set = set(all_frequent_item_sets_dict_list[-1].keys())
        #combination
        combinations_set = {a|b for a,b in combinations(post_loop_item_sets_set,2)}
        candidate_item_sets_set = {item_set for item_set in combinations_set if len(item_set)==size_of_set}
#-------3.2 Pruning
        passed_item_sets_set = set()
        flag = True
        for candidate_item_set in candidate_item_sets_set:
            candidate_item_set_combination_set = combinations(candidate_item_set,size_of_set-1)
            for candidate_item_set_combination in candidate_item_set_combination_set:
                if frozenset(candidate_item_set_combination) not in post_loop_item_sets_set:
                    flag = False
                    break
            if flag:
                passed_item_sets_set.add(candidate_item_set)
            else:
                flag = True
#-------3.3 Filtering
        candidate_item_sets_dict = {}
        for item_set in passed_item_sets_set:
            count = count_item_set_in_transaction(transactions,item_set)
            if count>=min_support:
                candidate_item_sets_dict[item_set] = count
#-------3.4 Saving or break
        if len(candidate_item_sets_dict)==0:
            break
        all_frequent_item_sets_dict_list.append(candidate_item_sets_dict)
        size_of_set += 1
#---4. return
    return all_frequent_item_sets_dict_list
def get_association_rules(frequent_item_sets_dict_list):
    pass
    #TODO
def writing_output_file(file_name,association_rules_set):
    pass
    #TODO

if __name__ == "__main__":
    import sys
    # Parse command line arguments
    min_support = int(sys.argv[1])
    input_file_name = sys.argv[2]
    output_file_name = sys.argv[3]
    
    #1. Reading input.txt
    transactions = read_input_file(input_file_name)
    #2. Searching frequent itemsets
    frequent_item_sets_dict_list = get_frequent_itemsets_with_apriori(transactions,min_support)
    #3. Searching association rules
    association_rules_set = get_association_rules(frequent_item_sets_dict_list)
    #4. Making output.txt
    writing_output_file(output_file_name,association_rules_set)