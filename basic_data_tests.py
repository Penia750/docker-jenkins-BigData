import pandas as pd
import os

def run_basic_data_tests(file_path):
    print(f"Corriendo pruebas básicas para el dataset: {file_path}")
    try:
        df = pd.read_csv(file_path)
        print("Dataset cargado exitosamente.")

        # Prueba 1: Verificar que el DataFrame no esté vacío
        if df.empty:
            raise ValueError("El dataset está vacío.")
        print("Prueba 1 (DataFrame no vacío): PASSED.")

        # Prueba 2: Verificar la existencia de columnas clave
        required_columns = ['u', 'g', 'r', 'i', 'z', 'redshift', 'class']
        if not all(col in df.columns for col in required_columns):
            missing_cols = [col for col in required_columns if col not in df.columns]
            raise ValueError(f"Faltan columnas requeridas en el dataset: {missing_cols}")
        print("Prueba 2 (Columnas clave existentes): PASSED.")

        # Prueba 3: Verificar que no hay valores nulos en columnas críticas
        critical_columns = ['u', 'g', 'r', 'i', 'z', 'redshift', 'class']
        if df[critical_columns].isnull().any().any():
            null_counts = df[critical_columns].isnull().sum()
            null_cols = null_counts[null_counts > 0].index.tolist()
            raise ValueError(f"Valores nulos encontrados en columnas críticas: {null_cols}")
        print("Prueba 3 (No nulos en columnas críticas): PASSED.")

        # Prueba 4: Verificar tipos de datos
        # Solo un ejemplo, puedes añadir más verificaciones específicas
        if not (pd.api.types.is_numeric_dtype(df['redshift'])):
            raise TypeError("La columna 'redshift' no es numérica.")
        print("Prueba 4 (Tipos de datos correctos): PASSED.")

        print("Todas las pruebas básicas del dataset han PASADO exitosamente.")

    except Exception as e:
        print(f"[ERROR] Fallo en las pruebas básicas del dataset: {e}")
        exit(1) # Salir con código de error para que Jenkins marque el fallo

if __name__ == '__main__':
    # El archivo del dataset se espera en '/app/sdss_sample.csv' dentro del contenedor Docker
    dataset_file = '/app/sdss_sample.csv'
    run_basic_data_tests(dataset_file)
