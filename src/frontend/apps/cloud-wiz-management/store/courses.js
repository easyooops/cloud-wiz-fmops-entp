import Courses from "@/data/courses.json"
export const useCourseStore =defineStore({
	id:'course',
	state:()=>{
		return{
			courses : Courses.courses
		}
	},
	getters:{
		specialcourses: state =>{
			return state.courses.filter((course) => {
				if (course.special === 1)
					return course;
			});
		},
		normalcourses: state =>{
			return state.courses.filter((course) => {
				if (course.special === 0)
					return course;
			});
		}
	}
})
