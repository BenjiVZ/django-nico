import requests
from pathlib import Path

def setup_chartjs():
    # Solo configuración para Chart.js
    chartjs_file = {
        'path': 'lidotel_app/static/vendor/chartjs/js/chart.min.js',
        'url': 'https://cdn.jsdelivr.net/npm/chart.js@3.7.0/dist/chart.min.js'
    }
    
    # Crear directorio para Chart.js
    file_path = Path(chartjs_file['path'])
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Descargar Chart.js
    print("Descargando Chart.js...")
    try:
        response = requests.get(chartjs_file['url'])
        response.raise_for_status()
        file_path.write_bytes(response.content)
        print("✓ Chart.js descargado exitosamente")
    except Exception as e:
        print(f"✗ Error descargando Chart.js: {str(e)}")

if __name__ == "__main__":
    setup_chartjs()
