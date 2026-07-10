/* 3D Image Lab — 全局交互脚本 */

/* ========== 1. 导航栏：滚动阴影 + 移动端菜单 ========== */
document.addEventListener('DOMContentLoaded', () => {
  // 滚动阴影
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    });
  }

  // 移动端菜单切换
  const menuToggle = document.querySelector('.menu-toggle');
  const navMenu = document.querySelector('.nav-menu');
  if (menuToggle && navMenu) {
    menuToggle.addEventListener('click', () => {
      navMenu.classList.toggle('open');
    });
    // 点击导航链接后关闭菜单
    navMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => navMenu.classList.remove('open'));
    });
  }

  // 画廊自动轮播
  if (document.querySelector('.hero-gallery')) {
    startGalleryAutoPlay();
  }
});

/* ========== 2. 画廊轮播 ========== */
let galleryIndex = 0;
let galleryTimer = null;

function gallerySlide(dir) {
  const slides = document.querySelector('.hero-gallery .slides');
  if (!slides) return;
  const total = slides.children.length;
  galleryIndex = (galleryIndex + dir + total) % total;
  updateGallery();
  resetGalleryAutoPlay();
}

function galleryGo(n) {
  galleryIndex = n;
  updateGallery();
  resetGalleryAutoPlay();
}

function updateGallery() {
  const slides = document.querySelector('.hero-gallery .slides');
  const dots = document.querySelectorAll('.hero-gallery .dot');
  if (!slides) return;
  slides.style.transform = `translateX(-${galleryIndex * 100}%)`;
  dots.forEach((dot, i) => dot.classList.toggle('active', i === galleryIndex));
}

function startGalleryAutoPlay() {
  galleryTimer = setInterval(() => gallerySlide(1), 5000);
}

function resetGalleryAutoPlay() {
  clearInterval(galleryTimer);
  startGalleryAutoPlay();
}

/* ========== 3. Publications Tab 切换 ========== */
function switchPubTab(tab) {
  // 切换按钮高亮
  document.querySelectorAll('.pub-tab').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tab);
  });
  // 切换面板
  document.querySelectorAll('.pub-panel').forEach(panel => {
    panel.classList.toggle('active', panel.id === `panel-${tab}`);
  });
}

/* ========== 4. Team Tab 切换 ========== */
function switchTeamTab(tab) {
  document.querySelectorAll('.team-tab').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tab);
  });
  document.querySelectorAll('.team-panel').forEach(panel => {
    panel.classList.toggle('active', panel.id === `panel-${tab}`);
  });
}


/* ========== 5. 专利列表（始终展开） ========== */

/* ========== 6. 平滑滚动（锚点链接）========== */
document.addEventListener('click', (e) => {
  const anchor = e.target.closest('a[href^="#"]');
  if (!anchor) return;
  const target = document.querySelector(anchor.getAttribute('href'));
  if (target) {
    e.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
});

/* ========== 7. 研究方向（Grid布局，无需轮播JS） ========== */