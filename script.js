$(document).ready(function () {

    // ── Sticky Navbar + Scroll Up Button ──
    $(window).scroll(function () {
        if (this.scrollY > 20) {
            $('.navbar').addClass("sticky");
        } else {
            $('.navbar').removeClass("sticky");
        }
        if (this.scrollY > 500) {
            $('.scroll-up-btn').addClass("show");
        } else {
            $('.scroll-up-btn').removeClass("show");
        }
    });

    // ── Scroll Up ──
    $('.scroll-up-btn').click(function () {
        $('html').animate({ scrollTop: 0 });
        $('html').css("scrollBehavior", "auto");
    });

    $('.navbar .menu li a').click(function () {
        $('html').css("scrollBehavior", "smooth");
    });

    // ── Mobile Menu Toggle ──
    $('.menu-btn').click(function () {
        $('.navbar .menu').toggleClass("active");
        $('.menu-btn i').toggleClass("active");
    });

    // ── Dark / Light Mode Toggle ──
    var savedTheme = localStorage.getItem('theme') || 'light-mode';
    $('body').removeClass('light-mode dark-mode').addClass(savedTheme);
    updateThemeIcon(savedTheme);

    $('#themeToggle').click(function () {
        if ($('body').hasClass('light-mode')) {
            $('body').removeClass('light-mode').addClass('dark-mode');
            localStorage.setItem('theme', 'dark-mode');
            updateThemeIcon('dark-mode');
        } else {
            $('body').removeClass('dark-mode').addClass('light-mode');
            localStorage.setItem('theme', 'light-mode');
            updateThemeIcon('light-mode');
        }
    });

    function updateThemeIcon(theme) {
        if (theme === 'dark-mode') {
            $('#themeIcon').removeClass('fa-moon').addClass('fa-sun');
        } else {
            $('#themeIcon').removeClass('fa-sun').addClass('fa-moon');
        }
    }

});
