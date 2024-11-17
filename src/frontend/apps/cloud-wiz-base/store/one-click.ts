import { defineStore } from "pinia"
import {integer} from "vscode-languageserver-types"

export const useOneClickStore = defineStore('oneClick', {
    state: () => ({
        oneClickStage: 0,
        stageLength: 0,
        stageSelected: {}
    }),
    actions: {

        isLast() {
            return this.oneClickStage + 1 == this.stageLength
        },

        isSelected(targetValue: string) {

            const storeSelected = this.stageSelected[this.oneClickStage];

            if (Array.isArray(storeSelected)) {
                const storeSelectedArr = [...storeSelected];

                return storeSelectedArr.includes(targetValue)
            } else {
                return storeSelected === targetValue;
            }
        },

        nextQuestion(type: string, selected: any, isEndYn: string) {
            if (isEndYn === 'Y' || this.isLast()) {
                return navigateTo('/consulting/result')
            }

            if (!this.stageSelected.hasOwnProperty(this.oneClickStage)) {
                // Directly assign to the property to ensure reactivity
                this.stageSelected[this.oneClickStage] = []
            }

            // Assign the value to the corresponding stage
            this.stageSelected[this.oneClickStage] = selected

            this.oneClickStage++
        },

        prevQuestion() {
            this.oneClickStage--
        },

        setOneClickStage(stage: integer) {
            this.oneClickStage = stage
        },

        setStageLength(stageLength: integer) {
            this.stageLength = stageLength
        }

    },
})
