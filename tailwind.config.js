/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/**/*.html",
        "./static/**/*.js",
        "./**/*.py",
    ],
    theme: {
        extend: {
            colors: {
                'darkgreen': '#182822',
                'castletongreen': '#257830',
                'erieblack': '#252525',
                'mirtlegreen': '#307474',
                'munsellblue': '#5397A7',
                'verdigris': '#62A8AC',
                'pechyellow': '#EED28E',
                'orchidpink': '#D4AEB8',
                'oranye': '#F29620',
                'white': '#FFFFFF',
                'gray': '#B0B0B0'
            },
            fontFamily: {
                'raleway': ['Raleway', 'sans-serif'],
                'domine': ['Domine', 'serif'],
            },
            fontSize: {
                'h1': '64px',
                'h2': '48px',
                'h3': '40px',
                'h4': '36px',
                'h5': '24px',
                'h6': '20px',
                'p': '20px',
                'small': '16px',
                'a': '14px',
            },
            fontWeight: {
                'heading': '800',
                'link': '700',
            }
        },
    },
    plugins: [],
}