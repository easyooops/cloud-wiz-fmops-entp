import { defineStore } from 'pinia';
import axios from 'axios';

export const useChatStore = defineStore( 'chat',{
    state:()=>{
        return{
            chats: [],
        };
    },
    actions: {
        async addChat(msg, sender) {
            var today = new Date().toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
            let addchat = this.chats.find(chat => chat.id === 0);

            if (!addchat) {
                addchat = { id: 0, messages: [] } as any; //채팅이 없다면 초기값으로 빈배열 세팅
                this.chats.push(addchat);
            }

            if (sender === 1 && addchat.messages.length > 0 && addchat.messages[addchat.messages.length - 1].sender === 1) {
                // 이미 고정된 답변이 있고, 새로운 응답이 오면 기존 답변을 제거하고 새로운 응답을 추가합니다.
                addchat.messages.pop();
            }

            const sendMessage = { 'sender': sender, 'time': today.toLowerCase(), 'text': msg };
            addchat.messages.push(sendMessage);

            if (sender === 0) {
                const responseMessage = {'sender': 1, 'time': today.toLowerCase(), 'loading' : true};
                addchat.messages.push(responseMessage);
                // 채팅이 추가될 때 이벤트 발생 (스크롤 다운을 넣고싶다...)
                //this.$pinia.appContext.config.globalProperties.$emit('chatAdded');
                await this.getChatApi(msg);
            }

        },
        async getChatApi(question: string){
            try{
                /!* local 테스트용- *!/
                // const response = await axios.post('http://localhost:8080/api/wiz/ai',{question});
                const response = await axios.post('https://be.cloudwiz-ai.com/api/wiz/ai',{question});
                const { answer } = response.data.resultData;
                const resCode = response.data.resultCode;
                var annswerCode = 1;

                if(resCode === '200'){
                    this.addChat(answer, annswerCode); //API 응답값 일 경우 sender = 1
                }else{
                    this.addChat('일시적으로 챗봇 오류가 발생했습니다, 다시 시도해주세요',annswerCode);
                }
            }catch(error){
                console.error('Error occured fetching Chat API:', error);
                this.addChat('일시적인 오류가 발생했습니다, 다시 시도해주세요',annswerCode);
            }
        }
    }
})
