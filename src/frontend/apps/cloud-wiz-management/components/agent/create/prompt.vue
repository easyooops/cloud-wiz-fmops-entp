<template>
    <div class="row chat-box">
        <div class="col pe-0 chat-right-aside">
            <div class="chat">
                <div class="chat-history chat-msg-box custom-scrollbar" ref="chatInput">
                    <ul>
                        <li v-for="(chat, index) in currentChatMessages" :key="index" v-bind:class="{ clearfix: chat.sender == 0 }">
                            <!-- <div class="message" v-bind:class="{ 'other-message pull-right': chat.sender == 0, 'my-message': chat.sender != 0}">
                                <img class="rounded-circle float-start chat-user-img img-30 text-end" alt="" v-if="chat.sender != 0" v-bind:src="getImgUrl(currentChatThumb)" />
                                <img class="rounded-circle float-end chat-user-img img-30" alt="" v-if="chat.sender == 0" v-bind:src="getImgUrl('user/1.jpg')" />
                                <div class="message-data text-end" v-bind:class="{ 'text-start': chat.sender == 0 }">
                                    <span class="message-data-time">{{ chat.time }}</span>
                                </div>
                                {{ chat.text }}
                            </div> -->

                            <div class="message" v-bind:class="{ 'other-message pull-right': chat.sender == 0, 'my-message': chat.sender != 0, 'blinking': chat.isLoading}">
                                <img class="rounded-circle float-start chat-user-img img-30 text-end" alt="" v-if="chat.sender != 0" v-bind:src="getImgUrl(currentChatThumb)" />
                                <img class="rounded-circle float-end chat-user-img img-30" alt="" v-if="chat.sender == 0" v-bind:src="getImgUrl('user/1.jpg')" />
                                <div class="message-data text-end" v-bind:class="{ 'text-start': chat.sender == 0 }">
                                    <span class="message-data-time">{{ chat.time }}</span>
                                </div>
                                <div v-html="chat.text"></div>
                            </div>
                        </li>
                    </ul>
                </div>
                <div class="chat-message clearfix">
                    <div class="row">
                        <div class="col-xl-12 d-flex">
                            <div class="input-group text-box" ref="abc">
                                <textarea 
                                    class="form-control input-txt-bx" 
                                    id="message-to-send" 
                                    v-model="text" 
                                    @keydown.enter="handleEnterKey"
                                    type="text" 
                                    name="message-to-send" 
                                    placeholder="Type a message......"></textarea>
                            </div>
                            <button @click="addChat()" class="btn btn-primary" type="button" :disabled="!agentId">
                                <i class="fa fa-send-o"></i>
                            </button>
                        </div>                       
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
    
<script>
import { useAgentStore } from '@/store/agent';

export default {
    name: 'prompt',
    data() {
        return {
            text: "",
            agentId: '',
            currentChatMessages: [
                {
                    sender: 0,
                    text: "Feel free to ask a variety of questions to test the agent you create.",
                    time: new Date().toLocaleTimeString()
                }
            ],
            currentChatThumb: 'default-thumbnail.jpg',
            chatmenutoogle: false
        }
    },
    computed: {
        agentId() {
            const agentStore = useAgentStore();
            const agent = agentStore.agent;
            const agentId = agent ? agent.agent_id : '';
            return agentId;
            // return agentStore.agent ? agentStore.agent.agent_id : '';
        }
    },    
    methods: {
        getImgUrl(path) {
            return ('/images/' + path);
        },
        handleEnterKey(event) {
            if ((event.shiftKey || event.altKey) && event.key === 'Enter') {
                // Shift+Enter 입력 시 줄바꿈 처리
                return;
            } else if (event.key === 'Enter') {
                event.preventDefault(); // 기본 엔터 동작 방지
                this.addChat(); // 엔터키 입력 시 채팅 전송
            }
        },          
        async addChat() {
            if (this.text.trim() === '') return;
            
            this.currentChatMessages.push({
                sender: 1,
                text: this.text.replace(/\n/g, '<br/>'),
                time: new Date().toLocaleTimeString()
            });
            const userInput = this.text.replace(/\n/g, '<br/>'); // 줄바꿈 처리;
            this.text = '';
            this.scrollChat();

            const agentStore = useAgentStore();
            const agentId = agentStore.agent ? agentStore.agent.agent_id : '';

            const loadingMessage = {
                sender: 0,
                text: "Analyzing...",
                time: new Date().toLocaleTimeString(),
                isLoading:true
            };
            this.currentChatMessages.push(loadingMessage);
            const loadingMessageIndex = this.currentChatMessages.length - 1;
            this.scrollChat();

            try {
                await agentStore.fetchLLMS(agentId, userInput);

                // this.currentChatMessages.push({
                //     sender: 0,
                //     text: agentStore.llmsResponse.answer,
                //     time: new Date().toLocaleTimeString()
                // });
                this.currentChatMessages.splice(loadingMessageIndex, 1, {
                    sender: 0,
                    text: agentStore.llmsResponse.answer.replace(/\n/g, '<br/>'),
                    time: new Date().toLocaleTimeString(),
                    isLoading: false
                });

                this.scrollChat();
            } catch (error) {
                console.error('Error fetching LLMS response:', error);
                this.currentChatMessages.splice(loadingMessageIndex, 1, {
                    sender: 0,
                    text: 'Error occurred. Please try again.',
                    time: new Date().toLocaleTimeString(),
                    isLoading: false
                });
            }
        },
        scrollChat() {
            const container = this.$refs.chatInput;  
            setTimeout(() => {
                container.scrollBy({
                    top: container.scrollHeight,
                    behavior: 'smooth'
                });
            }, 310);
        }
    }
}
</script>

<style scoped>
.chat-box .chat-right-aside .chat .chat-msg-box { 
    height: 700px; 
    border-top: 1px solid #f4f4f4;
    padding: 30px;
}
.chat-box {
    min-width: 100%;
}
.chat-box .chat-right-aside .chat .chat-msg-box .message-text {
    display: inline-block;
    max-width: 100%;
}
@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0; }
    100% { opacity: 1; }
}
.blinking {
    animation: blink 1s infinite;
}
</style>