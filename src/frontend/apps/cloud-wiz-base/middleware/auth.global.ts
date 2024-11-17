import { storeToRefs } from 'pinia'
import { useAuthStore } from '~/store/auth'
import commonUtil from "~/utils/common"
export default defineNuxtRouteMiddleware((to) => {
    const { authenticated } = storeToRefs(useAuthStore()) // make authenticated state reactive
    const token = useCookie('token') // get token from cookies

    // const { isUrlAllowed } = commonUtil()

    const urlWhiteList = [
        '/'
        , '/login'
        , '/about'
        , '/consulting'
        , '/consulting/**'
        , '/dashboard'
        , '/dashboard/**'
        , '/development'
        , '/development/**'
        , '/preparing'
        , '/preparing/**'
        , '/sample/**'
        , '/template/**'
    ]

    if (to?.name === 'logout'){
        useAuthStore().logUserOut()
        return navigateTo('/')
    }

    if (token.value) {
        // check if value exists
        // todo verify if token is valid, before updating the state
        authenticated.value = true // update the state to authenticated
    }

    // if token exists and url is /login redirect to homepage
    if (token.value && to?.name === 'login') {
        return navigateTo('/')
    }

    // if token doesn't exist redirect to log in
    if (!token.value) {

        if(!commonUtil().isUrlAllowed(to?.fullPath, urlWhiteList)){
            abortNavigation()
            return navigateTo('/login')
        }
    }
    
})
