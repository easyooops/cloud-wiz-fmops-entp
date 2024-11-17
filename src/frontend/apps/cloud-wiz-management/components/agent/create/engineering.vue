<template>
    <div class="card mb-0">
        <div class="loader-overlay" v-if="loading">
            <div class="loader-box">
                <div class="loader-30"></div>
            </div>
        </div>

        <div class="chat">
            <div class="card-header d-flex">
                <div class="about">
                    <ul>
                        <li class="list-inline-item"><i class="fa fa-chain"></i></li>
                        <li class="list-inline-item"><h5>Engineering</h5></li>
                    </ul>
                </div>
                <div class="row">
                    <div class="col">
                        <button v-if="agentId" class="btn btn-outline-primary me-2" @click.prevent="createIndexing()">
                            <vue-feather type="database" class="text-top"></vue-feather> Vector Indexing
                        </button>                                            
                        <button @click="saveAgent" class="btn btn-primary me-2">Save</button>
                        <button v-if="agentId" @click="deleteAgent" class="btn btn-danger me-2">Delete</button>
                        <router-link to="/agent/list" class="btn btn-secondary">Back to List</router-link>
                    </div>
                </div>
            </div>
        </div>

        <div class="card-body p-0">
        <div class="row list-persons" id="addcon">
            <div class="col-xl-3 xl-50 col-md-5">
                <div class="nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical">
                    <a class="contact-tab-0 nav-link" :class="this.activeTab == item.activeTab ? 'active show' : ''"
                        id="v-pills-user-tab" data-bs-toggle="pill" @click="activeDiv(item.activeTab)"
                        href="#v-pills-user" role="tab" aria-controls="v-pills-user" aria-selected="true"
                        v-for="(item, index) in menu" :key="index">
                        <div class="media">
                            <li class="list-inline-item"><i :class="item.class"></i></li>
                            <div class="media-body">
                                <h6> <span class="first_name_0">{{ item.menu }}</span></h6>
                                <p class="email_add_0">{{ item.description }}</p>
                            </div>
                        </div>
                    </a>
                </div>
            </div>
            <div class="col-xl-9 xl-50 col-md-7">
                <div class="tab-content" id="v-pills-tabContent" :style="!this.display ? { display: 'none' } : ''">
                    <div class="tab-pane contact-tab-0 tab-content-child fade show"
                        :class="item.activeTab === this.activeTab ? 'active' : ''" id="v-pills-user" role="tabpanel"
                        aria-labelledby="v-pills-user-tab" v-for="(item, index) in menu" :key="index">

                        <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
                        <div v-if="successMessage" class="alert alert-success mt-3">{{ successMessage }}</div>   

                        <!-- Foundation Model -->
                        <div class="card-body" v-if="'0'==this.activeTab">
                            <div class="form theme-form">
                                <div class="card">
                                    <div class="card-body">
                                        <div class="mb-3">
                                            <label for="agentName">Agent Name *</label>
                                            <input v-model="agentName" class="form-control" type="text" id="agentName" placeholder="Agent Name *" required>
                                        </div>
                                        <div class="mb-3">
                                            <label for="agentDescription">Agent Description</label>
                                            <input v-model="agentDescription" class="form-control" type="text" id="agentDescription" placeholder="Agent Description">
                                        </div>
                                    </div>
                                </div>                                    

                                <div class="card">
                                    <div class="card-body">                                    
                                        <div class="row">
                                            <div class="col-xl-4 mb-3">
                                                <div class="col-form-label">Model Type *</div>
                                                <select class="form-select form-control-primary" v-model="modelType">
                                                    <option value="C">Chat</option>
                                                    <option value="T">Text</option>
                                                    <option value="I">Image</option>
                                                </select>
                                            </div>
                                            <div class="col-xl-4 mb-3">
                                                <div class="col-form-label">Provider *</div>
                                                <select class="form-select form-control-primary" v-model="selectedProvider">
                                                    <option value="" disabled hidden>Select Provider</option>
                                                    <option v-for="provider in filteredProviders" :key="provider.credential_id" :value="provider.credential_id">{{ provider.credential_name }}</option>
                                                </select>
                                            </div> 
                                            <div class="col-xl-4 mb-3">
                                                <div class="col-form-label">Foundation Model *</div>
                                                <select class="form-select form-control-primary" v-model="selectedFoundationModel">
                                                    <option value="" disabled hidden>Select Foundation Model</option>
                                                    <option v-for="model in filteredModels" :key="model.model_id" :value="model.model_id">{{ model.model_name }}</option>
                                                </select>
                                            </div>                                             
                                        </div>                                
                                    </div>
                                </div> 

                                <div class="card">
                                    <div class="card-body">
                                        <div class="form-group row mb-5">
                                            <label class="col-md-2 col-form-label sm-left-text" for="temperature">Temperature *</label>
                                            <div class="col-md-9">
                                                <VueSlider v-model="temperature.value" :data="temperature.data" :marks="true" :tooltip="'always'" :tooltip-placement="'top'"></VueSlider>
                                            </div>
                                        </div>
                                        <div class="form-group row mb-5">
                                            <label class="col-md-2 col-form-label sm-left-text" for="topP">Top P *</label>
                                            <div class="col-md-9">
                                                <VueSlider v-model="topP.value" :data="topP.data" :marks="true" :tooltip="'always'" :tooltip-placement="'top'"></VueSlider>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="card">
                                    <div class="card-body"> 
                                        <div class="mb-3">
                                            <fieldset>
                                                <label class="col-md-2 col-form-label sm-left-text" for="requestToken">Request Token Limit</label>
                                                <div class="input-group col-md-9">
                                                    <button type="button" class="btn btn-primary btn-square bootstrap-touchspin-down" @click="decrementRequestToken"><i class="fa fa-minus"></i></button>
                                                    <input class="touchspin form-control" type="text" v-model="requestToken">
                                                    <button type="button" class="btn btn-primary btn-square bootstrap-touchspin-up" @click="incrementRequestToken"><i class="fa fa-plus"></i></button>
                                                </div>
                                            </fieldset>
                                        </div>
                                        <div class="mb-3">
                                            <label for="responseToken">Response Token Limit</label>
                                            <fieldset>
                                                <div class="input-group">
                                                    <button type="button" class="btn btn-primary btn-square bootstrap-touchspin-down" @click="decrementResponseToken"><i class="fa fa-minus"></i></button>
                                                    <input class="touchspin form-control" type="text" v-model="responseToken">
                                                    <button type="button" class="btn btn-primary btn-square bootstrap-touchspin-up" @click="incrementResponseToken"><i class="fa fa-plus"></i></button>
                                                </div>
                                            </fieldset>
                                        </div>
                                    </div>
                                </div>
                                                                      
                            </div>
                        </div>

                        <!-- Embedding -->
                        <div class="card-body" v-if="'1'==item.activeTab">
                          <div class="form theme-form">
                            <div class="card">
                              <div class="card-body">
                                <div class="media mb-3">
                                  <label class="col-form-label m-r-10">Embedding Enable</label>
                                  <div class="media-body text-end">
                                    <label class="switch">
                                      <input type="checkbox" v-model="embeddingEnabled"><span class="switch-state"></span>
                                    </label>
                                  </div>
                                </div>
                              </div>
                            </div>

                            <div class="card" :class="{ 'disabled-card': !embeddingEnabled }">
                              <div class="card-body">
                                <div class="row">
                                  <div class="col-xl-6 mb-3">
                                    <div class="col-form-label">Embedding Provider *</div>
                                    <select class="form-select form-control-primary" v-model="selectedEmbeddingProvider">
                                      <option value="" disabled hidden>Select Embedding Provider</option>
                                      <option v-for="provider in filteredEmbeddingProviders" :key="provider.credential_id" :value="provider.credential_id">{{ provider.credential_name }}</option>
                                    </select>
                                  </div>
                                  <div class="col-xl-6 mb-3">
                                    <div class="col-form-label">Embedding Model *</div>
                                    <select class="form-select form-control-primary" v-model="selectedEmbeddingModel">
                                      <option value="" disabled hidden>Select Embedding Model</option>
                                      <option v-for="model in filteredEmbeddingModels" :key="model.model_id" :value="model.model_id">{{ model.model_name }}</option>
                                    </select>
                                  </div>
                                </div>
                              </div>
                            </div>

                            <div class="card" :class="{ 'disabled-card': !embeddingEnabled }">
                              <div class="card-body">
                                <div class="mb-3">
                                  <div class="col-form-label">Provider *</div>
                                  <select class="form-select form-control-primary" v-model="selectedStorageProvider">
                                    <option value="" disabled hidden>Select Storage Provider</option>
                                    <option v-for="provider in filteredStorageProviders" :key="provider.credential_id" :value="provider.credential_id">{{ provider.credential_name }}</option>
                                  </select>
                                </div>
                                <div class="mb-3" v-if="filteredObjects.length > 0">
                                  <div class="col-form-label">Storage</div>
                                  <select class="form-select form-control-primary" v-model="selectedObject">
                                    <option value="" disabled hidden>Select Object</option>
                                    <option v-for="object in filteredObjects" :key="object.store_id" :value="object.store_id">{{ object.store_name }}</option>
                                  </select>
                                </div>
<!--                                <div class="mb-3">-->
<!--                                  <div class="col-form-label">File</div>-->
<!--                                  <select class="form-select form-control-primary" v-model="selectedFiles" >-->
<!--                                    <option value="" disabled hidden="">Select file</option>-->
<!--                                    <option v-for="file in filteredFiles" :key="file.key" :value="file.key">{{ getFileName(file.Key) }}</option>-->
<!--                                  </select>-->
<!--                                </div>-->
                              </div>
                            </div>

                            <div class="card" :class="{ 'disabled-card': !embeddingEnabled }">
                              <div class="card-body">
                                <div class="mb-3">
                                  <div class="col-form-label">Vector DB</div>
                                  <select class="form-select form-control-primary" v-model="selectedVectorDB">
                                    <option v-for="provider in filteredVectorDBProviders" :key="provider.credential_id" :value="provider.credential_id">{{ provider.credential_name }}</option>
                                  </select>
                                </div>
                              </div>
                            </div>

                          </div>
                        </div>
                        
                        <!-- Processing -->
                        <div class="card-body" v-if="'2' == item.activeTab">
                            <div class="form theme-form">
                                <div class="card">
                                    <div class="card-body">
                                        <div class="media mb-3">
                                            <label class="col-form-label m-r-10">Processing Enable</label>
                                            <div class="media-body text-end">
                                                <label class="switch">
                                                    <input type="checkbox" v-model="processingEnabled"><span class="switch-state"></span>
                                                </label>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="card" :class="{ 'disabled-card': !processingEnabled }">
                                    <div class="card-body">
                                        <div class="mb-3">
                                            <div class="col-form-label">Pre-Processing</div>
                                            <select class="form-select form-control-primary" v-model="selectedPreProcessing" :disabled="!processingEnabled">
                                                <option v-for="processing in filteredPreProcessings" :key="processing.processing_id" :value="processing.processing_id">{{ processing.processing_name }}</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div class="card" :class="{ 'disabled-card': !processingEnabled }">
                                    <div class="card-body">
                                        <div class="mb-3">
                                            <div class="col-form-label">Post-Processing</div>
                                            <select class="form-select form-control-primary" v-model="selectedPostProcessing" :disabled="!processingEnabled">
                                                <option v-for="processing in filteredPostProcessings" :key="processing.processing_id" :value="processing.processing_id">{{ processing.processing_name }}</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Template -->
                        <div class="card-body" v-if="'3' == item.activeTab">
                            <div class="form theme-form">
                                <div class="card">
                                    <div class="card-body">
                                        <div class="media mb-3">
                                            <label class="col-form-label m-r-10">Template Enable</label>
                                            <div class="media-body text-end">
                                                <label class="switch">
                                                    <input type="checkbox" v-model="templateEnabled"><span class="switch-state"></span>
                                                </label>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="card" :class="{ 'disabled-card': !templateEnabled }">
                                    <div class="card-body">
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <label class="col-form-label"><h5>Template</h5></label>
                                                <textarea v-model="textareaTemplate" class="form-control form-control-primary" id="textareaTemplate" rows="25"></textarea>
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
    </div>
</div>
</template>

<script>
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'
import { useAuthStore } from '@/store/auth';
import { useContactStore } from '~~/store/contact'
import { useAgentStore } from '@/store/agent';
import { useProviderStore } from '@/store/provider';
import { useStorageStore } from '@/store/storage';
import { useProcessingStore } from '@/store/processing';
import { mapState, mapActions } from 'pinia';
import { useRouter } from 'vue-router';

export default {
    name: 'EngineeringSetup',
    components: {
        VueSlider,
    },
    data() {
        return {
            router: {},
            num1: 5000,
            temperature: {
                value: 0.7,
                data: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
            },
            topP: {
                value: 1,
                data: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
            },
            agentName: '',
            agentDescription: '',
            selectedFoundationModel: '',
            requestToken: 256,
            responseToken: 256,
            selectedEmbeddingProvider: '',
            selectedEmbeddingModel: '',
            selectedProvider: '',
            selectedStorageProvider: '',
            selectedObject: '',
            selectedFiles: [],
            filteredFiles: [],
            selectedVectorDB: '',
            selectedPreProcessing: '',
            selectedPostProcessing: '',
            embeddingEnabled: false,
            processingEnabled: false,
            templateEnabled: false,
            textareaTemplate: '"""\n<Question>{question}</Question>\n<Context>\nSummarize it\n</Context>\n<Answer>\nSummarize within 250 characters.\nAnswer in Korean.\nIf you don`t know, say you don`t know. Don`t make things up.\n</Answer>\n"""',
            data: {
                "data": [
                    {
                        "activeTab": "0",
                        "class": "fa fa-code-fork",
                        "menu": "Foundation Model *",
                        "description": "Language Models (LLMs) serve as the foundation for chat systems, understanding and generating human-like text.",
                    },
                    {
                        "activeTab": "1",
                        "class": "fa fa-database",
                        "menu": "Embedding",
                        "description": "Embeddings capture semantic meaning of text for efficient retrieval in retrieval-augmented generation (RAG) models.",
                    },
                    {
                        "activeTab": "2",
                        "class": "fa fa-cogs",
                        "menu": "Processing",
                        "description": "Processing involves preparing input data for models (preprocessing) and handling model outputs (postprocessing) for effective communication or analysis.",
                    },
                    {
                        "activeTab": "3",
                        "class": "fa fa-file-code-o",
                        "menu": "Template",
                        "description": "Templates are predefined structures that guide the creation of input prompts for models, ensuring consistency and improving response quality.",
                    },
                ],
            },
            modelType: 'C',
            agentId: '',
            agentData: {},            
            errorMessage: '',
            successMessage: '',
            loading: false,
            userId: useAuthStore().userId
        }
    },
  computed: {
      display() {
        return useContactStore().display;
      },
      activeTab() {
        return useContactStore().activeTab;
      },
      menu() {
        return this.data.data;
      },
      ...mapState(useProviderStore, ['credentials', 'models']),
      ...mapState(useStorageStore, ['storages']),
      ...mapState(useAgentStore, ['agent']),
      ...mapState(useProcessingStore, ['processings']),
      filteredProviders() {
        return this.credentials.filter(provider => provider.provider_type === "M");
      },
      filteredModels() {
        let credentials = this.credentials.filter(provider => provider.credential_id === this.selectedProvider);
        let provider_id = '';
        if (credentials.length > 0) {
          provider_id = credentials[0].provider_id;
        }
        return this.models.filter(model => model.model_type === this.modelType && model.provider_id == provider_id);
      },
      filteredEmbeddingProviders() {
        return this.credentials.filter(provider => provider.provider_type === "M");
      },
      filteredEmbeddingModels() {
        let credentials = this.credentials.filter(provider => provider.credential_id === this.selectedEmbeddingProvider);
        let provider_id = '';
        if (credentials.length > 0) {
          provider_id = credentials[0].provider_id;
        }
        return this.models.filter(model => model.model_type === "E" && model.provider_id == provider_id);
      },
      filteredStorageProviders() {
        return this.credentials.filter(provider => provider.provider_type === "S" || provider.provider_type === "L");
      },

      filteredObjects() {
        return this.storages.filter(storage => storage.credential_id === this.selectedStorageProvider);
      },
      filteredFiles() {
        return this.filteredFiles;
      },
      isS3ProviderSelected() {
        let credentials = this.credentials.filter(provider => provider.credential_id === this.selectedStorageProvider);
        let provider_id = '';
        if (credentials.length > 0) {
          provider_id = credentials[0].provider_id;
        }
        let selectedProvider = this.credentials.find(provider => provider.provider_id === provider_id);
        return selectedProvider && selectedProvider.credential_name.includes('S3');
      },
      filteredVectorDBProviders() {
        return this.credentials.filter(provider => provider.provider_type === "V");
      },
      filteredPreProcessings() {
        return this.processings.filter(processing => processing.processing_type === 'pre');
      },
      filteredPostProcessings() {
        return this.processings.filter(processing => processing.processing_type === 'post');
      }
    },
    watch: {
        selectedStorageProvider(){
          const filteredObjects = this.filteredObjects;
          if (filteredObjects.length > 0){
            this.selectedObject = filteredObjects[0].store_id;
          }
        },
        requestToken(newValue) {
            if (newValue > 5000) this.requestToken = 5000
            else if (newValue < 0) this.requestToken = 0
        },
        responseToken(newValue) {
            if (newValue > 5000) this.responseToken = 5000
            else if (newValue < 0) this.responseToken = 0
        },
        selectedProvider() {
            if (this.models.length > 0) {
                let filteredModels = this.models.filter(model => model.model_type === this.modelType && model.model_id == this.selectedFoundationModel);
                if (filteredModels.length > 0) {
                    this.selectedFoundationModel = filteredModels[0].model_id;
                }
            }
        },
        modelType(newModelType) {
            let credentials = this.credentials.filter(provider => provider.credential_id === this.selectedProvider);
            if (credentials.length > 0) {
                if (this.models.length > 0) {
                    let filteredModels = this.models.filter(model => model.model_type === newModelType && model.provider_id == credentials[0].provider_id);
                    if (filteredModels.length > 0) {
                        this.selectedFoundationModel = filteredModels[0].model_id;
                    }
                }                
            }
        },
        selectedEmbeddingProvider() {
            if (this.models.length > 0) {
                let filteredEmbeddingModels = this.models.filter(model => model.model_type === "E" && model.model_id == this.selectedEmbeddingModel);
                if (filteredEmbeddingModels.length > 0) {
                    this.selectedEmbeddingModel = filteredEmbeddingModels[0].model_id;
                }
            }
        }

    },
    methods: {
        ...mapActions(useProviderStore, ['fetchCredential', 'fetchModels']),
        ...mapActions(useStorageStore, ['fetchAllStorages','fetchFiles','createIndexing']),
        ...mapActions(useAgentStore, ['fetchAgentById']),
        ...mapActions(useProcessingStore, ['fetchProcessingsById']),
        activeDiv(item) {
            useContactStore().active(item)
        },
        incrementRequestToken() {
            if (this.requestToken < 5000) this.requestToken++
        },
        decrementRequestToken() {
            if (this.requestToken > 0) this.requestToken--
        },
        incrementResponseToken() {
            if (this.responseToken < 5000) this.responseToken++
        },
        decrementResponseToken() {
            if (this.responseToken > 0) this.responseToken--
        },
        async fetchAgentData() {

            this.agentId = String(this.router.currentRoute.query.agentId);
            if (this.agentId) {
                try {
                    await useAgentStore().fetchAgentById(this.agentId);
                    const agentInfo = useAgentStore().agent; 
                    this.agentData = agentInfo;
                    this.agentName = agentInfo.agent_name;
                    this.agentDescription = agentInfo.agent_description;
                    this.modelType = agentInfo.fm_provider_type;
                    this.selectedProvider = agentInfo.fm_provider_id;
                    this.selectedFoundationModel = agentInfo.fm_model_id;
                    this.temperature.value = agentInfo.fm_temperature;
                    this.topP.value = agentInfo.fm_top_p;
                    this.requestToken = agentInfo.fm_request_token_limit;
                    this.responseToken = agentInfo.fm_response_token_limit;
                    this.embeddingEnabled = agentInfo.embedding_enabled;
                    this.selectedEmbeddingProvider = agentInfo.embedding_provider_id;
                    this.selectedEmbeddingModel = agentInfo.embedding_model_id;
                    this.selectedStorageProvider = agentInfo.storage_provider_id;
                    this.selectedObject = agentInfo.storage_object_id;
                    this.selectedVectorDB = agentInfo.vector_db_provider_id;
                    this.processingEnabled = agentInfo.processing_enabled;
                    this.templateEnabled = agentInfo.template_enabled;
                    this.textareaTemplate = agentInfo.template; 
                    this.selectedPreProcessing = agentInfo.pre_processing_id;
                    this.selectedPostProcessing = agentInfo.post_processing_id;                    
                } catch (error) {
                    console.error('Error fetching agent data:', error);
                }
            }
        },
        async deleteAgent() {
            this.loading = true;
            this.errorMessage = '';
            this.successMessage = '';

            try {
                await useAgentStore().deleteAgent(this.agentId);
                this.successMessage = 'Agent deleted successfully.';
                this.router.push('/agent/list');
            } catch (error) {
                this.errorMessage = 'An error occurred while deleting the agent.';
            } finally {
                this.loading = false;
            }
        },
        async saveAgent() {
            this.loading = true;
            this.errorMessage = '';
            this.successMessage = '';

            if (!this.agentName || !this.selectedFoundationModel || !this.selectedProvider || !this.temperature.value || !this.topP.value || !this.requestToken || !this.responseToken || !this.selectedProvider || !this.userId) {
                this.errorMessage = 'Please enter the required information.';
                setTimeout(() => {
                    this.errorMessage = '';
                    this.successMessage = '';
                }, 2000);                
                return;
            }

            try {
                const agentData = {
                    user_id: this.userId,
                    agent_name: this.agentName,
                    agent_description: this.agentDescription,
                    fm_provider_type: this.modelType,
                    fm_provider_id: this.selectedProvider,
                    fm_model_id: this.selectedFoundationModel,
                    fm_temperature: this.temperature.value,
                    fm_top_p: this.topP.value,
                    fm_request_token_limit: this.requestToken,
                    fm_response_token_limit: this.responseToken,
                    embedding_enabled: this.embeddingEnabled,
                    embedding_provider_id: this.selectedEmbeddingProvider,
                    embedding_model_id: this.selectedEmbeddingModel,
                    storage_provider_id: this.selectedStorageProvider,
                    storage_object_id: this.selectedObject,
                    vector_db_provider_id: this.selectedVectorDB,
                    processing_enabled: this.processingEnabled,
                    pre_processing_id: this.selectedPreProcessing,
                    post_processing_id: this.selectedPostProcessing,
                    template_enabled: this.templateEnabled,
                    template: this.textareaTemplate,      
                    creator_id: this.userId,
                    updater_id: this.userId
                };

                if (this.agentId) {
                    agentData.agent_id = this.agentId;
                    await useAgentStore().updateAgent(agentData);
                    
                } else {
                    await useAgentStore().createAgent(agentData);
                    const agentInfo = useAgentStore().agent;
                    this.agentId = agentInfo.agent_id;
                }   
                this.successMessage = 'Agent updated successfully.';
            } catch (error) {
                this.errorMessage = 'An error occurred while creating the agent.';
            } finally {
                this.loading = false;
                setTimeout(() => {
                    this.errorMessage = '';
                    this.successMessage = '';
                }, 2000);                  
            }
        },
        async createIndexing() {
            this.loading = true;
            this.errorMessage = '';
            this.successMessage = '';

            try {
                let embeddings = {
                    user_id: this.userId,
                    embedding_provider_id: this.selectedEmbeddingProvider,
                    embedding_model_id: this.selectedEmbeddingModel,
                    storage_provider_id: this.selectedStorageProvider,
                    storage_object_id: this.selectedObject,
                    vector_db_provider_id: this.selectedVectorDB
                };                
                await useStorageStore().createIndexing(embeddings);
                this.successMessage = 'Agent updated successfully.';
            } catch (error) {
                console.error('An error occurred while deleting the storage.', error);
            } finally {
                this.loading = false;
                setTimeout(() => {
                    this.errorMessage = '';
                    this.successMessage = '';
                }, 2000);  
            }
        },
        async loadFiles(storeName) {
          try {
            const files = await useStorageStore().fetchFiles(this.userId, storeName);
            this.filteredFiles = files;
          } catch (error) {
            console.error('Error loading files:', error);
          }
        },
        getFileName(filePath) {
          if (filePath && filePath.lastIndexOf('/') !== -1) {
            return filePath.substring(filePath.lastIndexOf('/') + 1);
          }
          return filePath;
        }
    },
    async mounted() {
        this.router = useRouter();

        this.loading = true

        try {
            const tasks = [
                !this.router.currentRoute.query.agentId && useAgentStore().resetAgent(),
                useProviderStore().fetchCredential({ userId: this.userId }),
                useProviderStore().fetchModels(),
                useProcessingStore().fetchProcessingsById({ userId: this.userId }),
                useStorageStore().fetchAllStorages(this.userId)            
            ];

            await Promise.all(tasks);

            if (this.credentials.length > 0) {
                this.selectedProvider = this.filteredProviders[0]?.credentials_id || '';
                this.selectedEmbeddingProvider = this.filteredEmbeddingProviders[0]?.credentials_id || '';
                this.selectedStorageProvider = this.filteredStorageProviders[0]?.credentials_id || '';
                this.selectedVectorDB = this.filteredVectorDBProviders[0]?.credentials_id || '';
            }
            if (this.processings.length > 0) {
                this.selectedPreProcessing = this.filteredPreProcessings[0]?.processing_id || '';
                this.selectedPostProcessing = this.filteredPostProcessings[0]?.processing_id || '';
            }
            if (this.storages.length > 0) {
                this.selectedObject = this.filteredObjects[0]?.store_id || '';
                // const firstStore = this.filteredObjects[0];
                // if (firstStore?.store_name) {
                //     await this.loadFiles(firstStore.store_name);
                // }
            }
            if (this.router.currentRoute.query.agentId || this.agentId) {
                await this.fetchAgentData();
            }
        } catch (error) {
            console.error('Error agents loading:', error);
        } finally {
            this.loading = false;
        }   
    }    
}
</script>

<style scoped>
.fa {
    font: normal normal normal 30px / 1 FontAwesome;
}
.fa-minus {
    font: normal normal normal 10px / 1 FontAwesome;
}
.fa-plus {
    font: normal normal normal 10px / 1 FontAwesome;
}
.product-name {
    margin-left: 10px;
}
.prooduct-details-box {
    cursor: pointer;
    padding: 10px;
}
.media.selected {
    border: 2px solid #007bff;
    background-color: #e7f1ff;
}
.form-control-primary {
    border-color: var(--theme-deafult);
    color: var(--theme-deafult);
}
.disabled-card {
    pointer-events: none;
    opacity: 0.6;
}
.loader-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5); /* 검정색 배경, 투명도 조절 가능 */
    z-index: 999; /* 로딩 오버레이가 최상위에 오도록 설정 */
    display: flex;
    justify-content: center;
    align-items: center;
}

.loader-box {
    width: 100px; /* 로딩 바의 너비 설정 */
    height: 100px; /* 로딩 바의 높이 설정 */
    background-color: #fff; /* 로딩 바의 배경색 */
    border-radius: 10px; /* 로딩 바 모서리 둥글게 */
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.5); /* 로딩 바에 그림자 효과 추가 */
}
</style>