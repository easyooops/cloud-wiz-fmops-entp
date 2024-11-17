import { defineStore } from 'pinia';
import restApi from "~/utils/axios"
import commonUtil from "~/utils/common";

export const useCommonStore = defineStore('common', {
    state: () => ({
        commFirstItem : '',
        commGrpCode : '',
        commCodeList : []
    }),
    actions: {

        async getCommCodeList()  {
            const error = ref()
            const pending = ref(true)

            try {

                const response = await restApi().get('/comm','',null)

                // @ts-ignore
                const items = response.data.value["resultData"].filter((e: { commGrpCode: any; }) => e.commGrpCode === this.commGrpCode)

                if (commonUtil().isNotEmpty(this.commFirstItem)) {
                    items.push({
                        commCode:"",
                        commCodeDesc:this.commFirstItem,
                        commCodeName:this.commFirstItem,
                        commCodeOrder:"0",
                        commGrpCode:this.commGrpCode
                    })
                }

                this.commCodeList = items.sort((a: any, b: any) => a["commCodeOrder"].localeCompare(b["commCodeOrder"]))

            } catch (err) {
                error.value = err
            } finally {
                pending.value = false
            }
        }
    }
});
