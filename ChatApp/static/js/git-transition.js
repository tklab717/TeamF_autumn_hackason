function openGitInNewTab() {
  // 新しいブラウザタブで開きたいURLを指定
  const url = "https://github.com/RT-F-HACKATHON/teamF_app.git";
  window.open(url, "_blank");
}
// GITへ移行ボタンと集まれボタンの説明
document.addEventListener("DOMContentLoaded", (event) => {
  const buttons = document.querySelectorAll(".button");

  buttons.forEach((button) => {
    button.addEventListener("mouseenter", showTooltip);
    button.addEventListener("mouseleave", hideTooltip);
  });

  function showTooltip(event) {
    const tooltip = document.createElement("div");
    tooltip.className = "tooltip";
    tooltip.textContent = event.currentTarget.getAttribute("data-tooltip");
    document.body.appendChild(tooltip);

    const buttonRect = event.currentTarget.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();

    tooltip.style.left = `${
      buttonRect.left + (buttonRect.width - tooltipRect.width) / 2
    }px`;
    tooltip.style.top = `${buttonRect.top - tooltipRect.height - 5}px`;
  }

  function hideTooltip(event) {
    document.querySelectorAll(".tooltip").forEach((tooltip) => {
      tooltip.remove();
    });
  }
});
