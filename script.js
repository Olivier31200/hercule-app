// Données à modifier
const prixDuJour = 2.46;
const prixVeille = 2.30; // Modifiez cette valeur pour tester

const stickerEl = document.getElementById('sticker');

function mettreAJourSticker(actuel, veille) {
    const variation = ((actuel - veille) / veille) * 100;
    const variationArrondie = variation.toFixed(2); // 2 décimales

    stickerEl.style.display = 'inline-block';

    if (variation > 0) {
        stickerEl.textContent = `+${variationArrondie}%`;
        stickerEl.classList.add('hausse');
    } else if (variation < 0) {
        stickerEl.textContent = `${variationArrondie}%`;
        stickerEl.classList.add('baisse');
    } else {
        stickerEl.textContent = `0%`;
        stickerEl.classList.add('neutre');
    }
}

// Exécution de la fonction
mettreAJourSticker(prixDuJour, prixVeille);
