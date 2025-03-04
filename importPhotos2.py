import smartsheet
import os
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

# Token de acceso a la API de Smartsheet

smartsheet_client = smartsheet.Smartsheet(token)

# Deshabilitar la verificación de certificados y check_hostname
class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.check_hostname = False  # Disable hostname verification
        context.verify_mode = ssl.CERT_NONE  # Disable certificate verification
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

# Access Smartsheet's HTTP session directly
smartsheet_client._session.mount('https://', SSLAdapter())

# ID de la hoja de Smartsheet
sheet_id = '7774568991117188'

# Carpeta de destino para guardar las fotos
output_folder = '_SIMA_fotos'
os.makedirs(output_folder, exist_ok=True)

# Obtener la hoja completa
sheet = smartsheet_client.Sheets.get_sheet(sheet_id)

# Recorrer las filas de la hoja
for row in sheet.rows:
    if row.row_number > 2712:
    # Obtener los archivos adjuntos para cada fila
        attachments = smartsheet_client.Attachments.list_row_attachments(sheet_id, row.id)
        if attachments.total_count > 0:
            # Crear una carpeta para cada fila con el número de fila como nombre
            row_folder = os.path.join(output_folder, f'FILA_{row.row_number}')
            os.makedirs(row_folder, exist_ok=True)

            # Recorrer los adjuntos y descargarlos
            for attachment in attachments.data:
                # Obtener el objeto completo del adjunto
                attachment_details = smartsheet_client.Attachments.get_attachment(sheet_id, attachment.id)

                # Descargar el archivo adjunto
                smartsheet_client.Attachments.download_attachment(attachment_details, row_folder)
                print(f'Descargado: {attachment.name} en la carpeta {row_folder}')
