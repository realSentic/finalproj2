document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-toast]').forEach((el) => {
        console.log('found toast:', el);

        setTimeout(() => {
            console.log('timeout fired');

            el.classList.remove('motion-preset-slide-up');

            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    el.classList.add('motion-opacity-out-0');
                    console.log('classes:', el.className);
                });
            });

            setTimeout(() => el.remove(), 300);
        }, 5000);
    });
});

