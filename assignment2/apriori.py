#Reading input.txt
def read_input_file(file_name):
    with open(file_name, 'r') as f:
        #There is no same item in one transaction, so set is the best data structure to store the transaction
        transactions = [set(line.strip().split('\t')) for line in f]
    return transactions

def count_itemset_in_transaction(transactions,candidate_itemset):
    count = 0
    for transaction in transactions:
        if candidate_itemset.issubset(transaction):
            count += 1
    return count
#Finding frequent itemsets with apriori algorithm
def get_frequent_itemsets_with_apriori(transactions, min_support):
#-----------Initialize frequent itemsets with size of 1 itemsets----------------#
    #Making combinations of items
    from itertools import combinations
    #Easy item counting with defaultdict
    from collections import defaultdict
    #Making size 1 frequent item and filtering
    size_1_item_count = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            size_1_item_count[item] += 1
    #Index means size of set
    frequent_itemsets = [{}]
    #Making size 1 frequent itemset and filtering
    frequent_itemsets.append({frozenset({item}):count for item,count in size_1_item_count.items() if count>=min_support})
    #Making size 2 frequent itemset
    size_2_itemsets = {a|b for a,b in combinations([frequent_itemsets[1].keys],2)}
    candidate_itemsets = size_2_itemsets[:]
    k = 2
    #LOOP
    while not candidate_itemsets.empty():
        k_size_frequent_itemsets = {}
        #1. Counting
        for itemset in candidate_itemsets:
            count = count_itemset_in_transaction(transactions=transactions,candidate_itemset=itemset)
        #2. Filtering
            if count >= min_support:
                k_size_frequent_itemsets.add({frozenset(itemset):count})
        #3. Saving
        frequent_itemsets.append(k_size_frequent_itemsets)
        #4. joining
        candidate_itemsets = {a|b for a,b in combinations(frequent_itemsets[k].keys,k+1)}
        k += 1
        #5. Pruning
        for candidate_itemset in candidate_itemsets:
            for itemset in k_size_frequent_itemsets.key:
                