
import io
from pathlib import Path
import urllib.request
import zipfile

URL = "https://storage.googleapis.com/download.tensorflow.org/data/petfinder-mini.zip"
ARQUIVO_ZIP = "petfinder-mini/petfinder-mini.csv"

ROOT = Path(__file__).resolve().parents[1]
DESTINO = ROOT / "data" / "petfinder-mini.csv"


def obter_dados():
    print("Baixando PetFinder.my mini...")

    with urllib.request.urlopen(URL, timeout=90) as response:
        arquivo_zip = response.read()

    with zipfile.ZipFile(io.BytesIO(arquivo_zip)) as zip_file:
        dados_csv = zip_file.read(ARQUIVO_ZIP)

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_bytes(dados_csv)

    print(f"Arquivo salvo em: {DESTINO}")


if __name__ == "__main__":
    obter_dados()