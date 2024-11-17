import { defineNuxtConfig } from 'nuxt/config';

export default defineNuxtConfig({
    runtimeConfig: {
        "public": {},
        "app": {
          "googleClientId": process.env.VITE_GOOGLE_CLIENT_ID,
        }
    },
    css: ["@/assets/scss/app.scss"],
    ssr:false,
    app: {
        head: {
            link: [
                {
                    href: "https://fonts.googleapis.com/css?family=Rubik:400,400i,500,500i,700,700i&amp;display=swap",
                    rel: "stylesheet",
                },
                {
                    href: "https://fonts.googleapis.com/css?family=Roboto:300,300i,400,400i,500,500i,700,700i,900&amp;display=swap",
                    rel: "stylesheet",
                },
            ],
            title: "CLOUDWIZ AI FMOPS - LLM 활용을 위한 클라우드 플랫폼",
            script: [
                {
                    src: "https://www.paypal.com/sdk/js?client-id=test&currency=USD",
                },
                { src: "https://checkout.stripe.com/checkout.js" },
                { src: 'https://accounts.google.com/gsi/client', async:true, defer:true}
            ],
        },
    },
    modules: [
        "@nuxtjs/i18n",
        [
            "@pinia/nuxt",
            {
                autoImports: ["defineStore",'acceptHMRUpdate'],
            },
        ],
    ],
    i18n: {
        strategy: "prefix_except_default",
        defaultLocale: "en",
        locales: [
            {
                icon: "flag-icon-us",
                code: "en",
                name: "English",
                short: "(US)"
            },
            {
                icon: "flag-icon-fr",
                code: "fr",
                name: "Français"
            },
            {
                icon: "flag-icon-es",
                code: "es",
                name: "Español"
            },
            {
                icon: "flag-icon-pt",
                short: "(BR)",
                code: "pt",
                name: "Português"
            }
        ],
        vueI18n: "./i18n.config.ts"
    },
    plugins: [
        { src: "~/plugins/plugins.js", mode: "client" },
        { src: "./plugins/useBootstrap.client.ts", mode: "client" }
    ]
});
