'use strict';
// Optional enhancement: all content and answer explanations already exist in HTML.
document.querySelectorAll('.js-only').forEach(el => { el.hidden = false; });
document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));
document.querySelectorAll('form[data-quiz]').forEach(form => {
  const result = form.querySelector('.quiz-result');
  const clearFeedback = () => {
    form.querySelectorAll('[data-feedback]').forEach(el => { el.hidden = true; el.textContent = ''; el.className = 'feedback'; });
    result.textContent = '';
  };
  form.addEventListener('submit', event => {
    event.preventDefault();
    let correct = 0, answered = 0;
    const questions = [...form.querySelectorAll('.question')];
    questions.forEach(question => {
      const choice = question.querySelector('input:checked');
      const feedback = question.querySelector('[data-feedback]');
      const why = question.querySelector('.why').textContent;
      feedback.hidden = false;
      if (!choice) {
        feedback.className = 'feedback unanswered';
        feedback.textContent = '這題還沒選。先試一試，再檢查答案。';
      } else {
        answered++;
        const right = choice.value === question.dataset.answer;
        if (right) correct++;
        feedback.className = 'feedback ' + (right ? 'correct' : 'incorrect');
        feedback.textContent = (right ? '答對了。' : '再想一想。') + why;
      }
    });
    result.textContent = answered < questions.length
      ? `已回答 ${answered} / ${questions.length} 題，其中 ${correct} 題答對。還有 ${questions.length - answered} 題可以試試。`
      : correct === questions.length
        ? `${correct} / ${questions.length} 題答對。接著試著在自己的句子裡使用。`
        : `${correct} / ${questions.length} 題答對。讀讀每題提示，再試一次；這不代表你的整體程度。`;
  });
  form.addEventListener('change', clearFeedback);
  form.addEventListener('reset', () => {
    clearFeedback();
    form.querySelectorAll('.answer-reveal').forEach(details => { details.open = false; });
    result.textContent = '已清除這一組作答，可以重新練習。';
  });
});
if ('IntersectionObserver' in window) {
  const links = [...document.querySelectorAll('.lesson-sidebar nav a')];
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        links.forEach(link => {
          const current = link.hash === '#' + entry.target.id;
          link.classList.toggle('current', current);
          if (current) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      }
    }
  }, {rootMargin: '-12% 0px -65% 0px'});
  document.querySelectorAll('.lesson-section[id]').forEach(section => observer.observe(section));
}
// Print the full lesson, including collapsed explanations; worksheet/answer pages are separate.
let printState = [];
window.addEventListener('beforeprint', () => {
  printState = [...document.querySelectorAll('details')].map(el => [el, el.open]);
  printState.forEach(([el]) => { el.open = true; });
});
window.addEventListener('afterprint', () => {
  printState.forEach(([el, wasOpen]) => { el.open = wasOpen; });
  printState = [];
});
