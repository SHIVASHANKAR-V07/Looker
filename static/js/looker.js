// Loader
window.addEventListener('load', function () {
  setTimeout(function () {
    document.getElementById('loader').style.display = 'none';
    document.getElementById('home').style.display = 'block';
  }, 1000);
});

// Navbar Hide/Show on Scroll
var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("navbar").style.top = "0";
  } else {
    document.getElementById("navbar").style.top = "-50px";
  }
  prevScrollpos = currentScrollPos;
}

// Mobile Menu Toggle
function toggleMenu() {
  const navLinks = document.querySelector('.nav-links');
  navLinks.classList.toggle('active');
}

// Profile Menu Toggle
function toggleProfile() {
  const menu = document.getElementById('profile-menu');
  menu.style.display = menu.style.display === 'none' || menu.style.display === '' ? 'block' : 'none';
}

// Buy Now / Cart
function buyNow() {
  window.location.href = "/buy_now";
}

// Close mobile menu when clicking a link
document.addEventListener('DOMContentLoaded', function() {
  const navLinks = document.querySelectorAll('.nav-links a');
  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      const navLinksContainer = document.querySelector('.nav-links');
      if (navLinksContainer.classList.contains('active')) {
        navLinksContainer.classList.remove('active');
      }
    });
  });
  
  // Close profile menu when clicking outside
  document.addEventListener('click', function(event) {
    const profileMenu = document.getElementById('profile-menu');
    const profileButton = document.getElementById('profile');
    
    if (profileMenu && profileButton) {
      if (!profileButton.contains(event.target) && !profileMenu.contains(event.target)) {
        profileMenu.style.display = 'none';
      }
    }
  });
});