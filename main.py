import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Crear el directorio 'outputs' si no existe
OUTPUTS_DIR = 'outputs'
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# --- 1. Cargar el Dataset ---
print("Cargando el dataset...")
df = pd.read_csv('/content/sample_data/sdss_sample.csv')
print(df.head())

# --- 2. Clasificación ---
print("\nEjecutando Clasificación (KNN)...")
if 'class' in df.columns:
    X = df[['u', 'g', 'r', 'i', 'z', 'redshift']] # Características
    y = df['class'] # Variable objetivo (asumida)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)
    y_pred_knn = knn.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred_knn)
    conf_matrix = confusion_matrix(y_test, y_pred_knn)

    print(f"Precisión (Accuracy): {accuracy:.4f}")
    print("Matriz de Confusión:\n", conf_matrix)

    # Guardar gráfica de Matriz de Confusión
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
                xticklabels=knn.classes_, yticklabels=knn.classes_)
    plt.xlabel('Predicción')
    plt.ylabel('Valor Real')
    plt.title('Matriz de Confusión KNN (k=5)')
    plt.savefig(os.path.join(OUTPUTS_DIR, 'confusion_matrix_knn.png'))
    plt.close() # Cerrar la figura para liberar memoria

    # Guardar métricas de clasificación
    with open(os.path.join(OUTPUTS_DIR, 'classification_metrics.txt'), 'w') as f:
        f.write(f"Accuracy: {accuracy:.4f}\n")
        f.write(f"Confusion Matrix:\n{conf_matrix}\n")
else:
    print("Columna 'class' no encontrada, saltando clasificación.")

# --- 3. Regresión ---
print("\nEjecutando Regresión (Lineal)...")
X_reg = df[['u', 'g', 'r', 'i', 'z']]
y_reg = df['redshift']

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_reg, y_reg, test_size=0.3, random_state=42)

linear_model = LinearRegression()
linear_model.fit(X_train_reg, y_train_reg)
y_pred_reg = linear_model.predict(X_test_reg)

mse = mean_squared_error(y_test_reg, y_pred_reg)
r2 = r2_score(y_test_reg, y_pred_reg)

print(f"Error Cuadrático Medio (MSE): {mse:.4f}")
print(f"Coeficiente de Determinación (R²): {r2:.4f}")

# Guardar gráfica de Regresión
plt.figure(figsize=(10, 6))
plt.scatter(y_test_reg, y_pred_reg, alpha=0.5)
plt.plot([y_test_reg.min(), y_test_reg.max()], [y_test_reg.min(), y_test_reg.max()], 'r--')
plt.xlabel('Redshift Real')
plt.ylabel('Redshift Predicho')
plt.title('Regresión Lineal: Predicciones vs. Valores Reales')
plt.grid(True)
plt.savefig(os.path.join(OUTPUTS_DIR, 'regression_predictions.png'))
plt.close()

# Guardar métricas de regresión
with open(os.path.join(OUTPUTS_DIR, 'regression_metrics.txt'), 'w') as f:
    f.write(f"MSE: {mse:.4f}\n")
    f.write(f"R2: {r2:.4f}\n")

# --- 4. Clustering ---
print("\nEjecutando Clustering (KMeans)...")
X_cluster = df[['u', 'g', 'r', 'i', 'z']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_cluster)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)
df['cluster'] = clusters

print("Conteo de elementos por cluster:\n", df['cluster'].value_counts())

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df_pca = pd.DataFrame(data=X_pca, columns=['PC1', 'PC2'])
df_pca['cluster'] = clusters
df_pca['class'] = df['class']

# Guardar gráficas de Clustering
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
sns.scatterplot(x='PC1', y='PC2', hue='cluster', data=df_pca, palette='viridis', legend='full')
plt.title('Clusters de KMeans (PCA 2D)')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.subplot(1, 2, 2)
sns.scatterplot(x='PC1', y='PC2', hue='class', data=df_pca, palette='tab10', legend='full')
plt.title('Clases Reales (PCA 2D)')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUTS_DIR, 'clustering_pca.png'))
plt.close()

# Guardar matriz de contingencia
contingency_matrix = pd.crosstab(df['cluster'], df['class'])
print("Matriz de Contingencia (Clusters vs Clases Reales):\n", contingency_matrix)
with open(os.path.join(OUTPUTS_DIR, 'clustering_contingency_matrix.txt'), 'w') as f:
    f.write("Contingency Matrix (Clusters vs Real Classes):\n")
    f.write(contingency_matrix.to_string())

print("\nPipeline de ML completado y resultados guardados en el directorio 'outputs/'.")
