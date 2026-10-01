function doPost(e) {
  try {
    const planilha = SpreadsheetApp.getActiveSpreadsheet();
    const aba = planilha.getSheets()[0];
    const dados = JSON.parse(e.postData.contents);

    const numero = aba.getLastRow();
    const protocolo = "ADP-" + String(numero).padStart(4, "0");

    aba.appendRow([
      new Date(),
      dados.nome || "",
      dados.whatsapp || "",
      dados.email || "",
      dados.animal || "",
      dados.aceita_contato || "",
      "Novo interesse",
      protocolo,
      dados.especie || ""
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({
        sucesso: true,
        mensagem: "Solicitação registrada com sucesso",
        protocolo: protocolo
      }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (erro) {
    return ContentService
      .createTextOutput(JSON.stringify({
        sucesso: false,
        mensagem: erro.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  try {
    const planilha = SpreadsheetApp.getActiveSpreadsheet();
    const aba = planilha.getSheets()[0];
    const linhas = aba.getDataRange().getDisplayValues();

    const email = (e.parameter.email || "").trim().toLowerCase();
    const whatsapp = (e.parameter.whatsapp || "").replace(/\D/g, "");
    const animal = (e.parameter.animal || "").trim().toLowerCase();

    if (!email && !whatsapp) {
      return ContentService.createTextOutput(JSON.stringify({
        sucesso: false,
        encontrado: false,
        mensagem: "Informe e-mail ou WhatsApp."
      })).setMimeType(ContentService.MimeType.JSON);
    }

    for (let i = linhas.length - 1; i >= 1; i--) {
      const nomeLinha = (linhas[i][1] || "").trim();
      const whatsappLinha = (linhas[i][2] || "").replace(/\D/g, "");
      const emailLinha = (linhas[i][3] || "").trim().toLowerCase();
      const animalLinha = (linhas[i][4] || "").trim().toLowerCase();
      const statusLinha = (linhas[i][6] || "").trim();
      const protocoloLinha = (linhas[i][7] || "").trim();

      const contatoConfere =
        (email && emailLinha === email) ||
        (whatsapp && whatsappLinha === whatsapp);

      const animalConfere = !animal || animalLinha === animal;

      if (contatoConfere && animalConfere) {
        return ContentService.createTextOutput(JSON.stringify({
          sucesso: true,
          encontrado: true,
          nome: nomeLinha,
          animal: linhas[i][4],
          status: statusLinha,
          protocolo: protocoloLinha
        })).setMimeType(ContentService.MimeType.JSON);
      }
    }

    return ContentService.createTextOutput(JSON.stringify({
      sucesso: true,
      encontrado: false,
      mensagem: "Solicitação não encontrada."
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (erro) {
    return ContentService.createTextOutput(JSON.stringify({
      sucesso: false,
      encontrado: false,
      mensagem: erro.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}
