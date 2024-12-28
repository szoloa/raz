const fileSelector = document.getElementById("fileSelector");
// const randomButton = document.getElementById("randomButtonWebsite");
const openButton = document.getElementById("openRandomWebsite");
// Example file list
const files = ["rurl.txt", "rurlamv_2023.txt", "rurlamv_2025.txt"];

// Populate the dropdown menu
files.forEach(file => {
  const option = document.createElement("option");
  option.value = file;
  option.textContent = file;
  fileSelector.appendChild(option);
});

var index = fileSelector.selectedIndex;
//获取选中的值
var filename = fileSelector.options[index].value;

// randomButton.addEventListener("click", () => {
//   const randomFile = files[Math.floor(Math.random() * files.length)];
//   alert(`Randomly selected file: ${randomFile}`);
// });

// document.getElementById("openRandomWebsite").addEventListener("click", () => {
//   chrome.runtime.sendMessage({ action: 'openRandomWebsite', params: filename });
// });

openButton.addEventListener("click", () => {
  const selectedIndex = fileSelector.selectedIndex; // Get current selected index
  const filename = fileSelector.options[selectedIndex].value; // Get current selected value
  chrome.runtime.sendMessage({ action: 'openRandomWebsite', params: { filename } }); // Pass filename as parameter
});