// Deployment settings. The deploy workflow overwrites this file using the
// repository secrets EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, EMAILJS_PUBLIC_KEY
// and HISTORY_URL (the Google Apps Script web app for shared song history).
// Values can also be entered in the app's Settings.
window.SONGS_CONFIG = {
  emailjs: { serviceId: '', templateId: '', publicKey: '' },
  historyUrl: '',
  replyTo: 'chalkuhns@gmail.com',
};
