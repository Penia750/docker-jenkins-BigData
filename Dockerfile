# Usar una imagen base de Python
FROM python:3.10-slim-buster

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo requirements.txt e instalar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el script principal (asegúrate de que exista un main.py)
# Asumimos que el dataset está en /content/sample_data/sdss_sample.csv
# y es accesible o se copiará de alguna forma al contenedor.
# Para este ejemplo, ajustamos la ruta del dataset en main.py a la ruta en el contenedor.
COPY main.py .

# Crear el directorio para los outputs
RUN mkdir -p outputs

# Comando para ejecutar el script principal
# Puedes ajustar el comando según cómo quieras ejecutar tu script
CMD ["python", "main.py"]
