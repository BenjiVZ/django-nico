import os
import requests
from pathlib import Path

def setup_static_files():
    # Definir la estructura de archivos
    files = {
        'bootstrap': {
            'css/bootstrap.min.css': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
            'js/bootstrap.bundle.min.js': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js'
        },
        'flatpickr': {
            'css/flatpickr.min.css': 'https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css',
            'css/themes/material_blue.css': 'https://cdn.jsdelivr.net/npm/flatpickr/dist/themes/material_blue.css',
            'js/flatpickr.min.js': 'https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.js'
        },
        'fontawesome': {
            'css/all.min.css': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
            'webfonts/fa-brands-400.woff2': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-brands-400.woff2',
            'webfonts/fa-regular-400.woff2': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-regular-400.woff2',
            'webfonts/fa-solid-900.woff2': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-solid-900.woff2'
        },
        'chartjs': {
            'js/chart.min.js': 'https://cdn.jsdelivr.net/npm/chart.js@3.7.0/dist/chart.min.js'
        }
    }

    # Crear directorio vendor si no existe
    base_path = Path('lidotel_app/static/vendor')
    base_path.mkdir(parents=True, exist_ok=True)

    # Descargar y guardar archivos
    for vendor, vendor_files in files.items():
        vendor_path = base_path / vendor
        print(f"\nDescargando archivos para {vendor}...")
        
        for file_path, url in vendor_files.items():
            full_path = vendor_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            print(f"Descargando {file_path}...")
            try:
                response = requests.get(url)
                response.raise_for_status()
                full_path.write_bytes(response.content)
                print(f"✓ Descargado exitosamente")
            except Exception as e:
                print(f"✗ Error descargando {file_path}: {str(e)}")

    print("\n¡Instalación completada!")
    print("Todos los archivos estáticos han sido descargados y organizados.")

if __name__ == "__main__":
    setup_static_files()