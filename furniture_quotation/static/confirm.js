// ============================================================
// confirm.js — Confirm & Save Button Logic
// ============================================================
// Ye file result.html ke saath kaam karti hai.
//
// Kya karta hai:
//   confirmQuotation() → Flask /confirm route ko call karta hai
//                       → MySQL mein save hota hai
//                       → PDF download button dikhata hai
//
// Data flow:
//   Browser → POST /confirm → app.py → database.py → MySQL
//   MySQL se ID aati hai → Browser mein PDF link update hoti hai
// ============================================================

function confirmQuotation() {
  // Agar already confirm ho chuka hai toh dobara mat karo
  if (IS_CONFIRMED) return;

  // Button ko "Saving..." state mein daalo
  var btn     = document.getElementById('confirmBtn');
  var btnText = btn.querySelector('.btn-text');
  var loader  = btn.querySelector('.btn-loader');

  btnText.style.display = 'none';
  loader.style.display  = 'inline';
  btn.disabled          = true;

  // Flask /confirm route ko POST request bhejo
  // Flask session mein pehle se data hai (generate route ne store kiya tha)
  fetch('/confirm', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  })
  .then(function(response) {
    return response.json();
  })
  .then(function(data) {
    if (data.success) {
      // SUCCESS → MySQL mein save ho gaya!
      var qid = data.quote_id;

      // Page refresh karo confirmed=True ke saath
      // (Naya URL banao jisse confirmed state dikhaye)
      showConfirmedState(qid);

    } else {
      // ERROR → server ne error diya
      alert('Error saving: ' + (data.error || 'Unknown error'));
      // Button reset karo
      btnText.style.display = 'inline';
      loader.style.display  = 'none';
      btn.disabled          = false;
    }
  })
  .catch(function(err) {
    // Network error (server band hai etc.)
    alert('Connection error. Is Flask server running?\n' + err);
    btnText.style.display = 'inline';
    loader.style.display  = 'none';
    btn.disabled          = false;
  });
}

// Confirm hone ke baad page UI update karo
// (page reload ki jagah in-place update karte hain — faster!)
function showConfirmedState(qid) {
  // 1. Confirm button ko replace karo PDF button se
  var actionsDiv = document.querySelector('.quote-actions');
  actionsDiv.innerHTML = `
    <a href="/pdf/${qid}" class="btn-pdf" id="pdfBtn">
      &#x1F4C4; Download PDF
    </a>
    <a href="/" class="btn-primary">+ New Quotation</a>
  `;

  // 2. Status badge update karo
  var previewBadge = document.querySelector('.badge-preview');
  if (previewBadge) {
    previewBadge.className  = 'badge-confirmed';
    previewBadge.innerHTML  = '&#x2714; Saved to Database #' + qid;
  }

  // 3. Quote reference update karo
  var quoteRef = document.querySelector('.quote-ref');
  if (quoteRef) {
    quoteRef.textContent = 'Saved #' + qid;
    quoteRef.style.color = '';
  }

  // 4. Page title update karo
  document.title = 'Quotation #' + qid + ' — WoodCraft';

  // 5. Global variable update karo
  IS_CONFIRMED = true;
  QUOTE_ID     = qid;

  // 6. Success toast dikhao
  showToast('✅ Quotation #' + qid + ' saved to MySQL database!');
}

// Toast notification (chhoti si popup message)
function showToast(message) {
  // Agar pehle se toast hai toh hatao
  var existing = document.getElementById('toastMsg');
  if (existing) existing.remove();

  var toast = document.createElement('div');
  toast.id = 'toastMsg';
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed;
    bottom: 2rem; right: 2rem;
    background: linear-gradient(135deg, #22C55E, #16A34A);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    font-weight: 600;
    font-size: 0.95rem;
    box-shadow: 0 8px 32px rgba(34,197,94,0.4);
    z-index: 9999;
    animation: slideIn 0.3s ease;
    font-family: 'Inter', sans-serif;
  `;

  // Slide-in animation add karo
  if (!document.getElementById('toastStyle')) {
    var styleEl = document.createElement('style');
    styleEl.id = 'toastStyle';
    styleEl.textContent = `
      @keyframes slideIn {
        from { transform: translateX(120%); opacity: 0; }
        to   { transform: translateX(0);   opacity: 1; }
      }
      @keyframes slideOut {
        from { transform: translateX(0);   opacity: 1; }
        to   { transform: translateX(120%); opacity: 0; }
      }
    `;
    document.head.appendChild(styleEl);
  }

  document.body.appendChild(toast);

  // 4 second baad automatically hide karo
  setTimeout(function() {
    toast.style.animation = 'slideOut 0.3s ease forwards';
    setTimeout(function() { toast.remove(); }, 300);
  }, 4000);
}
