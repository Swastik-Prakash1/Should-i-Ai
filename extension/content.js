// content.js - injected into Amazon product pages
console.log("✅ Content script loaded successfully");

// Helper: extract product data
function extractProductData() {
  const titleElement = document.getElementById("productTitle");
  const ratingElement = document.querySelector(".a-icon-alt");
  const reviewElements = document.querySelectorAll(".review-text-content span");

  const title = titleElement ? titleElement.innerText.trim() : "Unknown Product";
  const rating = ratingElement ? parseFloat(ratingElement.innerText) : null;

  const reviews = [];
  reviewElements.forEach((el) => {
    const txt = el.innerText && el.innerText.trim();
    if (txt) reviews.push(txt);
  });

  console.log("📦 Extracted product data:", { title, rating, reviews_count: reviews.length });
  return { title, rating, reviews };
}

// Send product data to your Flask backend
async function analyzeProduct(data) {
  try {
    console.log("🚀 Sending product data to backend:", data);
    // Keep endpoint exactly as you had it in content.js
    const response = await fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) throw new Error("Failed to fetch trust score from backend");
    const result = await response.json();
    console.log("✅ Trust analysis result:", result);
    injectProductPanel(result);
  } catch (error) {
    console.error("❌ Error during backend call:", error);
    injectErrorPanel(error);
  }
}

// Remove existing injected panel (if any)
function removeExistingPanel() {
  const existing = document.getElementById("should-i-panel");
  if (existing) existing.remove();
}

// Main injection: create a panel under the product title area
function injectProductPanel(result) {
  removeExistingPanel();

  // Find where to insert: ideally below the product title.
  // productTitle is an id on an element inside the title container.
  const titleEl = document.getElementById("productTitle");
  if (!titleEl) {
    console.warn("Could not find productTitle element to attach panel.");
    return;
  }

  // Find nearest container to insert after (some Amazon layouts place #productTitle inside an h1)
  const insertAfter = titleEl.closest("#title") || titleEl.parentElement;

  // Create panel
  const panel = document.createElement("div");
  panel.id = "should-i-panel";
  panel.setAttribute("data-source", "should-i-extension");
  panel.style.boxSizing = "border-box";
  panel.style.marginTop = "12px";
  panel.style.padding = "10px";
  panel.style.display = "flex";
  panel.style.alignItems = "flex-start";
  panel.style.gap = "12px";
  panel.style.border = "1px solid #e6e6e6";
  panel.style.borderRadius = "8px";
  panel.style.background = "#fff";
  panel.style.boxShadow = "0 1px 6px rgba(16,24,40,0.06)";
  panel.style.maxWidth = "980px"; // prevent overflow on desktop
  panel.style.fontFamily = "Arial, Helvetica, sans-serif";
  panel.style.fontSize = "14px";
  panel.style.color = "#111827";

  // Determine verdict and image
  const genuine = Number(result.genuine_count || 0);
  const fake = Number(result.fake_count || 0);
  const score = result.trust_score ?? "N/A";

  let state = "mixed";
  if (genuine > fake) state = "trust";
  else if (fake > genuine) state = "fake";
  else state = "suspicious";

  // Map state -> asset
  const assetMap = {
    trust: chrome.runtime.getURL("assets/trust.png"),
    fake: chrome.runtime.getURL("assets/fake.png"),
    suspicious: chrome.runtime.getURL("assets/suspicious.png"),
  };
  const imgSrc = assetMap[state] || assetMap["suspicious"];

  // Left column: image
  const left = document.createElement("div");
  left.style.flex = "0 0 80px";
  left.style.display = "flex";
  left.style.justifyContent = "center";
  left.style.alignItems = "center";

  const img = document.createElement("img");
  img.src = imgSrc;
  img.alt = `Trust: ${state}`;
  img.style.maxWidth = "64px";
  img.style.maxHeight = "64px";
  img.style.objectFit = "contain";
  img.style.display = "block";
  left.appendChild(img);

  // Right column: details
  const right = document.createElement("div");
  right.style.flex = "1 1 auto";

  // Header row: score and verdict
  const header = document.createElement("div");
  header.style.display = "flex";
  header.style.justifyContent = "space-between";
  header.style.alignItems = "center";
  header.style.gap = "12px";

  const title = document.createElement("div");
  title.style.fontSize = "15px";
  title.style.fontWeight = "700";
  title.innerText = state === "trust" ? "Trusted product" : state === "fake" ? "Likely fake / suspicious" : "Mixed reviews";

  const scoreEl = document.createElement("div");
  scoreEl.style.fontWeight = "800";
  scoreEl.style.fontSize = "16px";
  scoreEl.innerText = `Trust Score: ${score}`;

  header.appendChild(title);
  header.appendChild(scoreEl);

  // Counts row
  const counts = document.createElement("div");
  counts.style.marginTop = "6px";
  counts.innerHTML = `
    <div> Genuine reviews: <b>${genuine}</b> &nbsp; • &nbsp; Fake reviews: <b>${fake}</b> </div>
    <div style="margin-top:6px; color:#6b7280; font-size:13px;">${result.short_reason ?? ""}</div>
  `;

  // Small footer / CTA
  const footer = document.createElement("div");
  footer.style.marginTop = "8px";
  footer.style.display = "flex";
  footer.style.justifyContent = "space-between";
  footer.style.alignItems = "center";

  const conclusionText = document.createElement("div");
  conclusionText.style.fontWeight = "700";
  conclusionText.style.fontSize = "13px";
  if (state === "trust") {
    conclusionText.style.color = "#16a34a"; // green
    conclusionText.innerText = "✅ This product seems genuine. You can consider buying it.";
  } else if (state === "fake") {
    conclusionText.style.color = "#dc2626"; // red
    conclusionText.innerText = "❌ High risk of fake reviews. Consider avoiding this product.";
  } else {
    conclusionText.style.color = "#b45309"; // amber
    conclusionText.innerText = "⚠️ Mixed signals — proceed with caution.";
  }

  // small link to open popup (optional) - uses extension action
  const more = document.createElement("a");
  more.href = "#";
  more.style.fontSize = "13px";
  more.style.color = "#2563eb";
  more.style.textDecoration = "none";
  more.innerText = "See more details";
  more.addEventListener("click", (e) => {
    e.preventDefault();
    // open the extension popup (action) — this works as a hint for users
    // Note: chrome.action.openPopup is available in MV3 but may require permissions; fallback to showing a small alert.
    if (chrome && chrome.action && chrome.action.openPopup) {
      try { chrome.action.openPopup(); } catch (err) { window.alert("Open extension from toolbar for more details."); }
    } else {
      window.alert("Open extension from toolbar for more details.");
    }
  });

  footer.appendChild(conclusionText);
  footer.appendChild(more);

  // Put everything together
  right.appendChild(header);
  right.appendChild(counts);
  right.appendChild(footer);

  panel.appendChild(left);
  panel.appendChild(right);

  // Insert panel into page (after title container)
  if (insertAfter && insertAfter.parentNode) {
    insertAfter.parentNode.insertBefore(panel, insertAfter.nextSibling);
    console.log("🏷️ Inserted Should I? panel under product title");
  } else {
    // fallback: append to body
    document.body.insertBefore(panel, document.body.firstChild);
    console.log("🏷️ Inserted Should I? panel at top of body (fallback)");
  }
}

// Inject a small error panel if backend fails
function injectErrorPanel(error) {
  removeExistingPanel();
  const titleEl = document.getElementById("productTitle");
  const insertAfter = titleEl ? (titleEl.closest("#title") || titleEl.parentElement) : null;

  const panel = document.createElement("div");
  panel.id = "should-i-panel";
  panel.style.marginTop = "12px";
  panel.style.padding = "8px";
  panel.style.border = "1px solid #f3c6c6";
  panel.style.borderRadius = "6px";
  panel.style.background = "#fff7f7";
  panel.style.color = "#7f1d1d";
  panel.style.fontFamily = "Arial, sans-serif";
  panel.innerText = "Should I? — Error contacting analysis backend. See console for details.";

  if (insertAfter && insertAfter.parentNode) insertAfter.parentNode.insertBefore(panel, insertAfter.nextSibling);
  else document.body.insertBefore(panel, document.body.firstChild);
}

// Main run
(function () {
  const productData = extractProductData();
  if (productData.reviews.length > 0) {
    analyzeProduct(productData);
  } else {
    console.warn("⚠️ No reviews found on this product page.");
    // Optionally show a small hint panel that no reviews were found
    // injectErrorPanel({ message: "No reviews found." });
  }
})();
