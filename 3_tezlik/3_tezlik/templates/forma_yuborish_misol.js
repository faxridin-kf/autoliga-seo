/*
 * Mavjud forma kodidagi O'ZGARISH (reviewForm, contactForm, test-drayv formasi).
 * Hozirgi kod (bosh sahifadagi inline skript) taxminan shunday:
 *
 *   if (RECAPTCHA_SITE_KEY && typeof grecaptcha !== 'undefined') {
 *       grecaptcha.ready(function () {
 *           grecaptcha.execute(RECAPTCHA_SITE_KEY, { action: 'submit_review' }).then(function (token) {
 *               sendForm(token);
 *           });
 *       });
 *   } else {
 *       sendForm('');          // <-- reCAPTCHA yuklanmagan bo'lsa tokensiz ketadi
 *   }
 *
 * Yangi variant: reCAPTCHA yuklanishini kutadi, xato bo'lsa eski xatti-harakatga qaytadi.
 */
function submitWithRecaptcha(action, sendForm) {
  if (!RECAPTCHA_SITE_KEY || typeof window.ensureRecaptcha !== 'function') {
    sendForm('');
    return;
  }
  window.ensureRecaptcha()
    .then(function (grecaptcha) {
      grecaptcha.ready(function () {
        grecaptcha.execute(RECAPTCHA_SITE_KEY, { action: action }).then(sendForm);
      });
    })
    .catch(function () { sendForm(''); });
}

// Misol:
// submitWithRecaptcha('submit_review', function (token) { /* mavjud yuborish kodi, token bilan */ });
// submitWithRecaptcha('contact',       function (token) { ... });
// submitWithRecaptcha('test_drive',    function (token) { ... });
