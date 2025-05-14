const { ocr } = require('llama-ocr');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const pdfjsLib = require("pdfjs-dist/legacy/build/pdf.js");

async function runOcr(pdfDir, outputFile, tempImagesDir, ocrApiKey) {
  try {
    if (!fs.existsSync(tempImagesDir)) {
      fs.mkdirSync(tempImagesDir);
    }

    const pdfFiles = fs.readdirSync(pdfDir)
      .filter(file => /\.pdf$/i.test(file));

    let markdownContent = `# Résultats OCR - ${new Date().toLocaleString()}\n\n`;

    for (const pdfFile of pdfFiles) {
      const pdfPath = path.join(pdfDir, pdfFile);
      console.log(`📄 Conversion de : ${pdfPath}`);

      const pageCount = await getPdfPageCount(pdfPath);

      for (let i = 1; i <= pageCount; i++) {
        const outputPath = path.join(tempImagesDir, `page_${i}.png`);

        // Utilisation de la commande convert directement
        execSync(`convert -density 150 "${pdfPath}[${i-1}]" -quality 90 "${outputPath}"`);

        console.log(`🧠 OCR sur : ${outputPath}`);

        const markdown = await ocr({
          filePath: outputPath,
          apiKey: ocrApiKey
        });

        markdownContent += `## ${pdfFile} - Page ${i}\n\n`;
        markdownContent += markdown + '\n\n---\n\n';
      }
    }

    fs.writeFileSync(outputFile, markdownContent, 'utf8');
    console.log(`✅ Résultats sauvegardés dans ${outputFile}`);
  } catch (error) {
    console.error('❌ Erreur OCR :', error.message);
  }
}

async function getPdfPageCount(pdfPath) {
  const data = new Uint8Array(fs.readFileSync(pdfPath));
  const doc = await pdfjsLib.getDocument({ data }).promise;
  return doc.numPages;
}

// Accept command-line arguments
const pdfDir = process.argv[2];
const outputFile = process.argv[3];
const tempImagesDir = process.argv[4];
const ocrApiKey = process.argv[5];

runOcr(pdfDir, outputFile, tempImagesDir, ocrApiKey).catch(console.error);

