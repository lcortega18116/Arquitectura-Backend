
# import boto3

# # Configura las credenciales y la región de AWS
# s3 = boto3.client('s3', aws_access_key_id=os.getenv("aws_access_key_id"), aws_secret_access_key='LPsTraFqgII7gxVmwj/m6LSfJ+cIgG51HqMdxcyf', region_name='us-east-1')  # Reemplaza 'us-east-1' con la región correcta

# # Nombre del archivo local
# archivo_local = 'img/copernico.png'

# # Nombre del archivo en S3 (puede incluir una ruta)
# archivo_s3 = 'images/copernico.png'

# # Sube el archivo a S3
# s3.upload_file(archivo_local, 'sgv-filemanager-images', archivo_s3)

# import boto3

# # Configura las credenciales y la región de AWS
# s3 = boto3.client('s3', aws_access_key_id=os.getenv("aws_access_key_id"), aws_secret_access_key='LPsTraFqgII7gxVmwj/m6LSfJ+cIgG51HqMdxcyf', region_name='us-east-1')  # Reemplaza 'us-east-1' con la región correcta

# # Nombre del archivo en S3
# archivo_s3 = 'images/sandbox/art/1234_1.png'

# # Nombre del archivo local donde se guardará la imagen descargada
# archivo_local = 'imagen_descargada.png'

# # Descarga el archivo desde S3
# s3.download_file('sgv-filemanager-images', archivo_s3, archivo_local)


import os
import rembg

# Ruta de tu imagen de entrada
input_path = 'copernico.jpg'

# Ruta donde guardarás la imagen sin fondo
output_path = 'imagen_sin_fondo.png'

# Elimina el fondo de la imagen
with open(input_path, 'rb') as img_file:
    output = rembg.remove(img_file.read())

with open(output_path, 'wb') as output_file:
    output_file.write(output)

print(f'La imagen sin fondo se ha guardado en {output_path}')