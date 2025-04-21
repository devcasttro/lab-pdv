// Ativar/desativar menu colapsável em telas pequenas
document.getElementById('menu-toggle').addEventListener('click', function () {
  const menuList = document.querySelector('.menu ul');
  if (menuList) {
    menuList.classList.toggle('show');
  }
});

// Navegação suave para âncoras
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      window.scrollTo({
        top: target.offsetTop - 60,
        behavior: "smooth"
      });
    }

    // Esconder menu no mobile após clique
    const menuList = document.querySelector('.menu ul');
    if (menuList && menuList.classList.contains('show')) {
      menuList.classList.remove('show');
    }
  });
});

// Tooltip simples para SVGs com <title>
document.querySelectorAll("svg title").forEach(title => {
  const parent = title.parentElement;
  const tooltipText = title.textContent;
  title.remove();

  parent.addEventListener("mouseenter", e => {
    const tooltip = document.createElement("div");
    tooltip.className = "custom-tooltip";
    tooltip.textContent = tooltipText;
    tooltip.style.position = "absolute";
    tooltip.style.top = `${e.pageY + 10}px`;
    tooltip.style.left = `${e.pageX + 10}px`;
    tooltip.style.background = "#000";
    tooltip.style.color = "#fff";
    tooltip.style.padding = "5px 10px";
    tooltip.style.fontSize = "12px";
    tooltip.style.borderRadius = "4px";
    tooltip.style.zIndex = "9999";
    tooltip.id = "svg-tooltip";
    document.body.appendChild(tooltip);
  });

  parent.addEventListener("mouseleave", () => {
    const tooltip = document.getElementById("svg-tooltip");
    if (tooltip) tooltip.remove();
  });

  parent.addEventListener("mousemove", e => {
    const tooltip = document.getElementById("svg-tooltip");
    if (tooltip) {
      tooltip.style.top = `${e.pageY + 10}px`;
      tooltip.style.left = `${e.pageX + 10}px`;
    }
  });
});
