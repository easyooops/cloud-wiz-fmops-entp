export const useContactStore = defineStore({
    id:'contact',
    state:()=>{
        return {
            display1:true,
            activeTab1: '0',
            selectedUser: ''
        }
    },
    actions:{
        change(){
            this.display1 = !this.display1
            },
           
            active(payload)
            {
            this.activeTab1 = payload 
           
            },
            print(payload)
            {
            this.selectedUser = payload 
           
            },
    },
    getters:{
        display:(state)=>{return state.display1},
        activeTab:(state)=>{return state.activeTab1},
        selectedUser1:(state)=>{return state.selectedUser}
    }
})
