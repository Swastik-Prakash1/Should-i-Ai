document.getElementById("analyzeBtn").addEventListener("click", async () => {
  document.getElementById("result").innerText = "Analyzing reviews...";

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: async () => {
      let reviewElements = document.querySelectorAll(".review-text-content span");
      let reviews = [];
      reviewElements.forEach(el => {
        let text = el.innerText.trim();
        if (text.length > 0) reviews.push(text);
      });

      if (reviews.length === 0) return "No reviews found.";

      let res = await fetch("http://127.0.0.1:5000/analyze_reviews", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reviews })
      });

      let data = await res.json();
      return data.summary.verdict;
    }
  }).then(injectionResults => {
    const verdict = injectionResults[0].result;
    document.getElementById("result").innerText = verdict;
  }).catch(err => {
    document.getElementById("result").innerText = "Error fetching data!";
    console.error(err);
  });
});
