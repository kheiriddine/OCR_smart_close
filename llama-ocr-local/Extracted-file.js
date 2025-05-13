const { ocr } = require('llama-ocr');
const fs = require('fs');
const path = require('path');

const imageDir = './Images';
const outputFile = 'ocr_output.md';

async function runOcr() {
  try {
    const files = fs.readdirSync(imageDir)
      .filter(file => /\.(jpg|jpeg|png)$/i.test(file));

    let markdownContent = `# Résultats OCR - ${new Date().toLocaleString()}\n\n`;

    for (const file of files) {
      const filePath = path.join(imageDir, file);
      console.log(`📄 Traitement de : ${filePath}`);

      const markdown = await ocr({
        filePath,
        apiKey: process.env.TOGETHER_API_KEY
      });

      markdownContent += `## ${file}\n\n`;
      markdownContent += markdown + '\n\n---\n\n';
    }

    fs.writeFileSync(outputFile, markdownContent, 'utf8');
    console.log(`✅ Résultats sauvegardés dans ${outputFile}`);
  } catch (error) {
    console.error('❌ Erreur OCR :', error.message);
  }
}

runOcr();

