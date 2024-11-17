import  en  from "./locales/en.json";
import  fr  from "./locales/fr.json";
import  es  from "./locales/es.json";
import  pt  from "./locales/pt.json";

export default defineI18nConfig(nuxt => ({
    legacy: false,
    locale: "en",
    messages: {
        en: en.data,
        fr: fr.data,
        es: es.data,
        pt: pt.data,
    },
}))
