const { ocr } = require('llama-ocr');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const pdfDir = './Docs';
const outputFile = 'ocr_output_1.md';
const tempImagesDir = './temp_images';

async function runOcr() {
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
          apiKey: process.env.TOGETHER_API_KEY
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

function getPdfPageCount(pdfPath) {
  const pdfjsLib = require("pdfjs-dist/legacy/build/pdf.js");
  const data = new Uint8Array(fs.readFileSync(pdfPath));
  return pdfjsLib.getDocument({ data }).promise.then(doc => doc.numPages);
}

runOcr();
