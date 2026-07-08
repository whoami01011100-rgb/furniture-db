// ============================================================
// configure.js — Configure Page ka JavaScript
// ============================================================
// Unit conversion support: ft (default), cm, m, mm
// Raw inputs show values in selected unit.
// Hidden inputs (name="length/width/height") always hold ft values.
// ============================================================

// Conversion factors → convert TO feet
var TO_FT = { ft: 1, cm: 0.0328084, m: 3.28084, mm: 0.00328084 };
// Conversion factors → convert FROM feet to display unit
var FROM_FT = { ft: 1, cm: 30.48, m: 0.3048, mm: 304.8 };

var currentUnit = 'ft';

// Round to reasonable decimal places per unit
function roundForUnit(val, unit) {
  if (unit === 'ft') return Math.round(val * 100) / 100;
  if (unit === 'm')  return Math.round(val * 1000) / 1000;
  return Math.round(val * 10) / 10; // cm, mm
}

// Convert a raw-input value (in currentUnit) → feet
function toFt(rawVal) {
  return parseFloat(rawVal) * TO_FT[currentUnit];
}

// Convert feet → current display unit
function fromFt(ftVal) {
  return roundForUnit(ftVal * FROM_FT[currentUnit], currentUnit);
}

// Update all unit labels and hidden ft fields
function updateLive() {
  var rL = parseFloat(document.getElementById('raw_length').value) || 0;
  var rW = parseFloat(document.getElementById('raw_width').value)  || 0;
  var rH = parseFloat(document.getElementById('raw_height').value) || 0;

  // Convert to ft for hidden fields (backend)
  document.getElementById('length').value = (rL * TO_FT[currentUnit]).toFixed(4);
  document.getElementById('width').value  = (rW * TO_FT[currentUnit]).toFixed(4);
  document.getElementById('height').value = (rH * TO_FT[currentUnit]).toFixed(4);

  // Update live display spans
  document.getElementById('dL').textContent = rL || '—';
  document.getElementById('dW').textContent = rW || '—';
  document.getElementById('dH').textContent = rH || '—';
}

// Called when user picks a new unit from the dropdown
function changeUnit(newUnit) {
  // Read current raw values and convert them to the new unit
  var rL = parseFloat(document.getElementById('raw_length').value) || 0;
  var rW = parseFloat(document.getElementById('raw_width').value)  || 0;
  var rH = parseFloat(document.getElementById('raw_height').value) || 0;

  // Convert: raw → ft → newUnit
  var ftL = rL * TO_FT[currentUnit];
  var ftW = rW * TO_FT[currentUnit];
  var ftH = rH * TO_FT[currentUnit];

  currentUnit = newUnit;

  // Set inputs to new unit values
  document.getElementById('raw_length').value = roundForUnit(ftL * FROM_FT[newUnit], newUnit);
  document.getElementById('raw_width').value  = roundForUnit(ftW * FROM_FT[newUnit], newUnit);
  document.getElementById('raw_height').value = roundForUnit(ftH * FROM_FT[newUnit], newUnit);

  // Update all unit label badges
  ['unit_L', 'unit_W', 'unit_H', 'dU_L', 'dU_W', 'dU_H'].forEach(function(id) {
    document.getElementById(id).textContent = newUnit;
  });

  // Update input labels
  document.getElementById('label_length').textContent = 'Length (' + newUnit + ')';
  document.getElementById('label_width').textContent  = 'Width / Depth (' + newUnit + ')';
  document.getElementById('label_height').textContent = 'Height (' + newUnit + ')';

  updateLive();
}

// "Use Standard" button — fills standard dimensions in current unit
function fillStandard() {
  // STD_L/W/H are always in feet (injected from Python)
  document.getElementById('raw_length').value = roundForUnit(STD_L * FROM_FT[currentUnit], currentUnit);
  document.getElementById('raw_width').value  = roundForUnit(STD_W * FROM_FT[currentUnit], currentUnit);
  document.getElementById('raw_height').value = roundForUnit(STD_H * FROM_FT[currentUnit], currentUnit);
  updateLive();
}

// Highlight selected Material / Finish card
function selectCard(radio, groupId) {
  document.querySelectorAll('#' + groupId + ' .radio-card').forEach(function(c) {
    c.classList.remove('selected');
  });
  radio.closest('.radio-card').classList.add('selected');
}

// Form submit → show loading state
document.getElementById('quoteForm').addEventListener('submit', function() {
  // Make sure hidden ft values are up to date
  updateLive();
  document.querySelector('.btn-text').style.display   = 'none';
  document.querySelector('.btn-loader').style.display = 'inline';
  document.getElementById('generateBtn').disabled     = true;
});

// Fix browser back-button cache issue
window.addEventListener('pageshow', function(e) {
  var btn       = document.getElementById('generateBtn');
  var btnText   = document.querySelector('.btn-text');
  var btnLoader = document.querySelector('.btn-loader');
  if (btn.disabled || btnLoader.style.display === 'inline') {
    btn.disabled            = false;
    btnText.style.display   = 'inline';
    btnLoader.style.display = 'none';
  }
});
