<template>
    <div class="email-wrap bookmark-wrap">
        <div class="row">
            
            <div :class="getGridClass(filteredData.slice(0,4).length)" class="box-col-6" v-for="(dataItem, dataIndex) in filteredData.slice(0,4)" :key="dataIndex">
                <div class="card">
                    <div class="card-body">
                        <div class="email-app-sidebar left-bookmark">
                            <div class="media">
                                <div class="media-size-email">
                                    <li class="list-inline-item"><i class="fa fa-comments"></i></li>
                                </div>
                                <div class="media-body">
                                    <select class="form-select form-control-primary" v-model="dataItem.selectedAgent">
                                        <option value="" disabled hidden>Select Agent</option>
                                        <option v-for="agents in filteredData" :key="agents.agent_id" :value="agents.agent_id">{{ agents.agent_name }}</option>
                                    </select>
                                </div>                                         
                            </div>
                            <ul class="nav main-menu contact-options" role="tablist">
                                <div class="row chat-box">
                                    <div class="col pe-0 chat-right-aside">
                                        <div class="chat">
                                            <div class="chat-history chat-msg-box custom-scrollbar" :ref="`chatInput-${dataItem.agent_id}`">
                                                <ul>
                                                    <li v-for="(chat, index) in dataItem.currentChatMessages" :key="chat.time" :class="{ clearfix: chat.sender == 0 }">
                                                        <div class="message" :class="{ 'other-message pull-right': chat.sender == 0, 'my-message': chat.sender != 0, 'blinking': chat.isLoading}">
                                                            <img class="rounded-circle float-start chat-user-img img-30 text-end" alt="" v-if="chat.sender != 0" :src="getImgUrl(dataItem.currentChatThumb)" />
                                                            <img class="rounded-circle float-end chat-user-img img-30" alt="" v-if="chat.sender == 0" :src="getImgUrl('user/1.jpg')" />
                                                            <div class="message-data text-end" :class="{ 'text-start': chat.sender == 0 }">
                                                                <span class="message-data-time">{{ chat.time }}</span>
                                                            </div>
                                                            <div v-html="chat.text"></div>
                                                        </div>
                                                    </li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-xl-6">
                                <label class="col-form-label"><h6>Token Usage</h6></label>
                            </div>
                            <div class="col-xl-6 text-end">
                                <label class="col-form-label">{{ formatTokenSize(dataItem.tokens) }}</label>
                            </div>                        
                        </div>
                        <div class="row">
                            <div class="col-xl-6">
                                <label class="col-form-label"><h6>Expected Cost</h6></label>
                            </div>
                            <div class="col-xl-6 text-end">
                                <label class="col-form-label">{{ formatCost(dataItem.cost) }}</label>
                            </div>                        
                        </div>                        
                    </div>
                </div>
            </div>

            <div class="col-xl-12 box-col-6">
                <div class="card">
                    <div class="card-body">

                        <!-- loading area -->
                        <div class="loader-box" v-if="loading">
                            <div class="loader-30"></div>
                        </div> 

                        <div class="row chat-box">
                            <div class="col pe-0">
                                <div class="chat">
                                    <div class="chat-message clearfix">
                                        <div class="row">
                                            <div class="col-xl-1 d-flex"></div>
                                            <div class="col-xl-9 d-flex">
                                                <div class="input-group text-box" ref="abc">
                                                    <textarea class="form-control input-txt-bx" 
                                                        id="message-to-send" 
                                                        v-model="text" 
                                                        @keydown.enter="handleEnterKey" 
                                                        type="text" 
                                                        name="message-to-send" 
                                                        placeholder="Type a message......"></textarea>
                                                </div>
                                            </div>
                                            <div class="col-xl-1">
                                                <button @click="addChat()" class="btn btn-primary" type="button">
                                                    <i class="fa fa-send-o"></i>
                                                </button>
                                            </div>
                                            <div class="col-xl-1 d-flex"></div>                                 
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>     
                    </div>                
                </div>           
            </div>

        </div>
    </div>
</template>

<script>
import { useAgentStore } from '@/store/agent';
import { useAuthStore } from '@/store/auth';
import { mapState, mapActions } from 'pinia';

export default {
    name: 'agent',
    data() {
        return {
            activeclass: 'pills-personal-tab', 
            filtered: false,
            text: "",
            loading: false,            
            userId: useAuthStore().userId
        }
    },
    computed: {
        ...mapState(useAgentStore, ['agents']),
        filteredData() {
            return this.agents.map(agent => {
                return {
                    ...agent,
                    selectedAgent: '',
                    tokens: 0,
                    cost: 0,
                    currentChatMessages: [
                        {
                            sender: 0,
                            text: "Feel free to ask a variety of questions to test the agent you create.",
                            time: new Date().toLocaleTimeString()
                        }
                    ],
                    currentChatThumb: 'default-thumbnail.jpg',
                    isLoading: false
                };
            });
        }      
    },
    methods: {
        ...mapActions(useAgentStore, ['fetchAgentByUserId', 'fetchLLMS']),
        active(item) {
            this.activeclass = item
        },
        collapseFilter() {
            this.filtered = !this.filtered
        },
        getImgUrl(path) {
            return ('/images/' + path);
        },
        formatTokenSize(bytes) {
            if (bytes === 0) return '0 B';
            const units = ['B', 'KB', 'MB', 'GB', 'TB'];
            const decimalPlaces = 3;
            const k = 1024;
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(decimalPlaces)) + ' ' + units[i];
        },
        formatCost(cost) {
            return parseFloat(cost).toFixed(3) + ' $';
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
                        
            const userInput = this.text.replace(/\n/g, '<br/>'); // 줄바꿈 처리
            this.text = '';

            const promises = this.filteredData.map(async (dataItem) => {
                dataItem.currentChatMessages.push({
                    sender: 1,
                    text: userInput,
                    time: new Date().toLocaleTimeString()
                });

                // "Analyzing..." 메시지를 추가
                const loadingMessage = {
                    sender: 0,
                    text: "Analyzing...",
                    time: new Date().toLocaleTimeString(),
                    isLoading: true  // 로딩 상태를 표시하는 플래그 추가
                };
                dataItem.currentChatMessages.push(loadingMessage);
                const loadingMessageIndex = dataItem.currentChatMessages.length - 1;

                try {
                    const agentId = dataItem.selectedAgent;
                    let responseText = '';

                    if (!agentId) {
                        responseText = 'No agent selected';
                    } else {
                        await this.fetchLLMS(agentId, userInput);
                        responseText = useAgentStore().llmsResponse ? useAgentStore().llmsResponse.answer.replace(/\n/g, '<br/>') : 'No response';
                    }

                    // 새로운 객체로 할당하여 텍스트를 변경
                    dataItem.currentChatMessages.splice(loadingMessageIndex, 1, {
                        sender: 0,
                        text: responseText,
                        time: new Date().toLocaleTimeString(),
                        isLoading: false
                    });

                    dataItem.tokens += useAgentStore().llmsResponse.tokens;
                    dataItem.cost += useAgentStore().llmsResponse.cost;

                    this.scrollChat(agentId);

                    this.$forceUpdate();
                } catch (error) {
                    console.error('Error fetching LLMS response:', error);
                    // 오류 시 "Analyzing..." 메시지를 오류 메시지로 변경
                    dataItem.currentChatMessages.splice(loadingMessageIndex, 1, {
                        sender: 0,
                        text: 'Error occurred. Please try again.',
                        time: new Date().toLocaleTimeString(),
                        isLoading: false
                    });
                }
            });

            await Promise.all(promises);
        },
        scrollChat(agentId) {
            setTimeout(() => {
                const container = this.$refs[`chatInput-${agentId}`];
                if (container && container[0]) {
                    container[0].scrollBy({
                        top: container[0].scrollHeight,
                        behavior: 'smooth'
                    });
                } else {
                    console.error(`Container for agentId ${agentId} not found or is undefined.`);
                }
            }, 310);
        },        
        getGridClass(length) {
            if (length === 0) return "col-xl-12";
            const colSize = Math.max(1, Math.floor(12 / length));
            return `col-xl-${colSize}`;
        },
        setSelectedAgent(agentId, value) {
            const agent = this.filteredData.find(agent => agent.agent_id === agentId);
            if (agent) {
                agent.selectedAgent = value;
            }
        },
        async fetchData() {
          try {
            this.loading = true;
            useAgentStore().agents = [];
            await this.fetchAgentByUserId({ userId: this.userId });
            this.loading = false;

          } catch (error) {
            console.error('Error fetching data:', error);
          }
        }         
    },
    async mounted() {
        await this.fetchData();
    }
}
</script>

<style scoped>
.left-bookmark {
    height: 700px;
}
.bookmark-tabcontent {
    height: 700px;
}
.media { margin-bottom: 10px;}
.fa {
    font: normal normal normal 30px / 1 FontAwesome;
    margin-right: 10px;
}
.chat-box .chat-right-aside .chat .chat-msg-box { 
    height: 660px; 
    border-top: 1px solid #f4f4f4;
    padding: 30px;
    margin-bottom: 0px;
}
.chat-box {
    min-width: 100%;
}
.chat-box .chat-right-aside .chat .chat-msg-box .message-text {
    display: inline-block;
    max-width: 100%;
}
.form-control-primary {
    border-color: var(--theme-deafult);
    color: var(--theme-deafult);
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
