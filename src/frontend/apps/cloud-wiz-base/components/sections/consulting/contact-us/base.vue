<template>
  <section id="contacts-1" class="pb-50 inner-page-hero contacts-section division">
    <div class="container">
      <!-- SECTION TITLE -->
      <div class="row justify-content-center">
        <div class="col-md-10 col-lg-9">
          <div class="section-title text-center mb-80">
            <!-- Title -->
            <h2 class="s-52 w-700">Questions? Let's Talk</h2>
            <!-- Text -->
            <p class="p-lg">Want to learn more about CloudWiz AI, get a quote, or speak with an expert? Let us know what you are looking for and we’ll get back to you right away</p>
          </div>
        </div>
      </div>
      <!-- CONTACT FORM -->
      <div class="row justify-content-center">
        <div class="col-md-11 col-lg-10 col-xl-8">
          <div class="form-holder">
            <Form as="form" v-slot="{ errors, values, handleSubmit }">
              <form name="contactus" class="row contact-form" @submit.prevent="handleSubmit($event, onSubmit)">
                <!-- Contact Form Input -->
                <div class="col-md-12">
                  <Field type="text"
                         name="name"
                         rules="required"
                         id="customer_name"
                         v-slot="{ field }"
                         v-model="formData.customer_name" >
                    <p class="p-lg">Your Name:</p>
                    <span>Please enter your nick name: </span>
                    <input v-bind="field" class="form-control name" placeholder="Your Name*" />
                  </Field>
                  <span class="color--theme">{{ errors.name }}</span>
                </div>
                <div class="col-md-12">
                  <Field type="text"
                         name="email"
                         rules="required|email"
                         id="customer_email"
                         v-slot="{ field }"
                         v-model="formData.customer_email" >
                    <p class="p-lg">Your Email Address:</p>
                    <span>Please carefully check your email address for accuracy</span>
                    <input v-bind="field" class="form-control email" placeholder="Email Address*" />
                  </Field>
                  <span class="color--theme">{{ errors.email }}</span>
                </div>
                <div class="col-md-12">
                  <p class="p-lg">Explain your question in details:</p>
                  <span>Please ask questions about any type of service.</span>
                  <textarea class="form-control message" name="content" rows="6" placeholder="I have a question with..." id="content" v-model="formData.content"></textarea>
                </div>
                <!-- Contact Form Button -->
                <div class="col-md-12 mt-15 form-btn text-right">
                  <button type="submit" class="btn btn--theme hover--theme submit">Submit Request</button>
                </div>
                <div class="contact-form-notice">
                  <p class="p-sm">We are committed to your privacy. CloudWiz AI uses the information you provide us to contact you about our relevant content, products, and services. You may unsubscribe from these communications at any time. </p>
                </div>
                <!-- Contact Form Message -->
                <div class="col-lg-12 contact-form-msg">
                  <span class="loading"></span>
                </div>
              </form>
            </Form>
          </div>
        </div>
      </div>
      <!-- END CONTACT FORM -->
      <Dialog />
    </div>
    <!-- End container -->
  </section>
  <hr class="divider" />
</template>

<script setup lang="ts">
import restApi from "~/utils/axios"
import { useCommonStore } from '~/store/common'
import Dialog from "~/components/elements/Dialog.vue";
import {useDialogStore} from "~/store/dialog";
import commonUtil from "~/utils/common";
import { ref } from 'vue';

const { get, post } = restApi()
const error = ref()
const pending = ref(true)
const formData = ref({
  customer_email: '',
  customer_name: '',
  content: '',
  contactUsTp: ''
})


const onSubmit = async () => {

  let dialog_title = 'Contact Us'
  let dialog_message = 'fail'
  let dialog_btn = 'Close'

  try {
    const response = await post('/contactus/', formData.value, null)

    console.log(response.data)
    // @ts-ignore
    if (commonUtil().isNotEmpty(response.data.value["contactus_id"].toString())) {
      dialog_message = 'You have been successfully submitted. We will give you a quick reply.'
    }

  } catch (err) {
    error.value = err
  } finally {
    pending.value = false
  }
  useDialogStore().openDialog(dialog_title, dialog_message, dialog_btn)
}
</script>
