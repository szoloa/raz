const fileSelector = document.getElementById("fileSelector");

const openButton = document.getElementById("openRandomWebsite");

const files = ["rurl.txt", "rurlamv_2023.txt", "rurlamv_2025.txt"];

files.forEach(file => {
  const option = document.createElement("option");
  option.value = file;
  option.textContent = file;
  fileSelector.appendChild(option);
});

var index = fileSelector.selectedIndex;

var filename = fileSelector.options[index].value;

openButton.addEventListener("click", () => {
  const selectedIndex = fileSelector.selectedIndex; // Get current selected index
  const filename = fileSelector.options[selectedIndex].value; // Get current selected value
  chrome.runtime.sendMessage({ action: 'openRandomWebsite', params: { filename } }); // Pass filename as parameter
});