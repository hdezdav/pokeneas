"""
Script para ejecutar la aplicación en modo desarrollo.
"""
from app import create_app

if __name__ == '__main__':
    app = create_app('development')
    print("\n" + "="*60)
    print("🚀 Servidor Pokeneas iniciando...")
    print("="*60)
    print("📍 URL: http://localhost:8000")
    print("📍 API: http://localhost:8000/api/pokenea")
    print("📍 Vista: http://localhost:8000/pokenea")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )
