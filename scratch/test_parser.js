function parseTabular(tabularTex) {
            // Extract column alignment spec
            const colsMatch = tabularTex.match(/\\begin\{tabular\}\s*\{([^}]*)\}/i);
            if (!colsMatch) return '';

            const startIndex = colsMatch.index + colsMatch[0].length;
            const endIndex = tabularTex.lastIndexOf('\\end{tabular}');
            if (endIndex === -1) return '';
            let content = tabularTex.substring(startIndex, endIndex);

            // Clean lines: remove comments
            content = content.replace(/%.*$/gm, '');

            // Split into rows by \\
            const rawRows = content.split(/\\\\/);
            let htmlRows = '';

            rawRows.forEach(row => {
                let line = row.trim();
                // Skip clean-up macros
                line = line.replace(/\\toprule/g, '');
                line = line.replace(/\\midrule/g, '');
                line = line.replace(/\\bottomrule/g, '');
                line = line.replace(/\\hline/g, '');
                line = line.trim();

                if (!line) return;

                const cells = line.split('&');
                let htmlCells = '';
                cells.forEach(cell => {
                    const cellText = cell.trim();
                    htmlCells += `<td class="border border-neutral-300 px-4 py-2 text-center text-xs sm:text-sm font-medium text-primary">${cellText}</td>`;
                });
                htmlRows += `<tr class="hover:bg-neutral-50 transition-colors">${htmlCells}</tr>`;
            });

            return `<div class="overflow-x-auto my-6 flex justify-center"><table class="border-collapse border border-neutral-300 shadow-sm max-w-full bg-white my-2">${htmlRows}</table></div>`;
        }

        // LaTeX parsing engine to transform raw LaTeX documents to clean semantic HTML
        
function parseLatex(latex) {
            function findBalancedClosingBrace(str, startIndex) {
                let depth = 1;
                for (let i = startIndex; i < str.length; i++) {
                    if (str[i] === '{') depth++;
                    else if (str[i] === '}') {
                        depth--;
                        if (depth === 0) return i;
                    }
                }
                return -1;
            }

            function findBalancedClosingBracket(str, startIndex) {
                let depth = 1;
                for (let i = startIndex; i < str.length; i++) {
                    if (str[i] === '[') depth++;
                    else if (str[i] === ']') {
                        depth--;
                        if (depth === 0) return i;
                    }
                }
                return -1;
            }

            function replaceCommandWithBalancedBraces(content, commandPrefix, replacementGenerator) {
                let res = content;
                let idx = 0;
                const lowerPrefix = commandPrefix.toLowerCase();
                while (true) {
                    const matchIndex = res.toLowerCase().indexOf(lowerPrefix, idx);
                    if (matchIndex === -1) break;

                    const openingBraceIndex = res.indexOf('{', matchIndex + commandPrefix.length - 1);
                    if (openingBraceIndex !== -1 && openingBraceIndex < matchIndex + commandPrefix.length + 5) {
                        const closingBraceIndex = findBalancedClosingBrace(res, openingBraceIndex + 1);
                        if (closingBraceIndex !== -1) {
                            const innerContent = res.substring(openingBraceIndex + 1, closingBraceIndex);
                            const replacement = replacementGenerator(innerContent);
                            res = res.substring(0, matchIndex) + replacement + res.substring(closingBraceIndex + 1);
                            idx = matchIndex + replacement.length;
                            continue;
                        }
                    }
                    idx = matchIndex + 1;
                }
                return res;
            }

            function replaceHrefCommand(content) {
                let res = content;
                let idx = 0;
                while (true) {
                    const matchIndex = res.toLowerCase().indexOf('\\href{', idx);
                    if (matchIndex === -1) break;

                    const openingBrace1 = res.indexOf('{', matchIndex);
                    if (openingBrace1 !== -1) {
                        const closingBrace1 = findBalancedClosingBrace(res, openingBrace1 + 1);
                        if (closingBrace1 !== -1) {
                            const url = res.substring(openingBrace1 + 1, closingBrace1);
                            let nextOpenIndex = res.indexOf('{', closingBrace1 + 1);
                            if (nextOpenIndex !== -1 && nextOpenIndex < closingBrace1 + 5) {
                                const closingBrace2 = findBalancedClosingBrace(res, nextOpenIndex + 1);
                                if (closingBrace2 !== -1) {
                                    const text = res.substring(nextOpenIndex + 1, closingBrace2);
                                    const replacement = `<a href="${url}" target="_blank" class="text-primary hover:underline font-semibold">${text}</a>`;
                                    res = res.substring(0, matchIndex) + replacement + res.substring(closingBrace2 + 1);
                                    idx = matchIndex + replacement.length;
                                    continue;
                                }
                            }
                        }
                    }
                    idx = matchIndex + 1;
                }
                return res;
            }

            // Extract verbatim and lstlisting environments to preserve code blocks and avoid MathJax formatting errors
            const verbatimBlocks = [];
            let body = latex.replace(/\\begin\{verbatim\*?\}([\s\S]*?)\\end\{verbatim\*?\}/gi, (match, inner) => {
                const escaped = inner
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;');
                const htmlBlock = `<pre class="bg-neutral-50 border border-neutral-200 rounded-lg p-3.5 sm:p-5 font-mono text-xs overflow-x-auto text-neutral-800 leading-normal my-5 select-all">${escaped}</pre>`;
                const placeholder = `__VERBATIM_BLOCK_${verbatimBlocks.length}__`;
                verbatimBlocks.push(htmlBlock);
                return placeholder;
            });

            // Extract lstlisting environments robustly with potential optional square brackets
            let lstIdx = 0;
            while (true) {
                const startMatch = body.toLowerCase().indexOf('\\begin{lstlisting}', lstIdx);
                if (startMatch === -1) break;

                let contentStart = startMatch + '\\begin{lstlisting}'.length;
                let tempIdx = contentStart;
                while (tempIdx < body.length && (body[tempIdx] === ' ' || body[tempIdx] === '\t' || body[tempIdx] === '\n' || body[tempIdx] === '\r')) {
                    tempIdx++;
                }
                if (body[tempIdx] === '[') {
                    const closingBracket = findBalancedClosingBracket(body, tempIdx + 1);
                    if (closingBracket !== -1) {
                        contentStart = closingBracket + 1;
                    }
                }

                const endMatch = body.toLowerCase().indexOf('\\end{lstlisting}', contentStart);
                if (endMatch === -1) {
                    lstIdx = contentStart;
                    continue;
                }

                const innerContent = body.substring(contentStart, endMatch);
                const escaped = innerContent
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;');
                const htmlBlock = `<pre class="bg-neutral-50 border border-neutral-200 rounded-lg p-3.5 sm:p-5 font-mono text-xs overflow-x-auto text-neutral-800 leading-normal my-5 select-all">${escaped.trim()}</pre>`;
                const placeholder = `__VERBATIM_BLOCK_${verbatimBlocks.length}__`;
                verbatimBlocks.push(htmlBlock);

                body = body.substring(0, startMatch) + placeholder + body.substring(endMatch + '\\end{lstlisting}'.length);
                lstIdx = startMatch + placeholder.length;
            }

            // Extract tikzpicture environments to avoid any formatting corruption
            const tikzPictures = [];
            body = body.replace(/\\begin\{tikzpicture\}[\s\S]*?\\end\{tikzpicture\}/g, (match) => {
                const placeholder = `__TIKZ_PICTURE_${tikzPictures.length}__`;
                tikzPictures.push(match);
                return placeholder;
            });

            // Parse tabular environments to standard HTML tables
            body = body.replace(/\\begin\{tabular\}[\s\S]*?\\end\{tabular\}/gi, (match) => {
                return parseTabular(match);
            });

            // 1. Extract content inside \begin{document} ... \end{document}
            const docStart = body.indexOf('\\begin{document}');
            const docEnd = body.indexOf('\\end{document}');
            if (docStart !== -1 && docEnd !== -1) {
                body = body.substring(docStart + '\\begin{document}'.length, docEnd);
            }

            // 2. Remove comments
            body = body.replace(/^[ \t]*%.*$/gm, '');
            body = body.replace(/([^\\])%.*$/gm, '$1');

            // --- GLOBAL REPLACEMENTS BEFORE SPLITTING BY MATH BLOCKS ---
            // Prevents layout macros containing math symbols (like \pts{5 $\times$ 2 = 10}) from being split and corrupted.

            // Clean printed style for instructions (no colored box) using balanced braces
            body = replaceCommandWithBalancedBraces(body, '\\noindent\\textit{Instructions:', (inner) => {
                return `<div class="my-2 text-xs sm:text-sm italic text-neutral-800"><strong class="not-italic font-bold">Instructions:</strong> ${inner}</div>`;
            });
            body = replaceCommandWithBalancedBraces(body, '\\noindent\\textit{Note:', (inner) => {
                return `<div class="my-2 text-xs sm:text-sm italic text-neutral-800"><strong class="not-italic font-bold">Note:</strong> ${inner}</div>`;
            });
            body = replaceCommandWithBalancedBraces(body, '\\textit{Instructions:', (inner) => {
                return `<div class="my-2 text-xs sm:text-sm italic text-neutral-800"><strong class="not-italic font-bold">Instructions:</strong> ${inner}</div>`;
            });
            body = replaceCommandWithBalancedBraces(body, '\\textit{Note:', (inner) => {
                return `<div class="my-2 text-xs sm:text-sm italic text-neutral-800"><strong class="not-italic font-bold">Note:</strong> ${inner}</div>`;
            });

            // Parse href link commands
            body = replaceHrefCommand(body);

            // Marks command \pts{...} in LaTeX style (aligned to right margin in brackets)
            body = body.replace(/\\pts\{([\s\S]*?)\}/g, '<span class="inline-block float-right text-xs sm:text-sm italic font-normal text-neutral-700">[$1]</span>');

            // Center environments tags (no rounded cards for prints)
            body = body.replace(/\\begin\{center\}/gi, '<div class="text-center pyq-title-block space-y-1">');
            body = body.replace(/\\end\{center\}/gi, '</div>');

            // Font size modifications within brackets
            body = body.replace(/\{\\large\\bfseries\s*([\s\S]*?)\}/gi, '<h2 class="text-base sm:text-xl font-bold tracking-tight text-primary">$1</h2>');
            body = body.replace(/\{\\normalsize\s*([\s\S]*?)\}/gi, '<p class="text-xs sm:text-sm text-secondary font-medium">$1</p>');
            body = body.replace(/\{\\large\s*([\s\S]*?)\}/gi, '<p class="text-sm sm:text-base font-bold text-primary">$1</p>');
            body = body.replace(/\{\\small\s*([\s\S]*?)\}/gi, '<p class="text-[11px] text-secondary">$1</p>');

            // Text styling macros
            body = replaceCommandWithBalancedBraces(body, '\\texttt', (inner) => {
                return `<code class="bg-neutral-50 text-neutral-900 border border-neutral-200 px-1.5 py-0.5 rounded font-mono text-[10px] sm:text-xs select-all">${inner}</code>`;
            });
            body = replaceCommandWithBalancedBraces(body, '\\emph', (inner) => {
                return `<em class="italic">${inner}</em>`;
            });
            body = body.replace(/\\textbf\{([\s\S]*?)\}/g, '<strong>$1</strong>');
            body = body.replace(/\\textit\{([\s\S]*?)\}/g, '<span class="italic">$1</span>');
            body = body.replace(/\\textrm\{([\s\S]*?)\}/g, '<span class="font-serif">$1</span>');
            body = body.replace(/\{\\bfseries\s*([\s\S]*?)\}/g, '<strong>$1</strong>');
            // Underline and hspace parsing using balanced braces
            body = replaceCommandWithBalancedBraces(body, '\\underline', (inner) => {
                return `<span class="border-b border-neutral-900 pb-0.5">${inner}</span>`;
            });
            body = replaceCommandWithBalancedBraces(body, '\\hspace', (inner) => {
                const cleaned = inner.trim();
                return `<span class="inline-block" style="width: ${cleaned}; min-width: 1em;"></span>`;
            });

            // Section headings (matches A-D and Roman numerals to avoid matching plain words like 'which')
            body = body.replace(/SECTION\s+([A-D]|[IVX]+)\b/gi, '<span class="text-xs sm:text-sm font-extrabold uppercase tracking-widest text-primary border-b-2 border-primary/20 pb-1">SECTION $1</span>');

            // Standard OR choices dividers
            body = body.replace(/\\hfill\s*\\textbf\{OR\}/gi, '<div class="text-center font-bold my-4 text-xs sm:text-sm text-secondary uppercase tracking-widest">— OR —</div>');
            body = body.replace(/\\textbf\{OR\}/gi, '<div class="text-center font-bold my-4 text-xs sm:text-sm text-secondary uppercase tracking-widest">— OR —</div>');

            // \centerline{...} — centered line, commonly used for "OR", section titles, etc.
            body = replaceCommandWithBalancedBraces(body, '\\centerline', (inner) => {
                const trimmed = inner.trim();
                // Special styling for OR separators
                if (/^\s*(\\textbf\{)?OR\}?\s*$/.test(trimmed) || trimmed === 'OR') {
                    return '<div class="text-center font-bold my-3 text-xs sm:text-sm text-secondary uppercase tracking-widest">— OR —</div>';
                }
                return `<div class="text-center my-2">${trimmed}</div>`;
            });
            // Fallback regex for any remaining \centerline{...} not caught by balanced-brace handler
            body = body.replace(/\\centerline\{([^}]*)\}/g, (match, inner) => {
                const trimmed = inner.trim();
                if (trimmed === 'OR' || trimmed === '\\textbf{OR}') {
                    return '<div class="text-center font-bold my-3 text-xs sm:text-sm text-secondary uppercase tracking-widest">— OR —</div>';
                }
                return `<div class="text-center my-2">${trimmed}</div>`;
            });

            // Split text by math delimiters to process non-math text formatting
            const mathRegex = /(\$\$[\s\S]*?\$\$|\$[\s\S]*?\$|(?<!\\)\\\[[\s\S]*?\\\]|(?<!\\)\\\([\s\S]*?\\\))/g;
            const parts = body.split(mathRegex);

            for (let i = 0; i < parts.length; i++) {
                if (i % 2 === 0) {
                    let text = parts[i];

                    // Spacing and breaks
                    text = text.replace(/\\\\\s*\[.*?\]/gi, '<br/>');
                    text = text.replace(/\\\\/gi, '<br/>');
                    text = text.replace(/\\smallskip/gi, '<div class="h-2"></div>');
                    text = text.replace(/\\medskip/gi, '<div class="h-4"></div>');
                    text = text.replace(/\\bigskip/gi, '<div class="h-6"></div>');
                    text = text.replace(/\\noindent/gi, '');

                    // LaTeX accents
                    text = text.replace(/\\\"o/g, 'ö');
                    text = text.replace(/\\\"O/g, 'Ö');
                    text = text.replace(/\\\'e/g, 'é');
                    text = text.replace(/\\\'E/g, 'É');
                    text = text.replace(/\\\`e/g, 'è');
                    text = text.replace(/\\\`E/g, 'È');
                    text = text.replace(/\\\"a/g, 'ä');
                    text = text.replace(/\\\"A/g, 'Ä');
                    text = text.replace(/\\\"u/g, 'ü');
                    text = text.replace(/\\\"U/g, 'Ü');
                    text = text.replace(/\\\"\{o\}/g, 'ö');
                    text = text.replace(/\\\"\{O\}/g, 'Ö');
                    text = text.replace(/\\\'\{e\}/g, 'é');
                    text = text.replace(/\\\'\{E\}/g, 'É');
                    text = text.replace(/\\\`\{e\}/g, 'è');
                    text = text.replace(/\\\`\{E\}/g, 'È');
                    text = text.replace(/\\\"\{a\}/g, 'ä');
                    text = text.replace(/\\\"\{A\}/g, 'Ä');
                    text = text.replace(/\\\"\{u\}/g, 'ü');
                    text = text.replace(/\\\"\{U\}/g, 'Ü');
                    text = text.replace(/\\r\{\}/g, '');

                    // Horizontal lines (rules) - solid dark lines like printed LaTeX
                    text = text.replace(/\\rule\{[0-9.]+\\linewidth\}\{.*?\}/gi, '<hr class="w-[80%] mx-auto border-neutral-800 my-4" />');
                    text = text.replace(/\\rule\{\\linewidth\}\{.*?\}/gi, '<hr class="border-neutral-800 my-4" />');
                    text = text.replace(/\\rule\{.*?\}\{.*?\}/gi, '<hr class="border-neutral-800 my-4" />');

                    // Page break indicators
                    text = text.replace(/\\newpage/gi, '<div class="relative my-8"><hr class="border-dashed border-neutral-300"/><span class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white px-3 text-[10px] uppercase tracking-wider text-neutral-400 font-semibold select-none">Page Break</span></div>');

                    // Clean up remaining \hfill by floating the text or adding padding
                    text = text.replace(/\\hfill\s*([^\n\r]+)/g, '<span class="float-right font-semibold">$1</span>');
                    text = text.replace(/\\hfill/gi, ' &nbsp;&nbsp; ');
                    text = text.replace(/\\qquad/gi, '&emsp;&emsp;');
                    text = text.replace(/\\quad/gi, '&emsp;');

                    // Escaped characters in text
                    text = text.replace(/\\%/g, '%');
                    text = text.replace(/\\&/g, '&');
                    text = text.replace(/\\_/g, '_');
                    text = text.replace(/\\#/g, '#');
                    text = text.replace(/~/g, ' ');

                    // Replace LaTeX dots/ellipsis
                    text = text.replace(/\\dots\{\}/g, '...');
                    text = text.replace(/\\dots/g, '...');
                    text = text.replace(/\\ldots\{\}/g, '...');
                    text = text.replace(/\\ldots/g, '...');

                    // Replace LaTeX quotes safely (only in text, not inside HTML tags)
                    text = text.replace(/([^<]*)(<[^>]*>)?/g, function(match, textPart, tagPart) {
                        if (textPart) {
                            textPart = textPart.replace(/``/g, '“');
                            textPart = textPart.replace(/''/g, '”');
                            textPart = textPart.replace(/`/g, '‘');
                            textPart = textPart.replace(/'/g, '’');
                        }
                        return (textPart || '') + (tagPart || '');
                    });

                    // Clear font size tags
                    text = text.replace(/\\small/gi, '');
                    text = text.replace(/\\normalsize/gi, '');

                    // Format Question headings (no saffron dot or bottom border lines)
                    text = text.replace(/<strong>Question\s*([0-9]+)\.?<\/strong>/gi, '<h3 class="font-bold text-sm sm:text-base text-primary mt-4 mb-2">Question $1</h3>');

                    parts[i] = text;
                }
            }

            let processedBody = parts.join('');

            // 9. Robust list environment parser supporting parts, romanparts, enumerate, and itemize (with nested stack)
            let listStack = [];
            const lines = processedBody.split('\n');
            let parsedHtml = '';

            for (let i = 0; i < lines.length; i++) {
                let line = lines[i];
                let trimmed = line.trim();

                // Check for list start
                let beginIdx = line.indexOf('\\begin{parts}');
                if (beginIdx === -1) beginIdx = line.indexOf('\\begin{romanparts}');
                if (beginIdx === -1) beginIdx = line.indexOf('\\begin{enumerate}');
                if (beginIdx === -1) beginIdx = line.indexOf('\\begin{itemize}');

                if (beginIdx !== -1) {
                    // Keep text preceding list start command on same line
                    const textBefore = line.substring(0, beginIdx);
                    if (textBefore.trim()) {
                        parsedHtml += textBefore + '\n';
                    }

                    const beginCmd = line.substring(beginIdx);
                    let listTag = 'ol';
                    let listClass = 'list-decimal';

                    if (beginCmd.includes('itemize')) {
                        listTag = 'ul';
                        listClass = 'list-disc';
                    } else if (beginCmd.includes('romanparts') || beginCmd.includes('label=(\\roman*)') || beginCmd.includes('label=\\roman*')) {
                        listClass = 'list-[lower-roman]';
                    } else if (beginCmd.includes('parts') || beginCmd.includes('label=(\\alph*)') || beginCmd.includes('label=\\alph*')) {
                        listClass = 'list-[lower-alpha]';
                    } else if (beginCmd.includes('label=\\arabic*')) {
                        listClass = 'list-decimal';
                    } else {
                        listClass = beginCmd.includes('parts') ? 'list-[lower-alpha]' : 'list-decimal';
                    }

                    listStack.push(listTag);
                    parsedHtml += `<${listTag} class="${listClass} pl-6 sm:pl-8 my-3 space-y-2">`;

                    // If there's text after the \begin{...} on the same line, append it
                    const matchBegin = beginCmd.match(/\\begin\{[a-zA-Z]+\}(?:\[.*?\])?/);
                    if (matchBegin) {
                        const textAfter = beginCmd.substring(matchBegin[0].length);
                        if (textAfter.trim()) {
                            parsedHtml += textAfter + '\n';
                        }
                    }
                    continue;
                }

                // Check for list end
                let endIdx = line.indexOf('\\end{parts}');
                if (endIdx === -1) endIdx = line.indexOf('\\end{romanparts}');
                if (endIdx === -1) endIdx = line.indexOf('\\end{enumerate}');
                if (endIdx === -1) endIdx = line.indexOf('\\end{itemize}');

                if (endIdx !== -1) {
                    // Keep text preceding list end command on same line
                    const textBefore = line.substring(0, endIdx);
                    if (textBefore.trim()) {
                        if (textBefore.trim().startsWith('\\item')) {
                            let itemContent = textBefore.replace('\\item', '').trim();
                            parsedHtml += `<li class="pl-2 text-xs sm:text-sm text-neutral-900 leading-relaxed">${itemContent}</li>`;
                        } else {
                            parsedHtml += textBefore + '\n';
                        }
                    }

                    const closedTag = listStack.pop() || 'ol';
                    parsedHtml += `</${closedTag}>`;

                    const endCmd = line.substring(endIdx);
                    const matchEnd = endCmd.match(/\\end\{[a-zA-Z]+\}/);
                    if (matchEnd) {
                        const textAfter = endCmd.substring(matchEnd[0].length);
                        if (textAfter.trim()) {
                            parsedHtml += textAfter + '\n';
                        }
                    }
                    continue;
                }

                // Check for item
                if (trimmed.startsWith('\\item')) {
                    let itemContent = line.replace('\\item', '');
                    while (i + 1 < lines.length) {
                        const nextLine = lines[i + 1].trim();
                        if (nextLine.startsWith('\\item') ||
                            nextLine.includes('\\begin{parts}') ||
                            nextLine.includes('\\begin{romanparts}') ||
                            nextLine.includes('\\begin{enumerate}') ||
                            nextLine.includes('\\begin{itemize}') ||
                            nextLine.includes('\\end{parts}') ||
                            nextLine.includes('\\end{romanparts}') ||
                            nextLine.includes('\\end{enumerate}') ||
                            nextLine.includes('\\end{itemize}')) {
                            break;
                        }
                        i++;
                        itemContent += ' ' + lines[i];
                    }
                    parsedHtml += `<li class="pl-2 text-xs sm:text-sm text-neutral-900 leading-relaxed">${itemContent.trim()}</li>`;
                    continue;
                }

                parsedHtml += line + '\n';
            }

            // 10. Final cleanup of trailing links at bottom
            const vfillIndex = parsedHtml.indexOf('\\vfill');
            if (vfillIndex !== -1) {
                parsedHtml = parsedHtml.substring(0, vfillIndex);
            }

            // Restore tikzpictures
            for (let i = 0; i < tikzPictures.length; i++) {
                const rawTikz = tikzPictures[i];
                const htmlTikz = `<div class="flex justify-center my-6"><script type="text/tikz">${rawTikz}<\/script></div>`;
                parsedHtml = parsedHtml.replace(`__TIKZ_PICTURE_${i}__`, htmlTikz);
            }

            // Restore verbatim blocks
            for (let i = 0; i < verbatimBlocks.length; i++) {
                parsedHtml = parsedHtml.replace(`__VERBATIM_BLOCK_${i}__`, verbatimBlocks[i]);
            }

            return parsedHtml;
        }

        // --- A4 PAGINATION AND RESPONSIVE SCALING LAYOUT ENGINE ---
        
module.exports = { parseLatex };