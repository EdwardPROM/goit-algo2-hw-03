from BTrees.OOBTree import OOBTree
import pandas as pd
import timeit

# Завантаження даних
df = pd.read_csv("generated_items_data.csv")

# Створення OOBTree з Price як ключем
tree = OOBTree()
dict_data = {}

# Додаємо в дерево по Price
for _, row in df.iterrows():
    price = row['Price']
    item = {
        'ID': row['ID'],
        'Name': row['Name'],
        'Category': row['Category'],
        'Price': price
    }
    # Додаємо в дерево
    if price in tree:
        tree[price].append(item)
    else:
        tree[price] = [item]

    # Додаємо в dict
    dict_data[row['ID']] = item

# Діапазонний запит для дерева (по цінам)
def range_query_tree(tree, min_price, max_price):
    result = []
    for price, items in tree.items(min_price, max_price):
        result.extend(items)
    return result

# Діапазонний запит для dict (повний перебір)
def range_query_dict(dictionary, min_price, max_price):
    result = []
    for item in dictionary.values():
        if min_price <= item['Price'] <= max_price:
            result.append(item)
    return result

# Timeit функції
def run_tree_query():
    range_query_tree(tree, 10, 100)

def run_dict_query():
    range_query_dict(dict_data, 10, 100)

# Вимірювання часу
tree_time = timeit.timeit(run_tree_query, number=100)
dict_time = timeit.timeit(run_dict_query, number=100)

print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
print(f"Total range_query time for Dict: {dict_time:.6f} seconds")

if tree_time < dict_time:
    print("OOBTree is faster than Dict for range queries!")
else:
    print("Dict is faster than OOBTree for range queries!")
