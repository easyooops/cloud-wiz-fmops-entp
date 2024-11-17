import { defineStore } from 'pinia';
import commonUtil from "~/utils/common";

export const useDialogStore = defineStore('dialog', {
    state: () => ({
        dialog_status : false,
        dialog_title : 'CloudWiz',
        dialog_message : 'Welcome to CloudWiz',
        dialog_btn_text : 'Close'
    }),
    actions: {

        openDialog(title: string, message: string, btn_text: string)  {

            this.dialog_status = true

            if (commonUtil().isNotEmpty(title)) {
                this.dialog_title = title
            } else {
                this.dialog_title = 'CloudWiz'
            }

            if (commonUtil().isNotEmpty(message)) {
                this.dialog_message = message
            } else {
                this.dialog_message = 'Welcome to CloudWiz'
            }

            if (commonUtil().isNotEmpty(btn_text)) {
                this.dialog_btn_text = btn_text
            } else {
                this.dialog_btn_text = 'Close'
            }
        },
        closeDialog()  {
            this.dialog_status = false
        }
    }
});
