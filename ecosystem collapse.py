# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nP7mf4bc6Izr8o6zF87UXLvHb9EZTP37
"""

import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


# Simulate Food Web Data (Dummy Data for Illustration)


# 10 ecosystems, each represented by a food web graph
ecosystem_graphs = []
ecosystem_labels = []  # 1 = At Risk, 0 = Stable

for i in range(10):
    G = nx.erdos_renyi_graph(n=np.random.randint(10, 20), p=0.2)
    ecosystem_graphs.append(G)

    # Simulate that smaller or sparser ecosystems are more at risk
    risk = 1 if G.number_of_nodes() < 15 or nx.density(G) < 0.15 else 0
    ecosystem_labels.append(risk)


# Feature Extraction from Graphs


features = []

for G in ecosystem_graphs:
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    avg_degree = np.mean([deg for _, deg in G.degree()])
    density = nx.density(G)
    clustering_coeff = nx.average_clustering(G)

    features.append([num_nodes, num_edges, avg_degree, density, clustering_coeff])

# Convert to DataFrame
feature_names = ["num_nodes", "num_edges", "avg_degree", "density", "clustering_coeff"]
X = pd.DataFrame(features, columns=feature_names)
y = np.array(ecosystem_labels)

print("Feature Matrix:")
print(X)
print("\nLabels:")
print(y)

# Train ML Model


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)


# Evaluation


y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# Feature Importance Visualization


importances = model.feature_importances_
plt.figure(figsize=(8, 5))
plt.barh(feature_names, importances, color='forestgreen')
plt.xlabel('Feature Importance')
plt.title('Which Graph Features Influence Collapse Prediction')
plt.show()

#  Visualize Example Food Web


plt.figure(figsize=(5,5))
example_graph = ecosystem_graphs[0]
nx.draw_networkx(example_graph, with_labels=False, node_color='skyblue', edge_color='gray')
plt.title("Example Food Web Graph")
plt.show()