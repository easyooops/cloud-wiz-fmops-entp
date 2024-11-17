export default{
    data() {
        return {
            columns: [{
                    title: "Todo",
                    bgclass: 'bg-info',
                    lightbgclass: 'bg-light-info',
                    tasks: [{
                            id: 1,

                            title: "Design Dashboard",
                            date: "23/07/20",
                            badge: "medium",
                            badgetype: "badge-primary",
                            location: "Themeforest, australia",
                        },
                        {
                            id: 2,

                            title: "Test Sidebar",
                            date: "24/7/20",
                            badge: "Urgent",
                            badgetype: "badge-danger",
                            location: "Themeforest, australia",
                        },

                    ]
                },
                {
                    title: "Doing",
                    bgclass: 'bg-warning',
                    lightbgclass: 'bg-light-warning',
                    tasks: [{
                            id: 1,

                            title: "Design Dashboard",
                            date: "23/07/20",
                            badge: "medium",
                            badgetype: "badge-primary",
                            location: "Themeforest, australia",
                        },
                        {
                            id: 2,

                            title: "Test Sidebar",
                            date: "24/7/20",
                            badge: "Low",
                            badgetype: "badge-success",
                            location: "Themeforest, australia",
                        },
                    ]
                },
                {
                    title: "Done",
                    bgclass: 'bg-success',
                    lightbgclass: 'bg-light-success',
                    tasks: [{
                            id: 1,

                            title: "Design Dashboard",
                            date: "23/07/20",
                            badge: "medium",
                            badgetype: "badge-danger",
                            location: "Themeforest, australia",
                        },
                        {
                            id: 2,

                            title: "Test Sidebar",
                            date: "24/7/20",
                            badge: "Low",
                            badgetype: "badge-success",
                            location: "Themeforest, australia",
                        }
                    ]
                }
            ]
        };
    },
    methods: {
        add() {
            this.columns.push({
                title: "default",
                tasks: [{
                        id: 1,

                        title: "Design Dashboard",
                        date: "23/07/20",
                        badge: "medium",
                        badgetype: "badge-primary",
                        location: "Themeforest, australia",
                    },
                    {
                        id: 2,

                        title: "Test Sidebar",
                        date: "24/7/20",
                        badge: "Urgent",
                        badgetype: "badge-danger",
                        location: "Themeforest, australia",
                    },

                ]
            })
        },
        addelment() {
            this.columns[0].tasks.push({
                    id: 1,
                    title: "Design Dashboard",
                    date: "23/07/20",
                    badge: "medium",
                    badgetype: "badge-primary",
                    location: "Themeforest, australia",
                },
            )
        },
        remove() {
            this.columns.forEach((element,index)=>{
                if(element.title === 'done'){
                    this.columns.splice(index,1)
                }
            })
        }
    }
}