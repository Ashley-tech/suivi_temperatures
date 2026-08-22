<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-title>Suivi thermique</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true" class="ion-padding">
      <div class="signup-container">
        <h2>Inscription</h2>

        <form class="signup-form" @submit.prevent="inscrire">
          <ion-item lines="full">
            <ion-label position="floating">Email* :</ion-label>
            <ion-input v-model="email" type="email" name="email" autocomplete="username" required></ion-input>
          </ion-item>

          <ion-item lines="full">
            <ion-label position="floating">Email* (à reconfirmer) :</ion-label>
            <ion-input v-model="email2" type="email" name="email2" autocomplete="username" required></ion-input>
          </ion-item>

          <ion-item lines="full">
            <ion-label position="floating">Mot de passe* <i>(Minimum 8 caractères)</i> :</ion-label>
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
              ></ion-input-password-toggle></ion-input>
          </ion-item>

          <ion-item lines="full">
            <ion-label position="floating">Mot de passe* (à reconfirmer) :</ion-label>
            <ion-input
              v-model="password2"
              name="passwordr"
              type="password"
              autocomplete="current-password"
              :clear-on-edit="false"
              required
            >
          <ion-input-password-toggle
                slot="end"
              ></ion-input-password-toggle></ion-input>
          </ion-item>

          <ion-item lines="full">
            <ion-label position="floating">Nom de famille* :</ion-label>
            <ion-input v-model="ln" type="text" name="nom" autocomplete="username" required></ion-input>
          </ion-item>

          <ion-item lines="full">
            <ion-label position="floating">Prénom* :</ion-label>
            <ion-input v-model="fn" type="text" name="prenom" autocomplete="username" required></ion-input>
          </ion-item>

          <ion-item lines="full">
            <ion-label position="floating">Téléphone <i>(Maximum 20 caractères)</i> :</ion-label>
            <ion-input v-model="tel" type="text" name="tel"></ion-input>
          </ion-item>

          <ion-item lines="full">
            <ion-label position="floating">Adresse :</ion-label>
            <ion-input v-model="adresse" type="text" name="adresse"></ion-input>
          </ion-item>

          <ion-item lines="full">
            <ion-label position="floating">Complément d'adresse :</ion-label>
            <ion-input v-model="compadresse" type="text" name="compadresse"></ion-input>
          </ion-item>

          <ion-item lines="full">
            <ion-label position="floating">Code postal :</ion-label>
            <ion-input v-model="cp" type="text" name="cp"></ion-input>
          </ion-item>

          <ion-item lines="full">
            <ion-label position="floating">Ville :</ion-label>
            <ion-input v-model="ville" type="text" name="ville"></ion-input>
          </ion-item>

          <ion-item lines="full">
            <ion-label position="floating">Pays :</ion-label>
            <ion-input v-model="pays" type="text" name="pays"></ion-input>
          </ion-item>

          <ion-item lines="full">
            <ion-label position="floating">Ta fonction :</ion-label>
            <ion-textarea v-model="fonc" type="text" name="fonc"></ion-textarea>
          </ion-item>

          <ion-button expand="block" type="submit">
            Créer le compte
          </ion-button>

          <ion-button expand="block" fill="clear" type="button" @click="router.back()">
            Annuler
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
  IonInputPasswordToggle,
  IonToolbar,
} from '@ionic/vue';

const email = ref('');
const email2 =ref("")
const password = ref('');
const password2 = ref('');
const passwordVisible = ref(false);
const passwordVisible2 = ref(false);
const router = useRouter();
const ln = ref('')
const fn = ref('')
const tel = ref('')
const adresse = ref('')
const compadresse = ref('')
const cp=ref('')
const ville = ref('')
const pays = ref('')
const fonc = ref('')

const showAlert = async (header: string, message: string, buttons: string[] = ['OK']) => {
  const alert = await alertController.create({
    header,
    message,
    buttons,
  });

  await alert.present();
};

const inscrire = async () => {
    if (email.value != email2.value) {
        await showAlert("Erreur lors de l'inscription","Les 2 adresses mail sont différents !")
        return;
    }
    if (password.value != password2.value) {
        await showAlert("Erreur lors de l'inscription","Les 2 mots de passe sont différents !")
        return;
    }
    if (password.value.length < 8 || password.value.length > 50){
        await showAlert("Erreur lors de l'inscription","Le mot de passe doit comporter entre 8 et 50 caractères. Il en comporte "+password.value.length+".")
        return;
    }
    if (tel.value.length > 20){
        await showAlert("Erreur lors de l'inscription","Le numéro de téléphon ne doit pas avoir plus de 20 caractères.")
        return;
    }
    try {
        const response = await fetch("http://127.0.0.1:8000/comptes/find",{
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                email: email.value
            }),
        });
        if (response.ok) {
            await showAlert("Erreur lors de l'inscription","L'adresse email saisi est déjà utilisée. Veuillez en saisir une autre.");
            return;
        }
        const response1 = await fetch("http://127.0.0.1:8000/comptes", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                nom_compte: ln.value,
                prenom_compte: fn.value,
                email_compte: email.value,
                mdp: password.value,
                tel: tel.value,
                adresse: adresse.value,
                adresse_comp: compadresse.value,
                cp: cp.value,
                ville: ville.value,
                pays: pays.value,
                fonction: fonc.value
            }),
        })

        if (!response1.ok) {
            const errorData = await response.json().catch(() => null);
              const errorMessage = formatApiError(errorData, response.status);

            await showAlert("Erreur lors de l'inscription",errorMessage);
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
                sujet: "Inscription pour le suivi thermique",
                corps: "Bonjour,\n\nNous confirmons ton inscription pour le suivi thermique.\nDésormais, tu vas pouvoir enregistrer tes températures.\n\nCordialement,\n\nLe suivi thermique."
            }),
        })
        if (response2.ok){
            await showAlert("Inscription réussie","Ton inscription a bien été effectué. Tu recevras un mail de confirmation. Retour au formulaire de connexion.")
        } else {
            await showAlert("Inscription réussie - Echec d'envoi de mail","Ton inscription a bien été effectué, mais nous n'avons pas tu t'envoyer de mail de confirmation. Retour au formulaire de connexion.")
        }
        router.back()
    } catch (error) {
      const errorMessage = error instanceof Error
        ? error.message
        : 'La requête a échoué sans fournir de détails.';
      await showAlert("Erreur lors de l'inscription", `Impossible de créer ton compte : ${errorMessage}`);
    }
}

  const formatApiError = (errorData: unknown, status: number): string => {
    if (typeof errorData === 'object' && errorData !== null && 'detail' in errorData) {
      const detail = errorData.detail;

      if (typeof detail === 'string') {
        return detail;
      }

      if (Array.isArray(detail)) {
        return detail.map((error) => {
          if (typeof error === 'object' && error !== null && 'loc' in error && 'msg' in error) {
            const location = Array.isArray(error.loc) ? error.loc.join('.') : String(error.loc);
            return `${location} : ${error.msg}`;
          }
          return String(error);
        }).join('\n');
      }
    }

    return `Le serveur a renvoyé une erreur (${status}).`;
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
