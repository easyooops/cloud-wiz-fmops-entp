import Menu from '@/data/dashboard/menu.json';
import { defineStore } from 'pinia';
export const useMenuStore= defineStore({
  id:'menu',
  state:()=>{
    return{
      data: Menu.data,
      searchData: [],
      togglesidebar: true,
      activeoverlay : false,
      searchOpen : false,
      customizer: '',
      hideRightArrowRTL: false,
      hideLeftArrowRTL: true,
      hideRightArrow: true,
      hideLeftArrow: true,
      width: 0,
      height: 0,
      margin: 0,
      menuWidth: 0,
    }
  },
  actions:{
    opensidebar(){
      if (process.client) {
      this.togglesidebar = !this.togglesidebar;
      if (window.innerWidth < 991) {
        this.activeoverlay = true;
      } else {
        this.activeoverlay = false;
      }
    }},
    resizetoggle()  {
      if (process.client) {
      if (window.innerWidth < 1199) {
        this.togglesidebar = false;
        // this.activeoverlay = true
      } else {
        this.togglesidebar = true;
        // this.activeoverlay = false
      }
    }},
    searchTerm(term) {
      let items = [];
      var searchval = term.toLowerCase();
      this.data.filter(menuItems => {
        
        if (menuItems.title) {
          if (menuItems.title.toLowerCase().includes(searchval) && menuItems.type === 'link') {
            items.push(menuItems);
          }
          if (!menuItems.children) return false;
          menuItems.children.filter(subItems => {
            if (subItems.title.toLowerCase().includes(searchval) && subItems.type === 'link') {
              subItems.icon = menuItems.icon;
              items.push(subItems);
            }
            if (!subItems.children) return false;
            subItems.children.filter(suSubItems => {
              if (suSubItems.title.toLowerCase().includes(searchval)) {
                suSubItems.icon = menuItems.icon;
                items.push(suSubItems);
              }
            });
          });
          this.searchData = items;
        }
      });
    },
    
    setNavActive(item){
     
      if (!item.active) {
        this.data.forEach(a => {
          if (this.data.includes(item))
            a.active = false;
          if (!a.children) return false;
          a.children.forEach(b => {
            if (a.children.includes(item)) {
              b.active = false;
            }
            if(!b.children) return false;
          b.children.forEach(c =>{
            if(b.children.includes(item)){
              c.active = false
            }
          })
          });
        });
      }
      item.active = !item.active;
    },
    setActiveRoute(item){
    
      this.data.filter(menuItem => {
        if (menuItem !== item)
          menuItem.active = false;
        if (menuItem.children && menuItem.children.includes(item)){
        item.active = true;
        menuItem.active = true;}
        if (menuItem.children) {
          menuItem.children.filter(submenuItems => {
            if (submenuItems.children && submenuItems.children.includes(item)) {
              item.active = true;
              menuItem.active = true;
              submenuItems.active = true;
            }
          });
        }
      });
    }
  }
})
