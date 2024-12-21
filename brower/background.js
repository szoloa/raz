chrome.runtime.onInstalled.addListener(() => {
  console.log("Random Website Opener Extension Installed");
});

// Listen for the message from popup.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'openRandomWebsite') {
    // Get the random website and open it
    getRandomWebsite().then(url => {
      chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        chrome.tabs.update(tabs[0].id, { url: url });
      });
    }).catch(error => {
      console.error("Error opening random website:", error);
    });
  }
});

chrome.commands.onCommand.addListener((command) => {
  if (command === "open-random-website") {
    getRandomWebsite().then(url => {
      chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        chrome.tabs.update(tabs[0].id, { url: url });
      });
    }).catch(error => {
      console.error("Error opening random website:", error);
    });
  }
});

// Fetch and return a random website from the list
function getRandomWebsite() {
  return fetch(chrome.runtime.getURL('rurl_2023.txt'))
    .then(response => response.text())
    .then(data => {
      const websites = data.split('\n').filter(line => line.trim() !== '');
      const randomIndex = Math.floor(Math.random() * websites.length);
      return websites[randomIndex].trim();
    });
}