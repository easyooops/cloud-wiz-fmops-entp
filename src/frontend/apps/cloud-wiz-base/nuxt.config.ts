import { defineNuxtConfig } from 'nuxt/config';
import { resolve } from "path";

export default defineNuxtConfig({
    // buildDir: '../../dist/apps/cloud-wiz-base/.nuxt',
    alias: {
        "@": resolve(__dirname, "/")
    },
    app: {
        head: {
            meta: [
                { name: "viewport", content: "width=device-width, initial-scale=1" },
                { hid: 'description', name: 'description', content: 'Explore resources on AI, machine learning, and large language models. Find tutorials, guides, and the latest research on artificial intelligence and its applications.' },
                { hid: 'keywords', name: 'keywords', content: 'AI, Artificial Intelligence, Machine Learning, Deep Learning, Neural Networks, Large Language Models, LLM, NLP, Natural Language Processing, GPT, GPT-3, GPT-4, OpenAI, BERT, Transformer Models, AI Research, AI Development, AI Tools, AI Tutorials, AI Guides, AI Applications, AI Trends, Machine Learning Algorithms, Supervised Learning, Unsupervised Learning, Reinforcement Learning, AI Ethics, AI Safety, AI in Healthcare, AI in Finance, AI in Robotics, AI Programming, AI Frameworks, TensorFlow, PyTorch, AI Optimization, AI Performance, AI Scalability, AI Deployment, AI Integration, AI Startups, AI Innovations, AI Conferences, AI Workshops, AI Webinars, AI Courses, AI Certifications, AI Jobs, AI Careers' },
                { property: 'og:title', content: '미래를 여는 LLM 기반 AI 플랫폼' },
                { property: 'og:description', content: '노코드 기반의 쉬운 UI로 누구나 AI를 만들 수 있습니다. 지속적으로 발전하는 LLM 모델을 활용하여 시장 변화에 빠르게 대응하고 다양한 산업에 창의적인 솔루션을 제공합니다.' },
                { property: 'og:image', content: 'https://cloudwiz-ai.com/assets/images/cloudwiz-ai-fmops.png' },
                { name: 'twitter:card', content: 'summary_large_image' },
                { name: 'twitter:title', content: '미래를 여는 LLM 기반 AI 플랫폼' },
                { name: 'twitter:description', content: '노코드 기반의 쉬운 UI로 누구나 AI를 만들 수 있습니다. 지속적으로 발전하는 LLM 모델을 활용하여 시장 변화에 빠르게 대응하고 다양한 산업에 창의적인 솔루션을 제공합니다.' },
                { name: 'twitter:image', content: 'https://cloudwiz-ai.com/assets/images/cloudwiz-ai-fmops.png' },            
            ],
            title: "CLOUDWIZ AI FMOPS - LLM 활용을 위한 클라우드 플랫폼",
            script: []
        }
    },
    typescript: {
        shim: false
    },
    css: [
      "vuetify/lib/styles/main.sass",
      "~/assets/css/vendors/bootstrap.min.css",
      "~/assets/css/vendors/flaticon.css",
      "~/assets/css/vendors/menu.css",
      "~/assets/css/vendors/fade-down.css",
      "~/assets/css/vendors/magnific-popup.css",
      "~/assets/css/vendors/animate.css",
      "~/assets/css/main.scss",
      "~/assets/css/responsive.scss",
      "~/assets/css/color-scheme/blue.scss",
      "~/assets/css/color-scheme/crocus.scss",
      "~/assets/css/color-scheme/green.scss",
      "~/assets/css/color-scheme/magenta.scss",
      "~/assets/css/color-scheme/pink.scss",
      "~/assets/css/color-scheme/skyblue.scss",
      "~/assets/css/color-scheme/violet.scss",
      "@mdi/font/css/materialdesignicons.min.css",
    ],
    modules: [
        [
            "@nuxtjs/google-fonts",
            {
                families: {
                    Rubik: {
                        wght: [300, 400, 500, 600, 700]
                    },
                    "Plus+Jakarta+Sans": {
                        wght: [400, 500, 600, 700]
                    },
                    Inter: {
                        wght: [400, 500, 600, 700, 800]
                    },
                    download: true,
                    inject: true
                }
            }
        ],
        [
            '@pinia/nuxt',
            {
                autoImports: [
                    // automatically imports `defineStore`
                    'defineStore',
                ],
            },
        ],
        "nuxt-swiper",
        [
            '@vee-validate/nuxt',
            {
                // disable or enable auto imports
                autoImports: true,
                // Use different names for components
                componentNames: {
                    Form: 'Form',
                    Field: 'Field',
                    FieldArray: 'FieldArray',
                    ErrorMessage: 'ErrorMessage',
                },
            },
        ],
        "@nuxtjs/robots",
        "@nuxtjs/sitemap",
        "nuxt-gtag"
    ],
    robots: {
        UserAgent: '*',
        Disallow: '/admin',
        Sitemap: 'https://cloudwiz-ai.com/'
    },
    sitemap: {
        hostname: 'https://cloudwiz-ai.com/',
        gzip: true,
        routes: [
            '/'
        ]
    },
    gtag: {
        tags: [
          {
            id: 'G-CRC6Y6K8E1',
            config: {
              page_title: 'Cloudwiz AI FMOps'
            }
          }
        ],
        compatibilityDate: '2024-07-30'
    },
    plugins: [
        '~/plugins/validation.ts'
    ],

    build: {
        transpile: ['@vuepic/vue-datepicker','vuetify']
    },
    buildModules: [
        '@pinia/nuxt',
        '@nuxtjs/fontawesome',
    ],
    loading: {
        color: 'blue',
        height: '5px'
    },
    fontawesome: {
        component: 'Fa',
        suffix: false,
        icons: {
            solid: true,
            brands: true,
        },
    },
    vite:{
        define: {'process.env.DEBUG':false,
        },
    },
    ssr: false,
    site: {
        url: 'https://cloudwiz-ai.com'
    },       
});

