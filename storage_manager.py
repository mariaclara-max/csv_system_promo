# storage_manager.py
import os
import shutil
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

class StorageManager:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.backup_dir = self.base_path / "BACKUPS_DIR"
        self.logs_dir = self.base_path / "LOGS_DIR"
        self.archive_dir = self.base_path / "ARCHIVE_HISTORIC"
        self.mantenimiento_log = self.logs_dir / "Mantenimiento_Storage.log"
        
        for folder in [self.backup_dir, self.logs_dir, self.archive_dir]:
            folder.mkdir(parents=True, exist_ok=True)

    def _registrar_evento(self, mensaje):
        """Escribe una línea en el log de respaldo/mantenimiento."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.mantenimiento_log, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {mensaje}\n")

    def rotar_backups(self, dias_maximos=7):
        """Borra backups antiguos e informa el volumen liberado."""
        ahora = datetime.now()
        archivos_borrados = 0
        espacio_liberado = 0
        
        for archivo in self.backup_dir.glob("*.*"):
            mtime = datetime.fromtimestamp(archivo.stat().st_mtime)
            if ahora - mtime > timedelta(days=dias_maximos):
                tamano = archivo.stat().st_size
                espacio_liberado += tamano
                archivo.unlink()
                archivos_borrados += 1
        
        if archivos_borrados > 0:
            mb_liberados = espacio_liberado / (1024 * 1024)
            self._registrar_evento(f"LIMPIEZA: Se eliminaron {archivos_borrados} backups antiguos. Espacio recuperado: {mb_liberados:.2f} MB.")

    def comprimir_logs_antiguos(self):
        """Comprime logs y registra qué archivos se procesaron."""
        mes_actual = datetime.now().strftime("%Y_%m")
        zip_path = self.logs_dir / f"logs_historial_{mes_actual}.zip"
        logs_procesados = []

        for log_file in self.logs_dir.glob("*.log"):
            # No comprimimos el propio log de mantenimiento ni el de lectura actual
            if log_file.name in [self.mantenimiento_log.name, "Log_lectura.log"]:
                continue
            
            tamano_orig = log_file.stat().st_size / 1024 # KB
            with zipfile.ZipFile(zip_path, 'a', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(log_file, log_file.name)
            
            logs_procesados.append(f"{log_file.name} ({tamano_orig:.1f} KB)")
            
            # Limpiamos el contenido del log tras zipearlo
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(f"--- REINICIO TRAS COMPRESIÓN {datetime.now()} ---\n")

        if logs_procesados:
            self._registrar_evento(f"COMPRESIÓN: Logs archivados en {zip_path.name}: {', '.join(logs_procesados)}")

    def archivar_csv_procesado(self, file_path):
        """Mueve el archivo y registra el volumen de datos movido."""
        mes_dir = self.archive_dir / datetime.now().strftime("%Y_%m")
        mes_dir.mkdir(exist_ok=True)
        
        tamano_item = os.path.getsize(file_path) / 1024 # KB
        destino = mes_dir / file_path.name
        
        if destino.exists():
            destino = mes_dir / f"{datetime.now().strftime('%H%M%S')}_{file_path.name}"
            
        shutil.move(str(file_path), str(destino))
        self._registrar_evento(f"ARCHIVO: '{file_path.name}' ({tamano_item:.1f} KB) movido a HISTÓRICO.")