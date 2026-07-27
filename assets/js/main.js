(function () {
  "use strict";

  var nav = document.querySelector(".nav");
  var toggle = document.querySelector(".nav__toggle");
  var mobile = document.querySelector(".nav__mobile");

  if (nav) {
    var onScroll = function () {
      nav.classList.toggle("is-scrolled", window.scrollY > 24);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  if (toggle && mobile) {
    var setMenuOpen = function (open) {
      mobile.classList.toggle("is-open", open);
      if (nav) nav.classList.toggle("is-menu-open", open);
      document.body.classList.toggle("is-menu-open", open);
      toggle.setAttribute("aria-expanded", open);
      toggle.innerHTML = open
        ? '<i class="fa-solid fa-xmark"></i>'
        : '<i class="fa-solid fa-bars"></i>';
    };

    toggle.addEventListener("click", function () {
      setMenuOpen(!mobile.classList.contains("is-open"));
    });

    mobile.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setMenuOpen(false);
      });
    });
  }

  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length && "IntersectionObserver" in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    reveals.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    reveals.forEach(function (el) {
      el.classList.add("is-visible");
    });
  }

  var path = window.location.pathname.replace(/\/$/, "") || "/";
  document.querySelectorAll(".nav__link").forEach(function (link) {
    var href = link.getAttribute("href").replace(/\/$/, "") || "/";
    if (href === path || (href !== "/" && path.startsWith(href))) {
      link.classList.add("is-active");
    }
  });
})();
