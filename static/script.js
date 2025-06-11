// Initialize immediately to reduce delay
console.log("Script.js started executing at:", new Date().toISOString());

// Initialize Particles.js
particlesJS('particles-js', {
  particles: {
    number: { value: 80, density: { enable: true, value_area: 800 } },
    color: { value: ['#1E90FF'] },
    shape: { type: 'circle' },
    opacity: { value: 0.5, random: true },
    size: { value: 3, random: true },
    line_linked: { enable: true, distance: 150, color: '#1E90FF', opacity: 0.4, width: 1 },
    move: { enable: true, speed: 2, direction: 'none', random: true, straight: false, out_mode: 'out', bounce: false }
  },
  interactivity: {
    detect_on: 'canvas',
    events: { onhover: { enable: true, mode: 'repulse' }, onclick: { enable: true, mode: 'push' }, resize: true },
    modes: { repulse: { distance: 100, duration: 0.4 }, push: { particles_nb: 4 } }
  },
  retina_detect: true
});

// Glowing Cursor Trail
const canvas = document.getElementById('cursor-trail');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const trails = [];
window.addEventListener('mousemove', (e) => {
  trails.push({ x: e.clientX, y: e.clientY, life: 1 });
});
function animateTrail() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  trails.forEach((trail, index) => {
    ctx.beginPath();
    ctx.arc(trail.x, trail.y, 5 * trail.life, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(30, 144, 255, ${trail.life})`;
    ctx.fill();
    trail.life -= 0.02;
    if (trail.life <= 0) trails.splice(index, 1);
  });
  requestAnimationFrame(animateTrail);
}
animateTrail();
window.addEventListener('resize', () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});

// GSAP Animations
gsap.registerPlugin(ScrollTrigger);

// Animate the static text "Hi, I'm B Chaitanya Reddy" and its siblings
gsap.fromTo('.animate-slide-in', 
  { y: 100, opacity: 0 }, 
  { y: 0, opacity: 1, duration: 1.2, ease: 'power3.out', onComplete: () => {
    document.querySelector('.animate-slide-in').style.opacity = '1'; // Ensure final state
  }}
);

// Animate the image in the hero section
gsap.fromTo('.animate-fade-in',
  { opacity: 0 },
  { opacity: 1, duration: 1.5, ease: 'power3.out', onComplete: () => {
    document.querySelector('.animate-fade-in').style.opacity = '1'; // Ensure final state
  }}
);

// Animate stat cards on scroll
gsap.from('.stat-card', {
  scrollTrigger: { trigger: '#about', start: 'top 80%' },
  y: 50,
  opacity: 0,
  duration: 0.8,
  stagger: 0.2,
  ease: 'power3.out'
});

// Navigation Bar
const menuToggle = document.getElementById('menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');
menuToggle.addEventListener('click', () => {
  mobileMenu.classList.toggle('hidden');
  menuToggle.querySelector('i').classList.toggle('fa-bars');
  menuToggle.querySelector('i').classList.toggle('fa-times');
});

// Smooth Scrolling
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    mobileMenu.classList.add('hidden');
    menuToggle.querySelector('i').classList.add('fa-bars');
    menuToggle.querySelector('i').classList.remove('fa-times');
    document.querySelector(link.getAttribute('href')).scrollIntoView({ behavior: 'smooth' });
  });
});

// Theme Toggle (Disabled since theme switching isn't implemented)
const themeToggle = document.getElementById('theme-toggle');
themeToggle.addEventListener('click', () => {
  // Theme switching not implemented
});

// Back to Top Button
const backToTop = document.getElementById('back-to-top');
window.addEventListener('scroll', () => {
  backToTop.classList.toggle('hidden', window.scrollY < 500);
});
backToTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Ripple Effect for Buttons
document.querySelectorAll('.ripple').forEach(btn => {
  btn.addEventListener('click', (e) => {
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const ripple = document.createElement('span');
    ripple.style.left = `${x}px`;
    ripple.style.top = `${y}px`;
    ripple.classList.add('ripple-effect');
    btn.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  });
});

// Fetch Data Helper
const fetchData = async (url, elementId, renderCallback) => {
  try {
    console.log(`Fetching data from ${url}`);
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    console.log(`Fetched data from ${url}:`, data);
    const container = document.getElementById(elementId);
    if (!container) throw new Error(`Container with ID ${elementId} not found`);
    renderCallback(data, container);
  } catch (error) {
    console.error(`Error fetching ${url}:`, error);
    document.getElementById(elementId).innerHTML = '<p class="text-red-500">Error loading data. Please try again later.</p>';
  }
};

// Render Skills with Circular Progress
fetchData('/api/skills', 'skills-grid', (data, container) => {
  console.log('Rendering skills data:', data);
  container.innerHTML = '';
  data.forEach(category => {
    const card = document.createElement('div');
    card.className = 'skill-card rounded-xl hover:scale-105 transition-transform';
    card.style.opacity = '1';
    card.style.display = 'block';
    card.innerHTML = `
      <i class="fas fa-${category.icon} mb-2"></i>
      <h3 class="mb-4">${category.title}</h3>
      <div class="space-y-3">
        ${category.skills.map(skill => `
          <div class="skill-item">
            <span>${skill.name}</span>
            <div class="progress-circle-container">
              <div class="progress-circle-bg"></div>
              <svg class="progress-circle">
                <circle cx="20" cy="20" r="18" stroke="#E5E5E5" stroke-width="4" fill="none" />
                <circle class="progress-fill" cx="20" cy="20" r="18" stroke="#1E90FF" stroke-width="4" fill="none" stroke-dasharray="0 113" />
              </svg>
              <span class="progress-percentage">${skill.proficiency}%</span>
            </div>
          </div>
        `).join('')}
      </div>
    `;
    container.appendChild(card);
    console.log(`Rendered skill card for ${category.title}`);
    // Animate the circular progress
    card.querySelectorAll('.progress-fill').forEach(circle => {
      const proficiency = circle.parentElement.parentElement.querySelector('.progress-percentage').textContent.replace('%', '');
      const circumference = 2 * Math.PI * 18; // Circumference of the circle (r=18)
      const offset = circumference * (proficiency / 100);
      gsap.to(circle, {
        scrollTrigger: { 
          trigger: card, 
          start: 'left 80%',
          end: 'right 20%',
          scrub: true
        },
        strokeDasharray: `${offset} 113`,
        duration: 1.5,
        ease: 'power3.out'
      });
    });
  });
});

// Render Achievements
fetchData('/api/achievements', 'achievements-grid', (data, container) => {
  data.forEach(achievement => {
    const card = document.createElement('div');
    card.className = 'achievement-card glassmorphic p-6 rounded-xl hover:scale-105 transition-transform';
    card.setAttribute('data-tilt', '');
    card.setAttribute('data-tilt-max', '10');
    card.innerHTML = `
      <div class="flex items-start space-x-4">
        <div class="icon-wrapper p-3 glassmorphic rounded-full">
          <i class="fas fa-${achievement.icon} text-primary-blue glow"></i>
        </div>
        <div>
          <h3 class="text-lg font-orbitron text-primary-blue glow">${achievement.title}</h3>
          <p class="text-sm text-primary-blue">${achievement.organization}</p>
          <p class="text-gray-300">${achievement.description}</p>
        </div>
      </div>
    `;
    container.appendChild(card);
    VanillaTilt.init(card);
    gsap.from(card, { scrollTrigger: { trigger: card, start: 'top 80%' }, y: 50, opacity: 0, duration: 1, ease: 'power3.out' });
  });
});

// Render Hobbies
fetchData('/api/hobbies', 'hobbies-grid', (data, container) => {
  data.forEach(hobby => {
    const card = document.createElement('div');
    card.className = 'hobby-card glassmorphic p-6 rounded-xl hover:scale-105 transition-transform';
    card.setAttribute('data-tilt', '');
    card.setAttribute('data-tilt-max', '10');
    card.innerHTML = `
      <div class="flex items-center space-x-4">
        <div class="icon-wrapper p-3 glassmorphic rounded-full">
          <i class="fas fa-${hobby.icon} text-primary-blue glow"></i>
        </div>
        <div>
          <h3 class="text-lg font-orbitron text-primary-blue glow">${hobby.title}</h3>
          <p class="text-gray-300">${hobby.description}</p>
        </div>
      </div>
    `;
    container.appendChild(card);
    VanillaTilt.init(card);
    gsap.from(card, { scrollTrigger: { trigger: card, start: 'top 80%' }, y: 50, opacity: 0, duration: 1, ease: 'power3.out' });
  });
});

// Render Projects with Modal
const modal = document.getElementById('project-modal');
const modalClose = document.getElementById('modal-close');
fetchData('/api/projects', 'projects-grid', (data, container) => {
  data.forEach(project => {
    const card = document.createElement('div');
    card.className = 'project-card glassmorphic rounded-xl overflow-hidden cursor-pointer hover:scale-105 transition-transform';
    card.setAttribute('data-tilt', '');
    card.setAttribute('data-tilt-max', '10');
    card.innerHTML = `
      <div class="relative">
        <img src="${project.image}" alt="${project.title}" class="w-full h-48 object-cover glow">
        <div class="project-overlay absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100">
          <i class="fas fa-search text-white text-2xl glow"></i>
        </div>
      </div>
      <div class="p-6">
        <h3 class="text-lg font-orbitron text-primary-blue glow mb-2">${project.title}</h3>
        <p class="text-gray-300 text-sm mb-4">${project.description.substring(0, 100)}...</p>
        <div class="flex flex-wrap gap-2">
          ${project.technologies.map(tech => `<span class="tech-tag glassmorphic text-xs px-2 py-1 rounded-full text-primary-blue glow">${tech}</span>`).join('')}
        </div>
      </div>
    `;
    card.addEventListener('click', () => {
      document.getElementById('modal-image').src = project.image;
      document.getElementById('modal-title').textContent = project.title;
      document.getElementById('modal-description').textContent = project.description;
      const techContainer = document.getElementById('modal-tech');
      techContainer.innerHTML = project.technologies.map(tech => `<span class="tech-tag glassmorphic text-xs px-2 py-1 rounded-full text-primary-blue glow">${tech}</span>`).join('');
      document.getElementById('modal-github').href = project.githubLink;
      document.getElementById('modal-live').href = project.liveLink;
      modal.classList.remove('hidden');
      gsap.from(modal.querySelector('div'), { y: 100, opacity: 0, duration: 0.8, ease: 'power3.out' });
    });
    container.appendChild(card);
    VanillaTilt.init(card);
    gsap.from(card, { scrollTrigger: { trigger: card, start: 'top 80%' }, y: 50, opacity: 0, duration: 1, ease: 'power3.out' });
  });
});
modalClose.addEventListener('click', () => {
  modal.classList.add('hidden');
});
modal.addEventListener('click', (e) => {
  if (e.target === modal) modal.classList.add('hidden');
});

// Render Education
fetchData('/api/education', 'education-grid', (data, container) => {
  data.forEach(edu => {
    const card = document.createElement('div');
    card.className = 'education-card glassmorphic p-6 rounded-xl hover:scale-105 transition-transform';
    card.setAttribute('data-tilt', '');
    card.setAttribute('data-tilt-max', '10');
    card.innerHTML = `
      <div class="flex items-start space-x-4">
        <div class="icon-wrapper p-3 glassmorphic rounded-full">
          <i class="fas fa-graduation-cap text-primary-blue glow"></i>
        </div>
        <div class="flex-1">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-lg font-orbitron text-primary-blue glow">${edu.degree}</h3>
            <div class="period flex items-center text-gray-400">
              <i class="fas fa-calendar mr-1"></i>
              <span>${edu.period}</span>
            </div>
          </div>
          <h4 class="text-primary-blue glow mb-2">${edu.institution}</h4>
          <p class="text-gray-300 mb-4">${edu.description}</p>
          <h5 class="font-orbitron text-primary-blue glow">Key Achievements:</h5>
          <ul class="list-disc pl-5 text-gray-300">
            ${edu.achievements.map(achievement => `<li>${achievement}</li>`).join('')}
          </ul>
        </div>
      </div>
    `;
    container.appendChild(card);
    VanillaTilt.init(card);
    gsap.from(card, { scrollTrigger: { trigger: card, start: 'top 80%' }, y: 50, opacity: 0, duration: 1, ease: 'power3.out' });
  });
});

// Handle Contact Form Submission via Button Click
const contactSubmitButton = document.getElementById('contact-submit');
const emailInput = document.getElementById('email');
const messageInput = document.getElementById('message');

contactSubmitButton.addEventListener('click', async () => {
  const email = emailInput.value.trim();
  const message = messageInput.value.trim();

  // Validate inputs
  if (!email || !message) {
    alert('Please fill in both email and message fields.');
    return;
  }

  if (!/\S+@\S+\.\S+/.test(email)) {
    alert('Please enter a valid email address.');
    return;
  }

  try {
    const response = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, message })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    alert(data.message);
    emailInput.value = '';
    messageInput.value = '';
  } catch (error) {
    console.error('Error submitting contact form:', error);
    alert('Error submitting form. If you\'re on Hugging Face Spaces, please use LinkedIn or GitHub to contact me.');
  }
});