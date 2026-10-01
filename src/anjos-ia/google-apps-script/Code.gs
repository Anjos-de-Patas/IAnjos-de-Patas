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
