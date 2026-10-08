// Retain historical fragments (for example portfolio.html#amazonia).
const refresh = document.querySelector('meta[http-equiv="refresh"]');
const destination = refresh?.content.split('url=')[1];
if (destination?.startsWith('/')) window.location.replace(destination + window.location.hash);
