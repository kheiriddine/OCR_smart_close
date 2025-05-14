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

    const files = fs.readdirSync(pdfDir);
    let markdownContent = `# Résultats OCR - ${new Date().toLocaleString()}\n\n`;

    for (const file of files) {
      const filePath = path.join(pdfDir, file);
      console.log(`📄 Processing: ${filePath}`);

      if (file.toLowerCase().endsWith('.pdf')) {
        const pageCount = await getPdfPageCount(filePath);

        for (let i = 1; i <= pageCount; i++) {
          const outputPath = path.join(tempImagesDir, `page_${i}.png`);

          // Use the convert command directly
          execSync(`convert -density 150 "${filePath}[${i-1}]" -quality 90 "${outputPath}"`);

          console.log(`🧠 OCR on: ${outputPath}`);

          const markdown = await ocr({
            filePath: outputPath,
            apiKey: ocrApiKey
          });

          markdownContent += `## ${file} - Page ${i}\n\n`;
          markdownContent += markdown + '\n\n---\n\n';
        }
      } else if (file.match(/\.(jpg|jpeg|png|gif)$/i)) {
        console.log(`🧠 OCR on: ${filePath}`);

        const markdown = await ocr({
          filePath: filePath,
          apiKey: ocrApiKey
        });

        markdownContent += `## ${file}\n\n`;
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
