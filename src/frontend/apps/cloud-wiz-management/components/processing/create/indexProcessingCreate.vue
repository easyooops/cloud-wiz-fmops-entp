<template>
    <Breadcrumbs main="Processing" title="Processing Create" />

    <div class="container-fluid">
        <div class="loader-overlay" v-if="loading">
            <div class="loader-box">
                <div class="loader-30"></div>
            </div>
        </div>

        <div class="row">
            <div class="col-sm-12">
                <form @submit.prevent="createOrUpdateProcessing">
                <!-- Button -->
                <div class="card">
                    <div class="card-body">  
                        <div class="row">
                            <div class="col-sm-12">
                                <button type="submit" class="btn btn-primary me-2">Submit</button>
                                <button @click.prevent="deleteProcessing" class="btn btn-danger me-2">Delete</button>
                                <router-link to="/processing/list" class="btn btn-secondary">Back to List</router-link>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Type -->
                <div class="card">
                    <div class="card-body">  
                        <div class="row">
                            <div class="col-sm-4">
                                <div class="col-form-label"><h5>Processing Type *</h5></div>
                                <select class="form-select form-control-primary" v-model="processingType" :disabled="isEditMode">
                                    <option value="pre">Pre-Processing</option>
                                    <option value="post">Post-Processing</option>
                                </select>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-sm-6 mt-3">
                                <div class="col-form-label">Processing Name *</div>
                                <input v-model="processingName" class="form-control form-control-primary" type="text" placeholder="Processing Name *" required>
                            </div>
                            <div class="col-sm-6 mt-3">
                                <div class="col-form-label">Processing Description</div>
                                <input v-model="processingDesc" class="form-control form-control-primary" type="text" placeholder="Processing Description">
                            </div>                            
                        </div>                        
                    </div>
                </div>

                <!-- Template -->
                <!-- <div class="card" v-if="processingType === 'pre'">
                    <div class="card-body">                  
                        <div class="row">
                            <div class="col-sm-12">
                                <label class="col-form-label"><h5>Template</h5></label>
                                <textarea v-model="textareaTemplate" class="form-control form-control-primary" id="textareaTemplate" rows="5"></textarea>
                            </div>
                        </div> 
                    </div>
                </div> -->

                <!-- PII Masking -->
                <div class="card">
                    <div class="card-body">                                                     
                        <div class="row">
                            <div class="col">
                                <div class="mb-3">
                                    <label class="col-form-label"><h5>PII Masking</h5></label>
                                    <div class="form-group m-t-15 m-checkbox-inline mb-0">
                                        <div v-for="(option, index) in piiMaskingOptions" :key="index" class="checkbox checkbox-dark">
                                            <input :id="option.id" type="checkbox" v-model="option.checked">
                                            <label :for="option.id">{{ option.label }}</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Normalization -->
                <div class="card">
                    <div class="card-body">                                                     
                        <div class="row">
                            <div class="col">
                                <div class="mb-3">
                                    <label class="col-form-label"><h5>Normalization</h5></label>
                                    <div class="form-group m-t-15 m-checkbox-inline mb-0">
                                        <div v-for="(option, index) in normalizationOptions" :key="index" class="checkbox checkbox-dark">
                                            <input :id="option.id" type="checkbox" v-model="option.checked">
                                            <label :for="option.id">{{ option.label }}</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Stopword Removal -->
                <div class="card">
                    <div class="card-body">                                                     
                        <div class="row">
                            <div class="col">
                                <div class="mb-3">
                                    <label class="col-form-label"><h5>Stopword Removal</h5></label>
                                    <textarea v-model="textareaStopword" class="form-control form-control-primary" id="textareStopword" rows="5"></textarea>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
                <div v-if="successMessage" class="alert alert-success mt-3">{{ successMessage }}</div>                                        
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, watch, onMounted, computed } from 'vue';
import { useProcessingStore } from '@/store/processing';
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';

export default {
    name: 'createProcessing',
    setup() {
        const processingStore = useProcessingStore();
        const router = useRouter();
        
        const processingType = ref('pre');
        const processingName = ref('');
        const processingDesc = ref('');
        // const textareaTemplate = ref('"""\n<Question>{question}</Question>\n<Context>Summarize it</Context>\n<Answer>\nSummarize within 250 characters.\nTranslate into Korean.\nIf you don`t know, say you don`t know. Don`t make things up.\n</Answer>\n"""');
        const textareaStopword = ref('CLOUDWIZ|AI|FMOPS');
        const loading = ref(false);
        const errorMessage = ref(null);
        const successMessage = ref(null);
        const isEditMode = ref(false);
        const userId = ref(useAuthStore().userId);

        const piiMaskingOptions = ref([
            { id: 'email', label: 'Email', checked: false },
            { id: 'phone', label: 'Phone', checked: false },
            { id: 'credit_card', label: 'Credit Card', checked: false },
            { id: 'zip', label: 'Zip', checked: false },
            { id: 'name', label: 'Name', checked: false },
            { id: 'ssn', label: 'SSN', checked: false },
            { id: 'birthdate', label: 'Birthdate', checked: false },
            { id: 'driver_license', label: 'Driver License', checked: false },
            { id: 'bank_account', label: 'Bank Account', checked: false },
            { id: 'social_media', label: 'Social Media Account', checked: false },
            { id: 'medical_records', label: 'Medical Records', checked: false },
            { id: 'passport_number', label: 'Passport Number', checked: false }
        ]);

        const normalizationOptions = ref([
            { id: 'trim', label: 'Trim leading and trailing whitespace', checked: false },
            { id: 'duplicate_spaces', label: 'Remove duplicate spaces', checked: false },
            { id: 'newline', label: 'Remove newline characters', checked: false },
            { id: 'numbers', label: 'Remove numbers', checked: false },
            { id: 'lowercase', label: 'Convert to lowercase', checked: false },
            { id: 'uppercase', label: 'Convert to uppercase', checked: false },
            { id: 'html_tags', label: 'Remove HTML tags', checked: false },
            { id: 'urls', label: 'Remove URLs', checked: false },
            { id: 'emails', label: 'Remove email addresses', checked: false },
            { id: 'normalize_special_chars', label: 'Normalize special characters', checked: false },
            { id: 'punctuation', label: 'Remove punctuation', checked: false }
        ]);

        const fetchProcessing = async (processingId) => {
            loading.value = true;
            try {
                const processing = await processingStore.getProcessingById(processingId);
                if (processing) {
                    processingType.value = processing.processing_type;
                    processingName.value = processing.processing_name;
                    processingDesc.value = processing.processing_desc;
                    // textareaTemplate.value = processing.template;
                    textareaStopword.value = processing.stopword_removal;

                    // Update piiMaskingOptions and normalizationOptions based on processing data
                    updateCheckboxOptions(processing.pii_masking, 'pii');
                    updateCheckboxOptions(processing.normalization, 'normalization');

                    isEditMode.value = true;
                } else {
                    errorMessage.value = 'Processing not found.';
                }
            } catch (error) {
                errorMessage.value = 'Error fetching processing details.';
            } finally {
                loading.value = false;
            }
        };

        const updateCheckboxOptions = (selectedIds, type) => {
            const options = type === 'pii' ? piiMaskingOptions.value : normalizationOptions.value;
            options.forEach(option => {
                option.checked = selectedIds.split('|').includes(option.id);
            });
        };

        const createOrUpdateProcessing = async () => {
            loading.value = true;
            errorMessage.value = null;
            successMessage.value = null;

            const selectedPiiMaskingIds = getPiiMaskingSelectedIds();
            const selectedNormalizationIds = getNormalizationSelectedIds();

            try {
                if (isEditMode.value) {
                    await processingStore.updateProcessing({
                        processing_id: router.currentRoute.value.query.processingId,
                        processing_type: processingType.value,
                        processing_name: processingName.value,
                        processing_desc: processingDesc.value,
                        // template: textareaTemplate.value,
                        pii_masking: selectedPiiMaskingIds,
                        normalization: selectedNormalizationIds,
                        stopword_removal: textareaStopword.value,
                        updater_id: userId.value
                    });
                    successMessage.value = 'Processing updated successfully.';
                } else {
                    await processingStore.createProcessing({
                        user_id: userId.value,
                        processing_type: processingType.value,
                        processing_name: processingName.value,
                        processing_desc: processingDesc.value,
                        // template: textareaTemplate.value,
                        pii_masking: selectedPiiMaskingIds,
                        normalization: selectedNormalizationIds,
                        stopword_removal: textareaStopword.value,
                        creator_id: userId.value,
                        updater_id: userId.value
                    });
                    successMessage.value = 'Processing created successfully.';
                }
                router.push('/processing/list');
            } catch (error) {
                errorMessage.value = 'An error occurred while saving the processing.';
            } finally {
                loading.value = false;
            }
        };

        const getPiiMaskingSelectedIds = () => {
            return piiMaskingOptions.value.filter(option => option.checked).map(option => option.id).join('|');
        };

        const getNormalizationSelectedIds = () => {
            return normalizationOptions.value.filter(option => option.checked).map(option => option.id).join('|');
        };

        const handleCheckboxChange = (option, index, type) => {
            if (type === 'pii') {
                piiMaskingOptions.value[index].checked = option.checked;
            } else if (type === 'normalization') {
                normalizationOptions.value[index].checked = option.checked;
            }
        };

        const deleteProcessing = async () => {
            loading.value = true;
            errorMessage.value = null;
            successMessage.value = null;

            try {
                const processingId = router.currentRoute.value.query.processingId;                
                await processingStore.deleteProcessing(processingId);
                successMessage.value = 'Processing deleted successfully.';
            } catch (error) {
                errorMessage.value = 'An error occurred while deleting the processing.';
            } finally {
                loading.value = false;
                router.push('/processing/list');
            }
        };

        onMounted(() => {
            const processingId = router.currentRoute.value.query.processingId;
            if (processingId) {
                fetchProcessing(processingId);
            }
        });

        watch(() => router.currentRoute.value.query.processingId, (newProcessingId, oldProcessingId) => {
            if (newProcessingId !== oldProcessingId) {
                fetchProcessing(newProcessingId);
            }
        });


        return {
            processingType,
            processingName,
            processingDesc,
            // textareaTemplate,
            textareaStopword,
            piiMaskingOptions,
            normalizationOptions,
            handleCheckboxChange,
            loading,
            errorMessage,
            successMessage,
            createOrUpdateProcessing,
            deleteProcessing,
            isEditMode
        };
    }
}
</script>

<style scoped>
.form-control-primary {
    border-color: var(--theme-deafult);
    color: var(--theme-deafult);
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
