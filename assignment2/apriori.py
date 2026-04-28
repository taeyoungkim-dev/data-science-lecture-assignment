#Reading input.txt
def read_input_file(file_name):
    with open(file_name, 'r') as f:
        #There is no same item in one transaction, so set is the best data structure to store the transaction
        transactions = [set(line.strip().split('\t')) for line in f]
    return transactions

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
    frequent_itemsets.append({frozenset({item}):count for item,count in size_1_item_count.items() if count>=min_support})
    #Making size 2 frequent item
    size_2_itemsets = {a|b for a,b in combinations([frequent_itemsets[1].keys],2)}
    #LOOP
