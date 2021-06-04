  // Navbar appear on scroll up
  // https://www.w3schools.com/howto/howto_js_navbar_hide_scroll.asp

  var prevScrollpos = window.pageYOffset;
  window.onscroll = function () {
      var currentScrollPos = window.pageYOffset;
      if (prevScrollpos > currentScrollPos) {
          document.getElementById("navbar").style.top = "0";
      } else {
          document.getElementById("navbar").style.top = "-80px";
      }
      prevScrollpos = currentScrollPos;
  }

  // Divs appear on scroll down
  // https://scrollrevealjs.org/guide/whats-new.html

  ScrollReveal().reveal('.about-card', {
      duration: 2000,
      delay: 200
  });
  ScrollReveal().reveal('.contact-card', {
      duration: 2000,
      delay: 200
  });