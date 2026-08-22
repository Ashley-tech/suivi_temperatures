<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-title>Suivi thermique</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true" class="ion-padding">
      <div class="login-container">
        <h2>Connexion</h2>

        <form class="login-form" @submit.prevent="onLogin">
          <ion-item lines="full">
            <ion-label position="floating">Email</ion-label>
            <ion-input v-model="email" type="email" name="email" autocomplete="username" required></ion-input>
          </ion-item>

          <ion-item lines="full">
            <ion-label position="floating">
              Mot de passe
            </ion-label>

            <ion-input
              v-model="password"
              type="password"
              name="password"
              autocomplete="current-password"
              :clear-on-edit="false"
              required
            >
              <ion-input-password-toggle
                slot="end"
              ></ion-input-password-toggle>
            </ion-input>
          </ion-item>

          <ion-button fill="clear" size="small" type="button" @click="goToForgotPassword">
            Mot de passe oublié ?
          </ion-button>

          <ion-button expand="block" type="submit">
            Se connecter
          </ion-button>

          <ion-button expand="block" fill="clear" type="button" @click="goToSignup">
            Créer un compte
          </ion-button>
        </form>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Cookies from 'js-cookie';
import {
  alertController,
  IonButton,
  IonContent,
  IonHeader,
  IonInput,
  IonItem,
  IonLabel,
  IonPage,
  IonTitle,
  IonToolbar,
  IonInputPasswordToggle,
} from '@ionic/vue';

const email = ref('');
const password = ref('');
const passwordVisible = ref(false);
const router = useRouter();

const showLoginError = async (message: string) => {
  const alert = await alertController.create({
    header: 'Connexion impossible',
    message,
    buttons: ['OK'],
  });

  await alert.present();
};

const onLogin = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({
        email: email.value,
        mdp: password.value,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      const errorMessage = typeof errorData?.detail === 'string'
        ? errorData.detail
        : 'Une erreur est survenue pendant la connexion.';

      await showLoginError(errorMessage);
      return;
    }

    const loginData = await response.json();
    Cookies.set('compte_id', String(loginData.user.id), {
      expires: 1,
      sameSite: 'lax',
    });
    Cookies.set('email', loginData.user.email_compte, {
      expires: 1,
      sameSite: 'lax',
    });
    sessionStorage.setItem('access_token', loginData.access_token);
    await router.replace({
      path: '/dashboard',
    });
  } catch {
    await showLoginError('Le serveur est inaccessible. Vérifiez qu\'il est démarré, puis réessayez.');
  }
};

const goToForgotPassword = () => {
  router.push("/password")
};

const goToSignup = () => {
  router.push("/signup")
};
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  padding: 24px 20px;
}

.login-form {
  width: 100%;
  max-width: 420px;
}

h2 {
  margin: 0 0 24px;
  font-size: 1.8rem;
  color: #111827;
}

ion-button {
  margin-top: 12px;
}
</style>
