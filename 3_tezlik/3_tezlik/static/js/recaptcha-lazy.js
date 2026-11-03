/*
 * static/js/recaptcha-lazy.js
 *
 * reCAPTCHA v3 ni sahifa ochilganda emas, foydalanuvchi formaga tegsa yuklaydi.
 * Hozir api.js + recaptcha__ru.js har sahifada ~500 KB JS yuklaydi va mobil telefonda
 * asosiy oqimni band qiladi.
 *
 * Talab: sahifada window.RECAPTCHA_SITE_KEY bo'lishi kerak (hozir inline skriptda bor).
 *
 * Ishlatish:
 *   1) base.html dagi  <script src="https://www.google.com/recaptcha/api.js?render=...">  qatorini O'CHIRING.
 *   2) Uning o'rniga:  <script src="{% static 'js/recaptcha-lazy.js' %}" defer></script>
 *   3) Forma yuborish kodida:
 *        ensureRecaptcha().then(function (grecaptcha) {
 *          grecaptcha.ready(function () {
 *            grecaptcha.execute(RECAPTCHA_SITE_KEY, { action: 'submit_review' }).then(function (token) { ... });
 *          });
 *        });
 */
(function () {
  "use strict";

  var loading = null;

  function siteKey() {
    return window.RECAPTCHA_SITE_KEY || (typeof RECAPTCHA_SITE_KEY !== "undefined" ? RECAPTCHA_SITE_KEY : "");
  }

  function ensureRecaptcha() {
    if (window.grecaptcha && window.grecaptcha.execute) {
      return Promise.resolve(window.grecaptcha);
    }
    if (loading) return loading;
    var key = siteKey();
    if (!key) return Promise.reject(new Error("RECAPTCHA_SITE_KEY topilmadi"));

    loading = new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = "https://www.google.com/recaptcha/api.js?render=" + encodeURIComponent(key) + "&hl=" +
        (document.documentElement.lang || "uz");
      s.async = true;
      s.onload = function () {
        var tries = 0;
        (function wait() {
          if (window.grecaptcha && window.grecaptcha.execute) return resolve(window.grecaptcha);
          if (++tries > 100) return reject(new Error("grecaptcha yuklanmadi"));
          setTimeout(wait, 50);
        })();
      };
      s.onerror = function () { loading = null; reject(new Error("reCAPTCHA skripti yuklanmadi")); };
      document.head.appendChild(s);
    });
    return loading;
  }

  window.ensureRecaptcha = ensureRecaptcha;

  // Formaga birinchi teginishda oldindan yuklash (yuborishgacha tayyor bo'ladi)
  function warm(e) {
    if (e.target && e.target.closest && e.target.closest("form")) {
      ensureRecaptcha().catch(function () {});
      document.removeEventListener("focusin", warm, true);
      document.removeEventListener("pointerdown", warm, true);
    }
  }
  document.addEventListener("focusin", warm, true);
  document.addEventListener("pointerdown", warm, true);
})();
