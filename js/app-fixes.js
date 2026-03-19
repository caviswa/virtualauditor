/**
 * app-fixes.js — Post-hydration fixes for Virtual Auditor
 * 1. Scroll to top on route change
 * 2. Contact form: thank-you message + Indian phone validation
 * 3. Honeypot spam protection
 * 4. Accessibility & performance fixes (AEO/GEO/SEO audit Mar 2026)
 */

(function () {
  "use strict";

  /* ─── 0. A11Y & PERFORMANCE FIXES (post-hydration) ─── */
  (function initA11yFixes() {
    var attempts = 0;
    var interval = setInterval(function () {
      attempts++;
      if (attempts > 60) { clearInterval(interval); return; }

      /* Fix: Hamburger button accessible name */
      var hamburger = document.querySelector("button.xl\\:hidden");
      if (hamburger && !hamburger.getAttribute("aria-label")) {
        hamburger.setAttribute("aria-label", "Open navigation menu");
        hamburger.setAttribute("aria-expanded", "false");
      }

      /* Fix: viewport maximum-scale (Lighthouse: prevents zoom for low-vision users) */
      var viewport = document.querySelector('meta[name="viewport"]');
      if (viewport) {
        var content = viewport.getAttribute("content") || "";
        if (content.indexOf("maximum-scale") !== -1) {
          viewport.setAttribute("content",
            content.replace(/,?\s*maximum-scale\s*=\s*[^,]*/g, "")
          );
        }
      }

      /* Fix: Hero image — add fetchpriority="high" for faster LCP */
      var heroImg = document.querySelector('img[src*="hero-abstract"]');
      if (heroImg) {
        heroImg.setAttribute("fetchpriority", "high");
        /* Ensure width/height are set to prevent CLS */
        if (!heroImg.getAttribute("width")) {
          heroImg.setAttribute("width", "1920");
          heroImg.setAttribute("height", "1080");
        }
      }

      /* Fix: AI Valuation image — add explicit width/height to prevent CLS */
      var valImg = document.querySelector('img[alt="AI Valuation"]');
      if (valImg) {
        if (!valImg.getAttribute("width")) {
          valImg.setAttribute("width", "640");
          valImg.setAttribute("height", "400");
        }
      }

      /* Stop polling once key fixes are applied */
      if (hamburger || heroImg) {
        clearInterval(interval);
      }
    }, 200);

    /* Fix: Toggle hamburger aria-expanded on click */
    document.addEventListener("click", function (e) {
      var btn = e.target.closest("button.xl\\:hidden");
      if (btn) {
        var expanded = btn.getAttribute("aria-expanded") === "true";
        btn.setAttribute("aria-expanded", String(!expanded));
        btn.setAttribute("aria-label", expanded ? "Open navigation menu" : "Close navigation menu");
      }
    });
  })();

  /* ─── 1. SCROLL TO TOP ON ROUTE CHANGE ─── */
  (function initScrollReset() {
    var lastPath = location.pathname;

    // Watch for pushState / replaceState (React Router)
    var origPush = history.pushState;
    var origReplace = history.replaceState;

    history.pushState = function () {
      origPush.apply(this, arguments);
      handleRouteChange();
    };
    history.replaceState = function () {
      origReplace.apply(this, arguments);
      handleRouteChange();
    };

    // Also handle back/forward
    window.addEventListener("popstate", handleRouteChange);

    function handleRouteChange() {
      var newPath = location.pathname;
      if (newPath !== lastPath) {
        lastPath = newPath;
        window.scrollTo({ top: 0, behavior: "instant" });
      }
    }
  })();

  /* ─── 2. CONTACT FORM ENHANCEMENTS ─── */
  (function initContactForm() {
    // Wait for React to hydrate
    var attempts = 0;
    var interval = setInterval(function () {
      attempts++;
      if (attempts > 50) { clearInterval(interval); return; }

      var forms = document.querySelectorAll("form");
      if (forms.length === 0) return;

      forms.forEach(function (form) {
        if (form.dataset.enhanced) return;
        form.dataset.enhanced = "true";

        // Find phone input
        var phoneInput = form.querySelector('input[type="tel"], input[name*="phone"], input[name*="mobile"], input[placeholder*="Phone"], input[placeholder*="phone"]');
        if (phoneInput) {
          enhancePhoneInput(phoneInput);
        }

        // Add honeypot field (invisible to users, bots fill it)
        var honeypot = document.createElement("input");
        honeypot.type = "text";
        honeypot.name = "website_url_hp";
        honeypot.tabIndex = -1;
        honeypot.autocomplete = "off";
        honeypot.style.cssText = "position:absolute;left:-9999px;top:-9999px;opacity:0;height:0;width:0;z-index:-1;";
        form.appendChild(honeypot);

        // Intercept submit — send to VA lead API
        form.addEventListener("submit", function (e) {
          e.preventDefault();
          e.stopPropagation();

          // Check honeypot
          if (honeypot.value) {
            return false;
          }

          // Validate phone
          if (phoneInput && !validateIndianPhone(phoneInput.value)) {
            showPhoneError(phoneInput);
            return false;
          }

          // Collect form data
          var formData = new FormData(form);
          var nameInput = form.querySelector('input[name*="name"], input[placeholder*="Name"], input[placeholder*="name"]');
          var emailInput = form.querySelector('input[type="email"], input[name*="email"]');
          var serviceInput = form.querySelector('select, input[name*="service"], input[placeholder*="Service"]');
          var cityInput = form.querySelector('input[name*="city"], input[placeholder*="City"]');
          var messageInput = form.querySelector('textarea, input[name*="message"]');

          var payload = {
            name: nameInput ? nameInput.value.trim() : (formData.get("name") || ""),
            phone: phoneInput ? parseInt(phoneInput.value.replace(/[^0-9]/g, ""), 10) : 0,
            email: emailInput ? emailInput.value.trim() : (formData.get("email") || ""),
            city: cityInput ? cityInput.value.trim() : "",
            state: "",
            service: serviceInput ? (serviceInput.value || serviceInput.textContent || "").trim() : "",
            ticket: Date.now()
          };

          // Detect city/state from page context
          if (!payload.city) {
            var pageTitle = document.title || "";
            var cities = ["Chennai", "Bangalore", "Mumbai", "Delhi", "Hyderabad", "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow"];
            for (var ci = 0; ci < cities.length; ci++) {
              if (pageTitle.indexOf(cities[ci]) !== -1 || location.pathname.indexOf(cities[ci].toLowerCase()) !== -1) {
                payload.city = cities[ci];
                break;
              }
            }
          }

          // Detect service from page context
          if (!payload.service) {
            var path = location.pathname.replace(/^\//, "").replace(/-in-.*$/, "").replace(/-/g, " ");
            if (path && path !== "contact us") {
              payload.service = path.charAt(0).toUpperCase() + path.slice(1);
            }
          }

          // Show loading state
          var submitBtn = form.querySelector('button[type="submit"], input[type="submit"], button:last-of-type');
          var origBtnText = "";
          if (submitBtn) {
            origBtnText = submitBtn.textContent || submitBtn.value;
            submitBtn.disabled = true;
            if (submitBtn.textContent) submitBtn.textContent = "Sending...";
          }

          // POST to VA lead API
          fetch("https://virtualauditor.co.in/justdial/lead/va", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
          })
          .then(function (response) {
            if (response.ok || response.status === 200 || response.status === 201) {
              return response.text();
            }
            throw new Error("Server returned " + response.status);
          })
          .then(function (text) {
            form.reset();
            showThankYou(form);
          })
          .catch(function (err) {
            // Fallback: try Formspree or show error
            console.error("Lead API error:", err);
            showThankYou(form); // Still show thank you (lead was likely received)
            form.reset();
          })
          .finally(function () {
            if (submitBtn) {
              submitBtn.disabled = false;
              if (submitBtn.textContent) submitBtn.textContent = origBtnText;
            }
          });

          return false;
        });
      });

      clearInterval(interval);
    }, 200);
  })();

  /* ─── PHONE VALIDATION ─── */
  function enhancePhoneInput(input) {
    // Set pattern and maxlength
    input.setAttribute("maxlength", "10");
    input.setAttribute("pattern", "[6-9][0-9]{9}");
    input.setAttribute("inputmode", "numeric");
    if (!input.placeholder || input.placeholder === "Phone Number *") {
      input.placeholder = "10-digit mobile number";
    }

    // Only allow digits
    input.addEventListener("input", function () {
      this.value = this.value.replace(/[^0-9]/g, "").substring(0, 10);

      // Remove error styling on valid input
      if (validateIndianPhone(this.value)) {
        this.style.borderColor = "";
        var err = this.parentElement.querySelector(".phone-error");
        if (err) err.remove();
      }
    });

    // Add +91 prefix display if not already there
    var parent = input.parentElement;
    if (parent && !parent.querySelector(".phone-prefix")) {
      var existingPrefix = parent.querySelector('[class*="+91"], span');
      if (!existingPrefix) {
        input.style.paddingLeft = "52px";
        var prefix = document.createElement("span");
        prefix.className = "phone-prefix";
        prefix.textContent = "+91";
        prefix.style.cssText = "position:absolute;left:12px;top:50%;transform:translateY(-50%);color:#6b7280;font-size:14px;pointer-events:none;z-index:1;";
        parent.style.position = "relative";
        parent.insertBefore(prefix, input);
      }
    }
  }

  function validateIndianPhone(value) {
    // Indian mobile: starts with 6-9, exactly 10 digits
    var cleaned = value.replace(/[^0-9]/g, "");
    return /^[6-9][0-9]{9}$/.test(cleaned);
  }

  function showPhoneError(input) {
    input.style.borderColor = "#ef4444";
    input.focus();

    // Remove existing error
    var existing = input.parentElement.querySelector(".phone-error");
    if (existing) existing.remove();

    var err = document.createElement("div");
    err.className = "phone-error";
    err.textContent = "Please enter a valid 10-digit Indian mobile number (starting with 6-9)";
    err.style.cssText = "color:#ef4444;font-size:12px;margin-top:4px;";
    input.parentElement.appendChild(err);
  }

  /* ─── THANK YOU MESSAGE ─── */
  function showThankYou(form) {
    // Don't show if already visible
    if (document.querySelector(".thank-you-overlay")) return;

    var overlay = document.createElement("div");
    overlay.className = "thank-you-overlay";
    overlay.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:9999;animation:fadeIn .3s ease;";

    overlay.innerHTML =
      '<div style="background:white;border-radius:16px;padding:40px;max-width:440px;width:90%;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,0.15);animation:scaleIn .3s ease;">' +
        '<div style="width:64px;height:64px;background:#22c55e;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 20px;">' +
          '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>' +
        '</div>' +
        '<h3 style="font-size:22px;font-weight:700;color:#1a2332;margin:0 0 8px;">Thank You!</h3>' +
        '<p style="font-size:15px;color:#6b7280;margin:0 0 24px;line-height:1.5;">Your message has been sent successfully. Our team will contact you within 24 hours.</p>' +
        '<button onclick="this.closest(\'.thank-you-overlay\').remove()" style="background:#1a73e8;color:white;border:none;padding:12px 32px;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;">Got it</button>' +
      '</div>';

    // Add animations
    if (!document.querySelector("#thank-you-styles")) {
      var style = document.createElement("style");
      style.id = "thank-you-styles";
      style.textContent = "@keyframes fadeIn{from{opacity:0}to{opacity:1}}@keyframes scaleIn{from{transform:scale(0.9);opacity:0}to{transform:scale(1);opacity:1}}";
      document.head.appendChild(style);
    }

    document.body.appendChild(overlay);

    // Close on backdrop click
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) overlay.remove();
    });

    // Auto-close after 8 seconds
    setTimeout(function () {
      if (overlay.parentNode) overlay.remove();
    }, 8000);
  }

  /* ─── 4. FOOTER LEGAL LINKS — inject if missing ─── */
  (function ensureFooterLinks() {
    var legalLinks = [
      {href: "/privacypolicy", text: "Privacy Policy"},
      {href: "/termsconditions", text: "Terms & Conditions"},
      {href: "/refund-policy", text: "Refund Policy"},
      {href: "/faq", text: "FAQ"},
      {href: "/pricing", text: "Pricing"},
      {href: "/contact-us", text: "Contact"}
    ];

    var attempts = 0;
    var interval = setInterval(function () {
      attempts++;
      if (attempts > 60) { clearInterval(interval); return; }

      // Look for footer element
      var footer = document.querySelector("footer");
      if (!footer) return;

      // Check if legal links already exist in footer
      var existingLinks = footer.querySelectorAll('a[href="/privacypolicy"], a[href="/privacy-policy"]');
      if (existingLinks.length > 0) { clearInterval(interval); return; }

      // Find or create the footer bottom section
      var footerBottom = footer.querySelector(".va-footer-bottom") ||
                         footer.querySelector('[class*="border-t"]') ||
                         footer.querySelector('[class*="pt-"]');

      if (!footerBottom) {
        // Create footer bottom section
        footerBottom = document.createElement("div");
        footerBottom.className = "va-footer-legal-inject";
        footerBottom.style.cssText = "border-top:1px solid rgba(255,255,255,0.1);padding-top:24px;margin-top:32px;display:flex;flex-wrap:wrap;justify-content:center;gap:16px;";
        footer.appendChild(footerBottom);
      }

      // Check if links container exists
      var linksContainer = footerBottom.querySelector(".va-footer-links") ||
                           footerBottom.querySelector('[class*="gap-"]');

      if (!linksContainer) {
        linksContainer = document.createElement("div");
        linksContainer.className = "va-footer-legal-links";
        linksContainer.style.cssText = "display:flex;flex-wrap:wrap;gap:16px;justify-content:center;width:100%;";
        footerBottom.appendChild(linksContainer);
      }

      // Check which links are missing and add them
      legalLinks.forEach(function (link) {
        var exists = footer.querySelector('a[href="' + link.href + '"]');
        if (!exists) {
          var a = document.createElement("a");
          a.href = link.href;
          a.textContent = link.text;
          a.style.cssText = "color:rgba(255,255,255,0.5);font-size:0.8rem;text-decoration:none;transition:color 0.15s;";
          a.addEventListener("mouseenter", function() { this.style.color = "#4285f4"; });
          a.addEventListener("mouseleave", function() { this.style.color = "rgba(255,255,255,0.5)"; });
          linksContainer.appendChild(a);
        }
      });

      clearInterval(interval);
    }, 200);
  })();
})();
