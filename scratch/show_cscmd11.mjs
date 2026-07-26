import fs from 'fs';

const nepContent = fs.readFileSync('./js/nep-data.js', 'utf8')
  .replace('export const NEP_LATEX_PYQ_DATA =', 'const NEP_LATEX_PYQ_DATA =')
  .replace(/export\s+/g, '');
const evalNepEnv = new Function(nepContent + '; return NEP_LATEX_PYQ_DATA;');
const NEP_LATEX_PYQ_DATA = evalNepEnv();

const papers = NEP_LATEX_PYQ_DATA.filter(p => p.nepCode && p.nepCode.toLowerCase().includes('cscmd11'));
console.log("Papers for cscmd11:");
papers.forEach(p => {
  console.log(`- Title: ${p.subject}, Code: ${p.code}, File: ${p.filePath}`);
});
