import todo from "@/data/trace.json"
export const useTodoStore = defineStore({
    id:'trace',
    state:()=>{
        return{
            todo : todo.data
        }
    },
    actions:{
        taskcomplete(payload){
            this.todo.find(function (list) {
                if (list.id === payload) {
                    return list.status = list.status === 'complete' ? 'incomplete' : 'complete';
                }
            });
        },
        alltaskcomplete(payload){
           this.todo.filter(function (list) {
                   return list.status = payload === true ? 'complete':'incomplete';
            });
        },
        tododelete(payload){
            this.todo = this.todo.filter(list => list.id !== payload);
        },
        addtodo(payload){
    let id = Math.max(...this.todo.map(item=> item.id))+1;

             this.todo.unshift(
                {
                    'id': id,
                    'title': payload,
                    'priority':"Pending",
                    'date':"16 Jan",
                    'badgeClass':"badge-light-danger",
                    'delete': false,
                    'status': 'incomplete'
                }
            );
        }
    }
})

