<template>
    <v-container
        fluid
    >
        <v-row>
            <v-menu
                min-width="200px"
                rounded
            >
                <template v-slot:activator="{ props }">
                    <v-btn
                        icon
                        v-bind="props"
                    >
                        <v-avatar
                            color="brown"
                            size="large"
                        >
                            <span class="text-h5">{{ user.initials }}</span>
                        </v-avatar>
                    </v-btn>
                </template>
                <v-card>
                    <v-card-text>
                        <div class="mx-auto text-center">
                            <v-avatar
                                color="brown"
                            >
                                <span class="text-h5">{{ user.initials }}</span>
                            </v-avatar>
                            <h5>{{ user.fullName }}</h5>
                            <p class="text-caption mt-1">
                                {{ user.email }}
                            </p>
                            <v-list>
                                <v-list-item v-for="(item, index) in profileMenu" :key="index">
                                    <v-divider class="my-1"></v-divider>
                                    <v-btn rounded variant="text" @click=navigateTo(item.Destination)>{{ item.title }}</v-btn>
                                </v-list-item>
                            </v-list>
                        </div>
                    </v-card-text>
                </v-card>
            </v-menu>
        </v-row>
    </v-container>
</template>

<script setup lang="ts">
  const profileMenu = [
      { title: 'Edit Account', Destination: "/preparing"},
      { title: 'Disconnect', Destination: "/logout"},
  ];
  const user = {
      initials: 'JD',
      fullName: 'John Doe',
      email: 'john.doe@doe.com',
  }
</script>