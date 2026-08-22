<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-title>Suivi thermique</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true" class="ion-padding">
      <div class="login-container">
        <h2 id="title">Mot de passe oublié ?</h2>

        <form class="login-form" @submit.prevent="onFindPassword" v-if="showFormMel">
          <ion-item lines="full">
            <ion-label position="floating">Email :</ion-label>
            <ion-input v-model="email" type="email" name="email" autocomplete="username" required></ion-input>
          </ion-item>

          <ion-button expand="block" type="submit">
            Rechercher le compte
          </ion-button>

          <ion-button expand="block" fill="clear" type="button" @click="router.back()">
            Retour
          </ion-button>
        </form>
        <form class="login-form" @submit.prevent="onChangePassword" v-if="showFormMdp">
            <ion-label position="stacked">{{ titleEmailFound }}</ion-label>

          <ion-item lines="full">
            <ion-label position="floating">Mot de passe* : (entre 8 et 50 caractères)</ion-label>
            <ion-input
              :value="password"
              :type="passwordVisible ? 'text' : 'password'"
              name="password"
              autocomplete="current-password"
              @ionInput="onPasswordInput"
              required
            ></ion-input>
          </ion-item>

          <ion-button fill="clear" size="small" type="button" @click="togglePasswordVisibility">
            {{ passwordVisible ? 'Masquer' : 'Afficher' }} le mot de passe
          </ion-button>

          <ion-item lines="full">
            <ion-label position="floating">Mot de passe (à reconfirmer) :</ion-label>
            <ion-input
              :value="password2"
              :type="passwordVisible2 ? 'text' : 'password'"
              name="password2"
              autocomplete="current-password"
              @ionInput="onPasswordInput2"
              required
            ></ion-input>
          </ion-item>

          <ion-button fill="clear" size="small" type="button" @click="togglePasswordVisibility2">
            {{ passwordVisible2 ? 'Masquer' : 'Afficher' }} le mot de passe
          </ion-button>

          <ion-button expand="block" type="submit">
            Modifier le mot de passe
          </ion-button>

          <ion-button
            id="retry_btn"
            expand="block"
            fill="clear"
            type="button"
            @click="reinitaliser"
            >
            Recommencer
          </ion-button>

          <ion-button expand="block" fill="clear" type="button" @click="router.back()">
            Retour
          </ion-button>
        </form>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
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
} from '@ionic/vue';

const email = ref('');
const password = ref('');
const passwordVisible = ref(false);
const password2 = ref('');
const passwordVisible2 = ref(false);
const router = useRouter();
const showFormMel = ref(true)
const showFormMdp = ref(false)
const titleEmailFound = ref("Email")
const idC = ref(-1)

const showLoginError = async (message: string) => {
  const alert = await alertController.create({
    header: 'Connexion impossible',
    message,
    buttons: ['OK'],
  });

  await alert.present();
};

function reinitaliser(){
    showFormMel.value = true
    showFormMdp.value = false
    password.value = ""
    password2.value = ""
}

const togglePasswordVisibility = () => {
  passwordVisible.value = !passwordVisible.value;
};

const togglePasswordVisibility2 = () => {
  passwordVisible2.value = !passwordVisible2.value;
};

async function showAlert(header: string, message: string, buttons: string[] = ['OK']) {
    const alert = await alertController.create({
      header: header,
      message: message,
      buttons: buttons
    });

    await alert.present();
}

const onPasswordInput = (event: CustomEvent) => {
  password.value = event.detail.value ?? '';
};

const onPasswordInput2 = (event: CustomEvent) => {
  password2.value = event.detail.value ?? '';
};

const onChangePassword = async () => {
    if (password.value!= password2.value){
        await showLoginError("Les 2 mots de passes sont différents")
        return;
    }
    if (password.value.length < 8 ||password.value.length > 50){
        await showLoginError("Le mot de passe doit comporter entre 8 et 50 caractères. Il en comporte "+password.value.length+".")
        return
    }
    const response = await fetch(`http://127.0.0.1:8000/comptes/${idC.value}`, {
        method: "PATCH",
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
            mdp: password.value
        }),
    })
    if (!response.ok){
        const errorData = await response.json().catch(() => null);
        const errorMessage = typeof errorData?.detail === 'string'
          ? errorData.detail : 'Une erreur est survenue pendant la connexion.';
        await showLoginError(errorMessage);
        return;
    }
    const response2 = await fetch("http://127.0.0.1:8000/email/envoyer", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
            destinataire: email.value,
            sujet: "Suivi thermique",
            corps: "Bonjour,\n\nNous confirmons la modification de ton mot de passe pour le suivi thermique. Tu peux maintenant te connecter avec ce nouveau mot de passe.\n\nCordialement,\n\nLe suivi thermique."
        }),
    })
    if (response2.ok){
        await showAlert("Mot de passe oublié ?","Ton mot de passe a bien été modifié avec succès. Un mail de confirmation a été envoyé sur ton nouvel adresse mail.")
    } else {
        await showAlert("Mot de passe oublié ?","Ton mot de passe a bien été modifié avec succès")
    }
    router.back()
}

const onFindPassword = async () => {
    const response = await fetch("http://127.0.0.1:8000/comptes/find", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
            email: email.value,
        }),
    })
    if (!response.ok){
        showLoginError("L'adresse mail saisi ne figure pas dans la base de données. Autrement, il y aurait peut-être un problème de connexion.")
        return
    }
    const data = await response.json()
    idC.value = data.id
    showFormMel.value = false
    showFormMdp.value = true
    titleEmailFound.value = "Email : " + email.value
}

function regex(pattern: string, value: string): boolean {
    const regex = new RegExp(pattern);
    return regex.test(value);
}
</script>

<style scoped>
.no_display{
    display: none;
}

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
