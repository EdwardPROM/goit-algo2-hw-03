import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Побудова графа логістичної мережі
def build_graph():
    G = nx.DiGraph()
    edges = [
        ("Термінал 1", "Склад 1", 25),
        ("Термінал 1", "Склад 2", 20),
        ("Термінал 1", "Склад 3", 15),
        ("Термінал 2", "Склад 3", 15),
        ("Термінал 2", "Склад 4", 30),
        ("Термінал 2", "Склад 2", 10),
        ("Склад 1", "Магазин 1", 15),
        ("Склад 1", "Магазин 2", 10),
        ("Склад 1", "Магазин 3", 20),
        ("Склад 2", "Магазин 4", 15),
        ("Склад 2", "Магазин 5", 10),
        ("Склад 2", "Магазин 6", 25),
        ("Склад 3", "Магазин 7", 20),
        ("Склад 3", "Магазин 8", 15),
        ("Склад 3", "Магазин 9", 10),
        ("Склад 4", "Магазин 10", 20),
        ("Склад 4", "Магазин 11", 10),
        ("Склад 4", "Магазин 12", 15),
        ("Склад 4", "Магазин 13", 5),
        ("Склад 4", "Магазин 14", 10),
    ]
    for u, v, capacity in edges:
        G.add_edge(u, v, capacity=capacity)
    return G

# Візуалізація графа з ребрами
def draw_graph(G, title="Граф логістичної мережі", flow_dict=None):
    plt.figure(figsize=(14, 10))
    
    pos = nx.spring_layout(G, seed=42)  # Автоматичне розташування вершин
    
    # Ноди
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='lightblue')
    
    # Ребра та підписи
    edge_labels = {}
    for u, v, data in G.edges(data=True):
        capacity = data.get('capacity', 0)
        
        if flow_dict:
            flow = flow_dict.get(u, {}).get(v, 0)
            label = f"{flow}/{capacity}"
        else:
            label = f"{capacity}"
        
        edge_labels[(u, v)] = label
    
    # Малюємо ребра
    nx.draw_networkx_edges(G, pos, width=2, arrows=True, arrowstyle='-|>')
    
    # Додаємо підписи ребер і вершин
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title(title, fontsize=16)
    plt.axis('off')
    plt.show()

# Обчислення максимального потоку
def compute_max_flow(G, sources, sinks):
    super_source, super_sink = "Джерело", "Стік"

    for source in sources:
        G.add_edge(super_source, source, capacity=float('inf'))
    for sink in sinks:
        G.add_edge(sink, super_sink, capacity=float('inf'))

    flow_value, flow_dict = nx.maximum_flow(G, super_source, super_sink, flow_func=nx.algorithms.flow.edmonds_karp)

    G.remove_node(super_source)
    G.remove_node(super_sink)

    return flow_value, flow_dict

# Розрахунок фактичних потоків між терміналами та магазинами
def calculate_terminal_to_store_flows(flow_dict, sources, intermediate_nodes, sinks):
    terminal_to_store_flows = []

    for terminal in sources:
        for warehouse in intermediate_nodes:
            flow_terminal_to_warehouse = flow_dict.get(terminal, {}).get(warehouse, 0)

            if flow_terminal_to_warehouse > 0:
                for store in sinks:
                    flow_warehouse_to_store = flow_dict.get(warehouse, {}).get(store, 0)
                    if flow_warehouse_to_store > 0:
                        flow = min(flow_terminal_to_warehouse, flow_warehouse_to_store)
                        terminal_to_store_flows.append([terminal, store, flow])

    return terminal_to_store_flows

# Основний процес
G = build_graph()

sources = ["Термінал 1", "Термінал 2"]
intermediate_nodes = ["Склад 1", "Склад 2", "Склад 3", "Склад 4"]
sinks = ["Магазин 1", "Магазин 2", "Магазин 3", "Магазин 4", "Магазин 5", "Магазин 6",
         "Магазин 7", "Магазин 8", "Магазин 9", "Магазин 10", "Магазин 11", "Магазин 12",
         "Магазин 13", "Магазин 14"]

# Початковий граф
draw_graph(G, title="Початкова логістична мережа (пропускні здатності)")

# Обчислення максимального потоку
max_flow, flow_distribution = compute_max_flow(G, sources, sinks)

# Фінальний граф із потоками
draw_graph(G, title=f"Фактичні потоки товарів (загальний потік {max_flow})", flow_dict=flow_distribution)

# Розрахунок фактичних потоків між терміналами та магазинами
flow_results = calculate_terminal_to_store_flows(flow_distribution, sources, intermediate_nodes, sinks)

# Таблиця з результатами
df_flow_results = pd.DataFrame(flow_results, columns=["Термінал", "Магазин", "Фактичний Потік (одиниць)"])

# Виведення таблиці в консоль
print(df_flow_results)

# Виведення максимального потоку
print(f"\nМаксимальний загальний потік: {max_flow}")
