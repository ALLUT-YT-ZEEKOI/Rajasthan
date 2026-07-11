const fs = require('fs');

let tilesHtml = fs.readFileSync('rajasthan-marbles-tiles.html', 'utf8');

const varsToAdd = `
      --shell: min(1280px, 92vw);
      --ease: cubic-bezier(.22, .61, .36, 1);
      --ease-out: cubic-bezier(.16, 1, .3, 1);
      --fog: rgba(233, 222, 188, .62);
      --fog-dim: rgba(233, 222, 188, .40);
      --line-dark: rgba(233, 222, 188, .14);
`;

// Insert the variables right before the end of the :root block
tilesHtml = tilesHtml.replace(/--maxw: 1280px;[\s]*\}/, '--maxw: 1280px;' + varsToAdd + '    }');

fs.writeFileSync('rajasthan-marbles-tiles.html', tilesHtml);
console.log('Fixed rajasthan-marbles-tiles.html');
