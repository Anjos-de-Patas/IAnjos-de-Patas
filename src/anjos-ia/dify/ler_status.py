import json


def main(body: str):
    try:
        dados = json.loads(body)

        return {
            "encontrado": "sim" if dados.get("encontrado") else "não",
            "nome": str(dados.get("nome", "")),
            "animal": str(dados.get("animal", "")),
            "status": str(dados.get("status", "")),
            "protocolo": str(dados.get("protocolo", "")),
            "mensagem": str(dados.get("mensagem", "")),
        }

    except Exception:
        return {
            "encontrado": "não",
            "nome": "",
            "animal": "",
            "status": "",
            "protocolo": "",
            "mensagem": "Não foi possível consultar a solicitação.",
        }
