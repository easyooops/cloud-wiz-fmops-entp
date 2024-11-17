<template>
  <v-dialog
      v-model="useDialogStore().dialog_status"
      width="auto"
  >
    <v-card>
      <v-card-title>
        {{ useDialogStore().dialog_title }}
      </v-card-title>
      <v-card-text>
        {{ useDialogStore().dialog_message }}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="useDialogStore().dialog_status = false">
          {{ useDialogStore().dialog_btn_text }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
  import {useDialogStore} from "~/store/dialog";

</script>