/**
 * High-fidelity, zero-dependency HTML/CSS print-to-PDF utility.
 * Captures a DOM element by ID, clones it with all loaded page styles, 
 * injects print-specific overrides for styling (dark mode background, 
 * vector scaling, page break safety), and opens the print dialog.
 */
export const exportToPDF = (elementId: string, filename: string = 'roadmap.pdf'): Promise<void> => {
  return new Promise((resolve, reject) => {
    const element = document.getElementById(elementId);
    if (!element) {
      reject(new Error(`Element with id "${elementId}" not found.`));
      return;
    }

    // 1. Create temporary hidden iframe
    const iframe = document.createElement('iframe');
    iframe.style.position = 'fixed';
    iframe.style.right = '0';
    iframe.style.bottom = '0';
    iframe.style.width = '0';
    iframe.style.height = '0';
    iframe.style.border = '0';
    iframe.style.zIndex = '-9999';
    iframe.style.opacity = '0';
    document.body.appendChild(iframe);

    const doc = iframe.contentDocument || iframe.contentWindow?.document;
    if (!doc) {
      reject(new Error('Could not access iframe document.'));
      return;
    }

    // 2. Extract stylesheet links and dynamic style blocks from document
    const styles: string[] = [];

    // Capture dynamic CSSRules (especially useful in Vite dev mode HMR stylesheets)
    for (let i = 0; i < document.styleSheets.length; i++) {
      try {
        const sheet = document.styleSheets[i];
        const rules = sheet.cssRules || sheet.rules;
        if (rules) {
          const cssText = Array.from(rules).map(rule => rule.cssText).join('\n');
          styles.push(`<style>${cssText}</style>`);
        }
      } catch (e) {
        // Fallback for cross-origin CDN stylesheets
        const sheet = document.styleSheets[i];
        if (sheet.href) {
          styles.push(`<link rel="stylesheet" href="${sheet.href}">`);
        }
      }
    }

    // Ensure all direct links/styles are caught as a backup
    document.querySelectorAll('link[rel="stylesheet"], style').forEach((el) => {
      styles.push(el.outerHTML);
    });

    // 3. Inject printing overrides to enforce A4 size, dark mode colors, and print scaling
    const printOverrideStyles = `
      <style>
        /* PDF specific overrides */
        @media print {
          @page {
            size: A4 portrait;
            margin: 15mm;
          }
          * {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
            color-adjust: exact !important;
          }
          html, body {
            background-color: #080808 !important;
            background: #080808 !important;
            color: #e4e4e7 !important;
            margin: 0 !important;
            padding: 0 !important;
            min-height: 100% !important;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
          }
          /* Print Wrapper setup */
          #print-wrapper {
            background-color: #080808 !important;
            min-height: 100vh !important;
            width: 100% !important;
            padding: 0 !important;
            box-sizing: border-box !important;
          }
          /* Prevent cards from being split across page boundaries */
          .group {
            page-break-inside: avoid !important;
            break-inside: avoid !important;
            margin-bottom: 16px !important;
          }
          /* Hide print trigger buttons or interactive selectors */
          .no-print {
            display: none !important;
          }
        }
      </style>
    `;

    // Grab cloned inner elements, ignoring any print-trigger controls
    const clonedElement = element.cloneNode(true) as HTMLElement;
    
    // Remove export buttons inside the printed content if any are present
    clonedElement.querySelectorAll('.no-print').forEach((el) => el.remove());

    const elementHTML = clonedElement.outerHTML;

    // 4. Populate dynamic print page structure inside the isolated iframe document
    doc.open();
    doc.write(`
      <!DOCTYPE html>
      <html>
        <head>
          <title>${filename.replace('.pdf', '')}</title>
          ${styles.join('\n')}
          ${printOverrideStyles}
        </head>
        <body style="background-color: #080808; margin: 0; padding: 0;">
          <div id="print-wrapper">
            ${elementHTML}
          </div>
        </body>
      </html>
    `);
    doc.close();

    // 5. Trigger browser native printing dialog after layout/font parsing
    iframe.contentWindow?.focus();
    
    setTimeout(() => {
      try {
        iframe.contentWindow?.print();
        resolve();
      } catch (err) {
        reject(err);
      } finally {
        // Graceful cleanup of iframe DOM resources
        setTimeout(() => {
          if (document.body.contains(iframe)) {
            document.body.removeChild(iframe);
          }
        }, 1500);
      }
    }, 350);
  });
};
