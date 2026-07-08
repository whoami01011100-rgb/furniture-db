// script.js — WoodCraft frontend interactions

// Stagger animation for grid cards
document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.cat-card, .item-card, .step-card');
  cards.forEach((card, i) => {
    card.style.animationDelay = `${i * 0.04}s`;
  });

  // Auto-animate bars on result page (trigger after render)
  document.querySelectorAll('.bar-fill').forEach(bar => {
    const w = bar.style.width;
    bar.style.width = '0%';
    setTimeout(() => { bar.style.width = w; }, 100);
  });
});
