document.getElementById("openRandomWebsite").addEventListener("click", () => {
    chrome.runtime.sendMessage({ action: 'openRandomWebsite' });
  });
  